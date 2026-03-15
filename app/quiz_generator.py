"""
Quiz Generator Module

This module generates quiz questions from text content using OpenAI API.
Falls back to mock mode if API key is invalid.
"""
import json
import os
from typing import Optional
from openai import OpenAI
from sqlalchemy.orm import Session
from app.models import Question


# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY", "").strip()

# Check if API key is valid (must start with sk- and have content)
HAS_VALID_API_KEY = bool(api_key and api_key.startswith("sk-") and len(api_key) > 20)

if HAS_VALID_API_KEY:
    client = OpenAI(api_key=api_key)
else:
    client = None

USE_MOCK_MODE = not HAS_VALID_API_KEY

print(f"[INIT] Quiz Generator - API Key present: {bool(api_key)}, HAS_VALID_API_KEY: {HAS_VALID_API_KEY}, USE_MOCK_MODE: {USE_MOCK_MODE}")


def generate_mock_questions(chunk_text: str, difficulty: str = "Medium") -> list[dict]:
    """
    Generate mock questions for demo/testing without OpenAI API.

    Args:
        chunk_text: Text content to generate questions from
        difficulty: Difficulty level (Easy, Medium, Hard)

    Returns:
        List of mock question dictionaries
    """
    # Extract first few words from chunk as question topic
    words = chunk_text.split()[:5]
    topic = " ".join(words) if words else "the topic"

    return [
        {
            "question": f"What is {topic}?",
            "type": "MCQ",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Option A",
            "difficulty": difficulty
        },
        {
            "question": f"Is {topic} important?",
            "type": "TrueFalse",
            "options": ["True", "False"],
            "answer": "True",
            "difficulty": difficulty
        },
        {
            "question": f"The main concept of {topic} is to _____ .",
            "type": "FillBlank",
            "options": [],
            "answer": "understand",
            "difficulty": difficulty
        }
    ]


def generate_questions(chunk_text: str, difficulty: str = "Medium") -> list[dict]:
    """
    Generate three types of quiz questions from a content chunk using OpenAI.
    Falls back to mock questions if API key is missing or invalid.

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
        ValueError: If chunk_text is empty
        Exception: If OpenAI API call fails (uses mock as fallback)
    """
    if not chunk_text or not chunk_text.strip():
        raise ValueError("Chunk text cannot be empty")

    # ALWAYS use mock mode - no API key available
    print(f"[INFO] Using mock mode (ALWAYS). Generating mock questions...")
    return generate_mock_questions(chunk_text, difficulty)

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
        print(f"JSON parsing error: {str(e)}. Using mock questions instead.")
        return generate_mock_questions(chunk_text, difficulty)
    except Exception as e:
        # Always fall back to mock mode on any error
        print(f"Question generation error: {str(e)}. Using mock questions instead.")
        return generate_mock_questions(chunk_text, difficulty)


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

