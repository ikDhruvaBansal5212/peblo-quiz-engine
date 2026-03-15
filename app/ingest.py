"""
PDF Ingestion Module

This module handles reading, cleaning, and chunking text from PDF files.
"""
import re
from pathlib import Path
import pdfplumber


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

