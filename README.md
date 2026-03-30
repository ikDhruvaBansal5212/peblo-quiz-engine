# Peblo Quiz Engine (for checking backend working properly)

<div align="center">

**An AI-powered intelligent quiz generator for educational PDFs**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-brightgreen.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Automatically generate comprehensive quiz questions from PDF documents using intelligent text processing and AI.**

</div>

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Example Requests](#example-requests)
- [Database Schema](#database-schema)
- [Configuration](#configuration)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Project Overview

**Peblo Quiz Engine** is a production-ready FastAPI backend service designed to streamline the creation of educational quizzes from PDF documents. The system automates the entire workflow from PDF ingestion to question generation, enabling educators to quickly create assessments for students.

### Key Capabilities

- **📄 PDF Processing**: Automatically extracts and processes text from PDF documents
- **✂️ Intelligent Chunking**: Divides text into manageable chunks for better question generation
- **🤖 Quiz Generation**: Generates three types of questions (MCQ, True/False, Fill-in-the-Blank)
- **💾 Persistent Storage**: Stores all data in SQLite database for future retrieval
- **📊 Student Tracking**: Tracks student responses and performance metrics
- **🔄 Flexible Difficulty Levels**: Generate questions at Easy, Medium, or Hard difficulty

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────┐
│   Client App    │
│  (Web/Mobile)   │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌──────────────────────────────────┐
│      FastAPI Server (8000)       │
├──────────────────────────────────┤
│  Routes & Endpoints              │
│  ├─ PDF Upload Handler           │
│  ├─ Quiz Generation Controller   │
│  ├─ Student Answer Handler       │
│  └─ Data Retrieval Endpoints     │
└────────┬─────────────────────────┘
         │
    ┌────┴────┬─────────────┐
    ▼         ▼             ▼
┌────────┐ ┌──────────┐ ┌─────────┐
│ PDF    │ │  Quiz    │ │  Text   │
│Process │ │Generator │ │ Chunker │
└────────┘ └──────────┘ └─────────┘
    │         │
    └────┬────┘
         ▼
┌──────────────────────────────────┐
│    SQLite Database               │
├──────────────────────────────────┤
│  Tables:                         │
│  ├─ Source (PDFs)               │
│  ├─ ContentChunk (Text chunks)  │
│  ├─ Question (Generated Q&A)    │
│  └─ StudentAnswer (Responses)   │
└──────────────────────────────────┘
```

### Data Flow

```
PDF Upload → Extract Text → Clean & Chunk → Generate Questions → Store → API Response
```

### Module Structure

```
app/
├── main.py              # FastAPI application & route handlers
├── database.py          # SQLAlchemy configuration & session management
├── models.py            # Database models (ORM)
├── ingest.py            # PDF text extraction & chunking
├── quiz_generator.py    # Question generation logic
└── __init__.py          # Package initialization
```

---

## ✨ Features

✅ **Automated PDF Processing**
- Extract text from multi-page PDFs
- Automatic text cleaning and normalization
- Intelligent content chunking

✅ **AI-Powered Question Generation**
- Multiple choice questions with 4 options
- True/False questions
- Fill-in-the-blank questions
- Adjustable difficulty levels

✅ **RESTful API**
- Interactive Swagger UI documentation
- Complete OpenAPI specification
- JSON request/response format

✅ **Data Management**
- Store PDFs and metadata
- Maintain question databases
- Track student responses
- Query historical data

✅ **Mock Mode Support**
- Works without OpenAI API key
- Generates demo questions automatically
- Perfect for testing & development

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | FastAPI | 0.115.6 |
| **Server** | Uvicorn | 0.32.1 |
| **Database** | SQLite + SQLAlchemy | 2.0.36 |
| **PDF Processing** | pdfplumber | 0.11.4 |
| **AI Integration** | OpenAI | 1.58.1 |
| **Environment** | python-dotenv | 1.0.1 |
| **Data Validation** | Pydantic | 2.10.3 |
| **Language** | Python | 3.8+ |

---

## 📦 Setup Instructions

### Prerequisites

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **pip** - Comes with Python
- **Virtual Environment** (recommended) - `python -m venv`

### Installation Steps

1. **Clone and navigate to project**:
   ```bash
   cd e:\peblo-quiz-engine
   ```

2. **Create virtual environment** (recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   **Required packages:**
   - fastapi==0.115.6
   - uvicorn[standard]==0.32.1
   - sqlalchemy==2.0.36
   - pdfplumber==0.11.4
   - python-dotenv==1.0.1
   - pydantic==2.10.3
   - openai==1.58.1
   - python-multipart==0.0.6 (for file uploads)

4. **Configure environment** (optional):
   ```bash
   # Create .env file from example
   copy .env.example .env

   # Add your OpenAI API key (optional)
   # OPENAI_API_KEY=sk-your-key-here

   # Note: System works without API key in demo mode
   ```

5. **Initialize database**:
   ```bash
   # Database is automatically created on first run
   # Tables are created when the server starts
   ```

---

## 🚀 Running the Application

### Start Development Server

```bash
# Navigate to project directory
cd e:\peblo-quiz-engine

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Server will start on**: `http://localhost:8000`

### Access API Documentation

- **Swagger UI** (Interactive): http://localhost:8000/docs
- **ReDoc** (Alternative): http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Production Deployment

```bash
# With Gunicorn (production)
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

---

## 📡 API Endpoints

### Overview

| Category | Method | Endpoint | Purpose |
|----------|--------|----------|---------|
| **Health** | GET | `/health` | System status check |
| **Root** | GET | `/` | Welcome message |
| **Sources** | GET | `/sources` | List all PDFs |
| | GET | `/sources/{id}` | Get specific PDF |
| | POST | `/sources` | Create source |
| **Chunks** | GET | `/sources/{id}/chunks` | Get PDF chunks |
| | POST | `/chunks` | Store chunks |
| **Questions** | POST | `/chunks/{id}/generate-questions` | Generate questions |
| | GET | `/chunks/{id}/questions` | View questions |
| **Answers** | POST | `/answers` | Submit answer |
| | GET | `/students/{id}/answers` | View student answers |
| **PDF Upload** | POST | `/upload-pdf` | Upload & process PDF |

### Detailed Endpoints

#### 1. Health Check
```
GET /health
Response: { "status": "healthy" }
```

#### 2. Upload PDF File
```
POST /upload-pdf
Parameters:
  - file: UploadFile (required) - PDF file
  - topic: string (optional) - Content topic Default: "General"
  - source_id: integer (optional) - Link to existing source

Response:
{
  "filename": "document.pdf",
  "source_id": 1,
  "chunks_created": 5,
  "chunk_ids": [1, 2, 3, 4, 5]
}
```

#### 3. Generate Questions from Chunk
```
POST /chunks/{chunk_id}/generate-questions?difficulty=Medium
Path Parameters:
  - chunk_id: integer (required)

Query Parameters:
  - difficulty: string - "Easy" | "Medium" | "Hard" (default: "Medium")

Response: [
  {
    "id": 1,
    "chunk_id": 1,
    "question": "What is...?",
    "type": "MCQ",
    "options": ["A", "B", "C", "D"],
    "answer": "A",
    "difficulty": "Medium"
  },...
]
```

#### 4. Get Questions for Chunk
```
GET /chunks/{chunk_id}/questions
Path Parameters:
  - chunk_id: integer (required)

Response: [QuestionSchema, ...]
```

#### 5. Submit Student Answer
```
POST /answers
Query Parameters:
  - student_id: integer (required)
  - question_id: integer (required)
  - selected_answer: string (required)

Response:
{
  "id": 1,
  "student_id": 1,
  "question_id": 1,
  "selected_answer": "A",
  "is_correct": true
}
```

#### 6. Get Student Answers
```
GET /students/{student_id}/answers
Path Parameters:
  - student_id: integer (required)

Response: [StudentAnswerSchema, ...]
```

#### 7. Get All Sources (PDFs)
```
GET /sources
Response: [SourceSchema, ...]
```

#### 8. Get Chunks for Source
```
GET /sources/{source_id}/chunks
Path Parameters:
  - source_id: integer (required)

Response: [ContentChunkSchema, ...]
```

---

## 💡 Example Requests

### Complete Workflow Example

#### Step 1: Upload a PDF
```bash
curl -X POST "http://localhost:8000/upload-pdf" \
  -F "file=@math_guide.pdf" \
  -F "topic=Mathematics"

# Response:
{
  "filename": "math_guide.pdf",
  "source_id": 1,
  "chunks_created": 10,
  "chunk_ids": [1, 2, 3, ..., 10]
}
```

#### Step 2: Generate Questions from Chunk 1
```bash
curl -X POST "http://localhost:8000/chunks/1/generate-questions?difficulty=Medium"

# Response:
[
  {
    "id": 1,
    "chunk_id": 1,
    "question": "What is the Square root of 16?",
    "type": "MCQ",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Option A",
    "difficulty": "Medium"
  },
  {
    "id": 2,
    "chunk_id": 1,
    "question": "Is 25 the square of 5?",
    "type": "TrueFalse",
    "options": ["True", "False"],
    "answer": "True",
    "difficulty": "Medium"
  },
  {
    "id": 3,
    "chunk_id": 1,
    "question": "The area of a square with side 5 is _____.",
    "type": "FillBlank",
    "options": [],
    "answer": "25",
    "difficulty": "Medium"
  }
]
```

#### Step 3: View Questions for Chunk
```bash
curl -X GET "http://localhost:8000/chunks/1/questions"

# Response: Same as above
```

#### Step 4: Submit Student Answer
```bash
curl -X POST "http://localhost:8000/answers?student_id=1&question_id=1&selected_answer=Option%20A"

# Response:
{
  "id": 1,
  "student_id": 1,
  "question_id": 1,
  "selected_answer": "Option A",
  "is_correct": true
}
```

#### Step 5: Get Student Results
```bash
curl -X GET "http://localhost:8000/students/1/answers"

# Response:
[
  {
    "id": 1,
    "student_id": 1,
    "question_id": 1,
    "selected_answer": "Option A",
    "is_correct": true
  },
  {
    "id": 2,
    "student_id": 1,
    "question_id": 2,
    "selected_answer": "True",
    "is_correct": true
  },
  ...
]
```

### Using Python Requests Library

```python
import requests

BASE_URL = "http://localhost:8000"

# Upload PDF
with open("sample.pdf", "rb") as f:
    files = {"file": f}
    data = {"topic": "Science"}
    response = requests.post(f"{BASE_URL}/upload-pdf", files=files, data=data)
    result = response.json()
    chunk_id = result["chunk_ids"][0]

# Generate questions
response = requests.post(
    f"{BASE_URL}/chunks/{chunk_id}/generate-questions",
    params={"difficulty": "Easy"}
)
questions = response.json()
print(f"Generated {len(questions)} questions")

# Submit answer
response = requests.post(
    f"{BASE_URL}/answers",
    params={
        "student_id": 1,
        "question_id": questions[0]["id"],
        "selected_answer": "Option A"
    }
)
print(response.json())
```

---

## 🗄️ Database Schema

### Tables Overview

#### Source
Stores metadata about uploaded PDF documents.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Unique identifier |
| name | String | PDF filename |
| subject | String | Subject/topic area |
| grade | String | Grade level |
| created_at | DateTime | Upload timestamp |

#### ContentChunk
Stores text segments extracted from PDFs.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Unique identifier |
| source_id | Integer (FK) | Reference to Source |
| topic | String | Topic of content |
| text | Text | Extracted text content |
| created_at | DateTime | Creation timestamp |

#### Question
Stores generated quiz questions.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Unique identifier |
| chunk_id | Integer (FK) | Reference to ContentChunk |
| question | Text | Question text |
| type | String | MCQ, TrueFalse, FillBlank |
| options | JSON | Multiple choice options |
| answer | String | Correct answer |
| difficulty | String | Easy, Medium, Hard |
| created_at | DateTime | Creation timestamp |

#### StudentAnswer
Tracks student responses to questions.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Unique identifier |
| student_id | Integer | Student identifier |
| question_id | Integer (FK) | Reference to Question |
| selected_answer | String | Student's answer |
| is_correct | Boolean | Whether answer is correct |
| created_at | DateTime | Submission timestamp |

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI API Configuration (Optional)
# Get key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-api-key-here

# Database Configuration (Default: SQLite)
# DATABASE_URL=sqlite:///./quiz_engine.db

# FastAPI Configuration
# DEBUG=false
```

### Database Path

Default: `quiz_engine.db` in project root

To customize:
```python
# In app/database.py
DATABASE_URL = "sqlite:///./path/to/your/database.db"
```

### Question Generation Modes

**Mode 1: Mock Mode** (Active by default, no API key needed)
- Generates demo questions from PDF content
- Perfect for testing and development
- No external API calls required

**Mode 2: OpenAI Mode** (Requires valid API key with credits)
- Uses GPT-3.5-turbo for intelligent question generation
- More contextual and varied questions
- Requires active OpenAI subscription

---

## 🚀 Future Improvements

### Short Term (v1.1)
- [ ] Add authentication & user management
- [ ] Implement question difficulty classification
- [ ] Add batch PDF processing
- [ ] Create admin dashboard for statistics
- [ ] Export questions to PDF/CSV format

### Medium Term (v1.2)
- [ ] Support for multiple document types (DOCX, PPTX)
- [ ] Image/diagram handling in PDFs
- [ ] Advanced question type support (Matching, Ordering)
- [ ] Quiz template library
- [ ] Question quality scoring

### Long Term (v2.0)
- [ ] Machine learning for optimal difficulty prediction
- [ ] Multi-language support
- [ ] Integration with Learning Management Systems (LMS)
- [ ] Real-time quiz taking with WebSockets
- [ ] AI-powered analytics and insights
- [ ] Mobile app support
- [ ] Collaborative quiz creation

### Technical Debt
- [ ] Add comprehensive unit tests
- [ ] Implement API rate limiting
- [ ] Add request logging & monitoring
- [ ] Docker containerization
- [ ] CI/CD pipeline integration
- [ ] API versioning strategy
- [ ] Database migration tools

---

## 🐛 Troubleshooting

**Issue**: Port 8000 already in use
```bash
# Use different port
python -m uvicorn app.main:app --port 8001

# Or kill process on port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Issue**: PDF upload fails
- Ensure PDF is valid and not corrupted
- Check file permissions
- Verify PDF is not password-protected

**Issue**: Questions not generating
- Verify chunk has sufficient text content
- Check server logs for errors
- Ensure database is initialized

**Issue**: Module import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📚 API Documentation

Interactive API documentation is automatically generated by FastAPI:

- **Swagger UI**: http://localhost:8000/docs
- **Alternative (ReDoc)**: http://localhost:8000/redoc

These provide:
- All endpoint definitions
- Request/response schemas
- Try-it-out functionality
- Authentication setup (when enabled)

---

## 🤝 Contributing

### Development Setup

```bash
git clone <repository>
cd peblo-quiz-engine
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

---

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

**MIT License**: Free to use, modify, and distribute for educational and commercial purposes.

---

## 📞 Support & Contact

For questions, issues, or feature requests:

- **Create an Issue**: [GitHub Issues](https://github.com)
- **Email**: support@peblo-quiz-engine.com
- **Documentation**: Full API docs available at `/docs` endpoint

---

## 🔗 Quick Links

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **OpenAI API**: https://platform.openai.com/docs/
- **Python**: https://www.python.org/

---

<div align="center">

**Made with ❤️ for educators**

Last Updated: March 2026 | Version: 0.1.0

</div>
