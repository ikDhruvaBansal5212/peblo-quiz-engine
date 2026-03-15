from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    subject = Column(String(100), nullable=False)
    grade = Column(String(50), nullable=False)

    # Relationships
    content_chunks = relationship("ContentChunk", back_populates="source", cascade="all, delete-orphan")


class ContentChunk(Base):
    __tablename__ = "content_chunks"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    topic = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)

    # Relationships
    source = relationship("Source", back_populates="content_chunks")
    questions = relationship("Question", back_populates="chunk", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(Integer, ForeignKey("content_chunks.id"), nullable=False)
    question = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)  # MCQ, TrueFalse, FillBlank
    options = Column(JSON, nullable=True)  # List of options for MCQ
    answer = Column(Text, nullable=False)
    difficulty = Column(String(50), nullable=False)  # Easy, Medium, Hard

    # Relationships
    chunk = relationship("ContentChunk", back_populates="questions")
    student_answers = relationship("StudentAnswer", back_populates="question", cascade="all, delete-orphan")


class StudentAnswer(Base):
    __tablename__ = "student_answers"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)  # Can be extended to ForeignKey if Student table exists
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)

    # Relationships
    question = relationship("Question", back_populates="student_answers")
