# Setup Guide - Peblo Quiz Engine

## Prerequisites

- Python 3.9+
- pip (Python package manager)

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Then edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

### 3. Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in to your OpenAI account
3. Create a new API key
4. Copy the key and paste it in `.env` file

### 4. Initialize Database

The database will be automatically created on first run, but you can manually initialize it:

```python
from app.database import init_db
init_db()
```

## Running the Application

### Start the FastAPI Server

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## Usage Example

```python
from app.ingest import ingest_pdf, store_chunks
from app.quiz_generator import generate_questions, save_questions_to_db
from app.database import SessionLocal
from app.models import Source

# 1. Create a source
db = SessionLocal()
source = Source(name="Biology 101", subject="Biology", grade="10")
db.add(source)
db.commit()
source_id = source.id

# 2. Ingest PDF and store chunks
chunks = ingest_pdf("path/to/document.pdf")
chunk_ids = store_chunks(source_id=source_id, chunks=chunks)

# 3. Generate questions from each chunk
for chunk_id in chunk_ids:
    questions = generate_questions(chunks[chunk_ids.index(chunk_id)])
    save_questions_to_db(chunk_id, questions, db)

db.close()
```

## Project Structure

```
peblo-quiz-engine/
├── app/
│   ├── database.py       # SQLAlchemy configuration
│   ├── models.py         # SQLAlchemy models
│   ├── ingest.py         # PDF processing
│   ├── quiz_generator.py # OpenAI question generation
│   └── main.py           # FastAPI routes
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
├── .env                  # Environment variables (gitignored)
└── README.md
```

## Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for question generation | Yes | `sk-...` |
| `DATABASE_URL` | Database connection string | No | `sqlite:///./quiz_engine.db` |

## Troubleshooting

### OpenAI API Key Error
- Ensure `.env` file exists in project root
- Check that `OPENAI_API_KEY` is correctly set
- Verify the API key is valid at https://platform.openai.com/api-keys

### PDF Extraction Fails
- Ensure the PDF file is valid and readable
- Check that pdfplumber is installed: `pip install pdfplumber`

### Database Errors
- Delete `quiz_engine.db` and restart the app to reset the database
- Ensure the database file is in the correct location

## License

MIT
