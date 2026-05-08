CREATE EXTENSION IF NOT EXISTS vector;

CREATE SCHEMA IF NOT EXISTS rag;

CREATE TABLE IF NOT EXISTS rag.document_chunks (
    id BIGSERIAL PRIMARY KEY,
    doc_id TEXT NOT NULL,
    chunk_id TEXT NOT NULL UNIQUE,
    text TEXT NOT NULL,
    source_name TEXT,
    page_number INT,
    embedding VECTOR(384) NOT NULL
);
