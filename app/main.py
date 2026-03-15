"""
Peblo Quiz Engine - FastAPI Backend

An AI-powered quiz generator that creates quizzes from PDF documents.
"""
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db, init_db
from app.models import Source, ContentChunk, Question, StudentAnswer
from app.ingest import ingest_pdf, store_chunks
from app.quiz_generator import generate_questions, save_questions_to_db

# Initialize FastAPI app
app = FastAPI(
    title="Peblo Quiz Engine",
    description="An AI-powered quiz generator for PDF documents",
    version="0.1.0"
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup"""
    init_db()


# ==================== API Models ====================
from pydantic import BaseModel


class SourceSchema(BaseModel):
    id: Optional[int] = None
    name: str
    subject: str
    grade: str

    class Config:
        from_attributes = True


class ContentChunkSchema(BaseModel):
    id: Optional[int] = None
    source_id: int
    topic: str
    text: str

    class Config:
        from_attributes = True


class QuestionSchema(BaseModel):
    id: Optional[int] = None
    chunk_id: int
    question: str
    type: str
    options: Optional[List] = None
    answer: str
    difficulty: str

    class Config:
        from_attributes = True


class StudentAnswerSchema(BaseModel):
    id: Optional[int] = None
    student_id: int
    question_id: int
    selected_answer: str
    is_correct: bool

    class Config:
        from_attributes = True


# ==================== API Routes ====================

@app.get("/", tags=["root"])
async def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to Peblo Quiz Engine",
        "docs": "/docs",
        "version": "0.1.0"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# ==================== Source Routes ====================

@app.post("/sources", response_model=SourceSchema, tags=["sources"])
async def create_source(source: SourceSchema, db: Session = Depends(get_db)):
    """Create a new source"""
    new_source = Source(name=source.name, subject=source.subject, grade=source.grade)
    db.add(new_source)
    db.commit()
    db.refresh(new_source)
    return new_source


@app.get("/sources", response_model=List[SourceSchema], tags=["sources"])
async def get_sources(db: Session = Depends(get_db)):
    """Get all sources"""
    sources = db.query(Source).all()
    return sources


@app.get("/sources/{source_id}", response_model=SourceSchema, tags=["sources"])
async def get_source(source_id: int, db: Session = Depends(get_db)):
    """Get a specific source"""
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


# ==================== Content Chunk Routes ====================

@app.post("/chunks", response_model=List[int], tags=["chunks"])
async def create_chunks(
    source_id: int,
    topic: str = "General",
    db: Session = Depends(get_db)
):
    """Store text chunks for a source"""
    # This is typically called from the ingest process
    pass


@app.get("/sources/{source_id}/chunks", response_model=List[ContentChunkSchema], tags=["chunks"])
async def get_chunks(source_id: int, db: Session = Depends(get_db)):
    """Get all chunks for a source"""
    chunks = db.query(ContentChunk).filter(ContentChunk.source_id == source_id).all()
    return chunks


# ==================== Question Routes ====================

@app.get("/chunks/{chunk_id}/questions", response_model=List[QuestionSchema], tags=["questions"])
async def get_questions(chunk_id: int, db: Session = Depends(get_db)):
    """Get all questions for a chunk"""
    questions = db.query(Question).filter(Question.chunk_id == chunk_id).all()
    return questions


@app.post("/chunks/{chunk_id}/generate-questions", response_model=List[QuestionSchema], tags=["questions"])
async def generate_chunk_questions(chunk_id: int, difficulty: str = "Medium", db: Session = Depends(get_db)):
    """Generate questions for a chunk"""
    try:
        chunk = db.query(ContentChunk).filter(ContentChunk.id == chunk_id).first()
        if not chunk:
            raise HTTPException(status_code=404, detail="Chunk not found")

        # Generate questions - use mock mode for demo
        try:
            questions = generate_questions(chunk.text, difficulty=difficulty)
        except Exception as api_error:
            # Fallback to mock mode
            print(f"API Error, using mock mode: {str(api_error)}")
            from app.quiz_generator import generate_mock_questions
            questions = generate_mock_questions(chunk.text, difficulty=difficulty)

        # Save to database
        question_ids = save_questions_to_db(chunk_id, questions, db)

        # Return created questions
        created_questions = db.query(Question).filter(Question.id.in_(question_ids)).all()
        return created_questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Student Answer Routes ====================

@app.post("/answers", response_model=StudentAnswerSchema, tags=["answers"])
async def submit_answer(
    student_id: int,
    question_id: int,
    selected_answer: str,
    db: Session = Depends(get_db)
):
    """Submit a student answer"""
    try:
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        # Check if answer is correct
        is_correct = selected_answer.lower().strip() == question.answer.lower().strip()

        answer = StudentAnswer(
            student_id=student_id,
            question_id=question_id,
            selected_answer=selected_answer,
            is_correct=is_correct
        )
        db.add(answer)
        db.commit()
        db.refresh(answer)
        return answer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/students/{student_id}/answers", response_model=List[StudentAnswerSchema], tags=["answers"])
async def get_student_answers(student_id: int, db: Session = Depends(get_db)):
    """Get all answers from a student"""
    answers = db.query(StudentAnswer).filter(StudentAnswer.student_id == student_id).all()
    return answers


# ==================== PDF Upload ====================

@app.post("/upload-pdf", tags=["pdf"])
async def upload_pdf(
    file: UploadFile = File(...),
    source_id: Optional[int] = None,
    topic: str = "General",
    db: Session = Depends(get_db)
):
    """Upload and process a PDF file"""
    try:
        import tempfile
        from pathlib import Path

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name

        # Extract and chunk PDF
        chunks = ingest_pdf(tmp_path)

        # Create source if not provided
        if not source_id:
            source = Source(
                name=file.filename,
                subject="General",
                grade="General"
            )
            db.add(source)
            db.commit()
            source_id = source.id

        # Store chunks in database
        chunk_ids = store_chunks(source_id, chunks, topic=topic, db=db)

        # Clean up temp file
        Path(tmp_path).unlink()

        return {
            "filename": file.filename,
            "source_id": source_id,
            "chunks_created": len(chunk_ids),
            "chunk_ids": chunk_ids
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
