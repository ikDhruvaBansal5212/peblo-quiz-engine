"""
Quiz Generator Module

This module generates quiz questions from text content using OpenAI API.
"""
import json
import os
from typing import Optional
from openai import OpenAI
from sqlalchemy.orm import Session
from app.models import Question


# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_questions(chunk_text: str, difficulty: str = "Medium") -> list[dict]:
    """
    Generate three types of quiz questions from a content chunk using OpenAI.

    Args:
        chunk_text: Text content to generate questions from
        difficulty: Difficulty level (Easy, Medium, Hard) - default: Medium

    Returns:
        List of question dictionaries with format:
        {
            "question": "",
            "type": "",
            "options": [],
            "answer": "",
            "difficulty": ""
        }

    Raises:
        ValueError: If chunk_text is empty or OpenAI API key is missing
        Exception: If OpenAI API call fails
    """
    if not chunk_text or not chunk_text.strip():
        raise ValueError("Chunk text cannot be empty")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    prompt = f"""Generate exactly 3 quiz questions from the following text content. Return ONLY valid JSON array with no additional text.

Text: {chunk_text}

Generate:
1. One Multiple Choice Question (MCQ) with 4 options
2. One True/False Question
3. One Fill-in-the-Blank Question

For each question, follow this exact JSON format:
{{
    "question": "the question text",
    "type": "MCQ" or "TrueFalse" or "FillBlank",
    "options": ["option1", "option2", "option3", "option4"] (for MCQ only),
    "answer": "correct answer",
    "difficulty": "{difficulty}"
}}

Return as a JSON array ONLY:
[question1, question2, question3]"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a quiz generator. Generate educational questions from text. Return ONLY valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1500
        )

        response_text = response.choices[0].message.content.strip()

        # Parse JSON response
        questions = json.loads(response_text)

        # Validate and format questions
        formatted_questions = []
        for q in questions:
            formatted_q = {
                "question": q.get("question", ""),
                "type": q.get("type", ""),
                "options": q.get("options", []),
                "answer": q.get("answer", ""),
                "difficulty": q.get("difficulty", difficulty)
            }
            formatted_questions.append(formatted_q)

        return formatted_questions

    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse OpenAI response as JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating questions: {str(e)}")


def save_questions_to_db(chunk_id: int, questions: list[dict], db: Session) -> list[int]:
    """
    Save generated questions to the database.

    Args:
        chunk_id: ID of the ContentChunk
        questions: List of question dictionaries from generate_questions()
        db: SQLAlchemy session

    Returns:
        List of created Question IDs
    """
    question_ids = []

    try:
        for q in questions:
            question = Question(
                chunk_id=chunk_id,
                question=q["question"],
                type=q["type"],
                options=q.get("options"),
                answer=q["answer"],
                difficulty=q["difficulty"]
            )
            db.add(question)
            db.flush()
            question_ids.append(question.id)

        db.commit()
        return question_ids

    except Exception as e:
        db.rollback()
        raise Exception(f"Error saving questions to database: {str(e)}")

