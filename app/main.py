"""
Peblo Quiz Engine - FastAPI Backend

An AI-powered quiz generator that creates quizzes from PDF documents.
"""
from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db, init_db
from app.models import Quiz, Question, QuestionOption
from app.ingest import PDFIngester
from app.quiz_generator import QuizGenerator

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


class QuestionOptionSchema(BaseModel):
    id: Optional[int] = None
    option_text: str
    is_correct: bool
    order: int

    class Config:
        from_attributes = True


class QuestionSchema(BaseModel):
    id: Optional[int] = None
    quiz_id: Optional[int] = None
    question_text: str
    question_type: str = "multiple_choice"
    options: List[QuestionOptionSchema] = []

    class Config:
        from_attributes = True


class QuizSchema(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    source_pdf: Optional[str] = None
    questions: List[QuestionSchema] = []

    class Config:
        from_attributes = True


class QuizCreateSchema(BaseModel):
    title: str
    description: Optional[str] = None
    source_pdf: Optional[str] = None


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


@app.get("/quizzes", response_model=List[QuizSchema], tags=["quizzes"])
async def get_quizzes(db: Session = Depends(get_db)):
    """Get all quizzes"""
    quizzes = db.query(Quiz).all()
    return quizzes


@app.post("/quizzes", response_model=QuizSchema, tags=["quizzes"])
async def create_quiz(
    quiz_data: QuizCreateSchema,
    db: Session = Depends(get_db)
):
    """Create a new quiz"""
    quiz = Quiz(
        title=quiz_data.title,
        description=quiz_data.description,
        source_pdf=quiz_data.source_pdf
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return quiz


@app.get("/quizzes/{quiz_id}", response_model=QuizSchema, tags=["quizzes"])
async def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """Get a specific quiz by ID"""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


@app.post("/quizzes/{quiz_id}/questions", response_model=QuestionSchema, tags=["questions"])
async def add_question(
    quiz_id: int,
    question_data: QuestionSchema,
    db: Session = Depends(get_db)
):
    """Add a question to a quiz"""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    question = Question(
        quiz_id=quiz_id,
        question_text=question_data.question_text,
        question_type=question_data.question_type
    )
    db.add(question)
    db.commit()
    db.refresh(question)

    # Add options
    for option in question_data.options:
        q_option = QuestionOption(
            question_id=question.id,
            option_text=option.option_text,
            is_correct=int(option.is_correct),
            order=option.order
        )
        db.add(q_option)
    db.commit()
    db.refresh(question)

    return question


@app.post("/upload-pdf", tags=["pdf"])
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF file for quiz generation"""
    try:
        ingester = PDFIngester()
        content = await file.read()
        saved_path = ingester.save_pdf(file.filename, content)
        return {
            "filename": file.filename,
            "saved_path": saved_path,
            "size": len(content)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
