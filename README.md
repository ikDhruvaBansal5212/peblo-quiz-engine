# Peblo Quiz Engine

An AI-powered backend service for generating quizzes from PDF documents.

## Project Overview

Peblo Quiz Engine is a FastAPI-based backend service that:
- Ingests PDF documents
- Extracts text content
- Generates quiz questions automatically
- Stores quiz data in a SQLite database
- Provides REST API endpoints for quiz management

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.8+
- **Database**: SQLite with SQLAlchemy ORM
- **API Documentation**: Swagger UI (built-in with FastAPI)

## Project Structure

```
peblo-quiz-engine/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # SQLAlchemy database configuration
│   ├── models.py            # Database models (Quiz, Question, Option)
│   ├── ingest.py            # PDF ingestion and text extraction
│   ├── quiz_generator.py    # Quiz generation logic
│
├── data/
│   └── pdfs/                # Storage for uploaded PDF files
│
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── .gitignore             # Git ignore rules
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**:
   ```bash
   cd peblo-quiz-engine
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Start the development server:
```bash
python -m uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`

### Access the API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /health` - Check if the service is running

### Quizzes
- `GET /quizzes` - List all quizzes
- `POST /quizzes` - Create a new quiz
- `GET /quizzes/{quiz_id}` - Get a specific quiz

### Questions
- `POST /quizzes/{quiz_id}/questions` - Add a question to a quiz

### PDF Upload
- `POST /upload-pdf` - Upload a PDF file for processing

## Database Models

### Quiz
- `id`: Primary key
- `title`: Quiz title
- `description`: Quiz description
- `source_pdf`: Source PDF file name
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `questions`: Relationship to Question model

### Question
- `id`: Primary key
- `quiz_id`: Foreign key to Quiz
- `question_text`: The question content
- `question_type`: Type of question (multiple_choice, true_false, short_answer)
- `created_at`: Creation timestamp
- `options`: Relationship to QuestionOption model

### QuestionOption
- `id`: Primary key
- `question_id`: Foreign key to Question
- `option_text`: Option content
- `is_correct`: Boolean flag for correct answer
- `order`: Display order of the option

## Future Enhancements

- [ ] Integrate with LLM API for AI-powered question generation
- [ ] Add authentication and authorization
- [ ] Implement quiz taking and grading functionality
- [ ] Add batch PDF processing
- [ ] Create admin dashboard
- [ ] Add export functionality (PDF, CSV)
- [ ] Support for different question types

## License

MIT License - feel free to use this project for educational purposes.

## Support

For issues or questions, please create an issue in the project repository.
