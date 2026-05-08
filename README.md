# RAG System - Retrieval Augmented Generation

A comprehensive Retrieval Augmented Generation (RAG) system for extracting, processing, and searching through PDF documents using vector embeddings and PostgreSQL.

## Project Structure

```
RAG-System/
├── src/
│   ├── extract_pdfs.py          # PDF text extraction module
│   ├── text_processor.py        # Text cleaning and processing
│   ├── vector_store.py          # Vector embedding and storage
│   └── __init__.py
├── config/
│   ├── database_config.py       # Database configuration
│   └── settings.py              # Application settings
├── data/
│   ├── input_pdfs/              # Place your PDF files here
│   └── processed/               # Processed JSON output
├── logs/                         # Application logs
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── main.py                      # Main application entry point
└── README.md                    # This file
```

## Installation

1. **Clone or navigate to the project:**
   ```bash
   cd RAG-System
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate      # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Update `.env` with your settings:**
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=rag_database
   DB_USER=postgres
   DB_PASSWORD=your_password
   OPENAI_API_KEY=your_api_key
   ```

## Usage

### Extract PDFs

Place your PDF files in `data/input_pdfs/` folder, then run:

```bash
python src/extract_pdfs.py
```

This will:
- Extract text from all PDFs
- Clean and normalize the text
- Save results to `data/processed/data.json`

### Run the Main Application

```bash
python main.py
```

## Features

- **PDF Text Extraction** - Uses PyMuPDF for fast and reliable extraction
- **Text Processing** - Removes noise and normalizes content
- **Vector Embeddings** - Converts text to embeddings using SentenceTransformers
- **Database Storage** - Stores embeddings in PostgreSQL
- **Similarity Search** - Find similar documents based on queries

## Dependencies

- **PyMuPDF** - PDF text extraction
- **Pandas** - Data manipulation
- **SentenceTransformers** - Vector embeddings
- **psycopg2** - PostgreSQL connection
- **LangChain** - LLM framework
- **OpenAI** - LLM integration

## Database Setup (PostgreSQL)

```sql
CREATE DATABASE rag_database;

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255),
    page_number INT,
    content TEXT,
    embedding VECTOR(384),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX ON documents USING IVFFLAT (embedding vector_cosine_ops);
```

## Troubleshooting

- **PyMuPDF not installed:** `pip install PyMuPDF`
- **PostgreSQL not running:** Start your PostgreSQL service
- **Connection errors:** Check `.env` configuration and database credentials

## License

MIT License

## Author

RAG System Development Team
