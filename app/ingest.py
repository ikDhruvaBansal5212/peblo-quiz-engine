"""
PDF Ingestion Module

This module handles reading, cleaning, chunking text from PDF files, and storing chunks in the database.
"""
import re
from pathlib import Path
import pdfplumber
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import ContentChunk


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text content from a PDF file using pdfplumber.

    Args:
        file_path: Path to the PDF file

    Returns:
        Extracted text content from all pages

    Raises:
        FileNotFoundError: If the PDF file does not exist
        Exception: If PDF extraction fails
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def clean_text(text: str) -> str:
    """
    Clean extracted text by removing extra whitespace, special characters, and normalizing.

    Args:
        text: Raw text to clean

    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\—\-\:\;]', '', text)

    # Remove multiple spaces
    text = re.sub(r' +', ' ', text)

    # Strip leading and trailing whitespace
    text = text.strip()

    return text


def chunk_text(text: str, chunk_size: int = 300) -> list[str]:
    """
    Split text into chunks of approximately the specified word count.

    Args:
        text: Text to split
        chunk_size: Target word count per chunk (default: 300)

    Returns:
        List of text chunks
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_word_count = 0

    for word in words:
        current_chunk.append(word)
        current_word_count += 1

        # When chunk reaches target size, save it and start a new one
        if current_word_count >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_word_count = 0

    # Add any remaining words as the final chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def ingest_pdf(file_path: str) -> list[str]:
    """
    Complete pipeline: extract, clean, and chunk a PDF file.

    Args:
        file_path: Path to the PDF file

    Returns:
        List of text chunks ready for processing
    """
    raw_text = extract_text_from_pdf(file_path)
    cleaned_text = clean_text(raw_text)
    chunks = chunk_text(cleaned_text)
    return chunks


def store_chunks(source_id: int, chunks: list[str], topic: str = "General", db: Session = None) -> list[int]:
    """
    Store text chunks in the database as ContentChunk records.

    Args:
        source_id: ID of the Source record
        chunks: List of text chunks to store
        topic: Topic name for the chunks (default: "General")
        db: SQLAlchemy session (if None, creates a new one)

    Returns:
        List of created ContentChunk IDs

    Raises:
        ValueError: If source_id is invalid or chunks list is empty
        Exception: If database operation fails
    """
    if not chunks:
        raise ValueError("Chunks list cannot be empty")

    if source_id <= 0:
        raise ValueError("Invalid source_id: must be a positive integer")

    # Use provided session or create a new one
    session = db or SessionLocal()
    close_session = db is None

    try:
        chunk_ids = []

        for chunk_text in chunks:
            if not chunk_text.strip():
                continue

            content_chunk = ContentChunk(
                source_id=source_id,
                topic=topic,
                text=chunk_text.strip()
            )
            session.add(content_chunk)
            session.flush()  # Flush to get the ID
            chunk_ids.append(content_chunk.id)

        session.commit()
        return chunk_ids

    except Exception as e:
        session.rollback()
        raise Exception(f"Error storing chunks in database: {str(e)}")
    finally:
        if close_session:
            session.close()

