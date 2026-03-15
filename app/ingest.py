"""
PDF Ingestion Module

This module handles reading and extracting text from PDF files.
"""
import os
from pathlib import Path


class PDFIngester:
    """Handles PDF file ingestion and text extraction"""

    def __init__(self, pdf_directory: str = "data/pdfs"):
        self.pdf_directory = Path(pdf_directory)
        self.pdf_directory.mkdir(parents=True, exist_ok=True)

    def extract_text_from_pdf(self, file_path: str) -> str:
        """
        Extract text content from a PDF file.

        Args:
            file_path: Path to the PDF file

        Returns:
            Extracted text content
        """
        try:
            # Import PyPDF2 here to handle optional dependency
            from PyPDF2 import PdfReader

            with open(file_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except ImportError:
            raise ImportError("PyPDF2 is required for PDF processing. Install it using: pip install PyPDF2")
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    def get_pdf_files(self) -> list[str]:
        """Get list of all PDF files in the PDF directory"""
        return [f.name for f in self.pdf_directory.glob("*.pdf")]

    def save_pdf(self, file_path: str, content: bytes) -> str:
        """
        Save uploaded PDF file to storage directory.

        Args:
            file_path: Name of the file
            content: Binary content of the PDF

        Returns:
            Full path to saved file
        """
        full_path = self.pdf_directory / file_path
        with open(full_path, 'wb') as f:
            f.write(content)
        return str(full_path)
