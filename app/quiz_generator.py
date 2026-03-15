"""
Quiz Generator Module

This module handles automatic quiz generation from text content.
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models import Quiz, Question, QuestionOption


class QuizGenerator:
    """Generates quiz content from text"""

    def __init__(self, db: Optional[Session] = None):
        self.db = db

    def generate_quiz_from_text(
        self,
        title: str,
        content: str,
        num_questions: int = 5,
        source_pdf: Optional[str] = None
    ) -> Quiz:
        """
        Generate a quiz from text content.

        Args:
            title: Quiz title
            content: Text content to generate questions from
            num_questions: Number of questions to generate
            source_pdf: Source PDF file name

        Returns:
            Quiz object with generated questions
        """
        # Create quiz
        quiz = Quiz(
            title=title,
            description=f"Auto-generated quiz from PDF: {source_pdf}" if source_pdf else "Auto-generated quiz",
            source_pdf=source_pdf
        )

        if self.db:
            self.db.add(quiz)
            self.db.commit()
            self.db.refresh(quiz)

        # TODO: Implement actual question generation logic
        # This could integrate with an LLM API to generate questions
        # For now, this is a placeholder structure

        return quiz

    def generate_question(self, content: str) -> dict:
        """
        Generate a single question from content.

        Args:
            content: Text content to generate question from

        Returns:
            Dictionary with question data
        """
        # TODO: Implement LLM-based question generation
        return {
            "question_text": "Sample question?",
            "question_type": "multiple_choice",
            "options": [
                {"option_text": "Option A", "is_correct": 1},
                {"option_text": "Option B", "is_correct": 0},
                {"option_text": "Option C", "is_correct": 0},
                {"option_text": "Option D", "is_correct": 0},
            ]
        }

    def add_question_to_quiz(
        self,
        quiz_id: int,
        question_text: str,
        options: list[dict],
        question_type: str = "multiple_choice"
    ) -> Question:
        """
        Add a question to an existing quiz.

        Args:
            quiz_id: ID of the quiz
            question_text: Question text
            options: List of question options with is_correct flag
            question_type: Type of question

        Returns:
            Question object
        """
        if not self.db:
            raise ValueError("Database session required")

        question = Question(
            quiz_id=quiz_id,
            question_text=question_text,
            question_type=question_type
        )

        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)

        # Add options
        for idx, option in enumerate(options):
            q_option = QuestionOption(
                question_id=question.id,
                option_text=option["option_text"],
                is_correct=option.get("is_correct", 0),
                order=idx
            )
            self.db.add(q_option)

        self.db.commit()
        return question
