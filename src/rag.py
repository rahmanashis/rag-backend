import os
import hashlib
import psycopg2
from dotenv import load_dotenv
from prompt_rules import SYSTEM_RULES

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Lazy load model to avoid import errors at startup
_model = None
_model_failed = False


def _fallback_embedding(text: str, dim: int = 384):
    # Deterministic fallback vector for environments where sentence-transformers is unavailable.
    values = []
    for i in range(dim):
        digest = hashlib.sha256(f"{text}:{i}".encode("utf-8")).digest()
        num = int.from_bytes(digest[:4], "big", signed=False)
        values.append((num / 4294967295.0) * 2.0 - 1.0)
    return values

def get_model():
    global _model, _model_failed
    if _model is None and not _model_failed:
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            _model_failed = True
    return _model


def get_query_embedding(user_query: str):
    model = get_model()
    if model is not None:
        return model.encode(user_query).tolist()
    return _fallback_embedding(user_query)


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def retrieve_chunks(user_query, top_k=5):
    query_embedding = get_query_embedding(user_query)

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT doc_id, chunk_id, source_name, page_number, text
            FROM rag.document_chunks
            ORDER BY embedding <-> %s::vector
            LIMIT %s;
        """, (str(query_embedding), top_k))

        rows = cur.fetchall()
    except Exception:
        # Return empty results when DB or embedding-backed retrieval is unavailable.
        rows = []
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    results = []
    for row in rows:
        results.append({
            "doc_id": row[0],
            "chunk_id": row[1],
            "source_name": row[2],
            "page_number": row[3],
            "text": row[4]
        })

    return results


def build_context(chunks):
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        context_parts.append(
            f"[Chunk {i}]\n"
            f"Source: {chunk['source_name']}\n"
            f"Page: {chunk['page_number']}\n"
            f"Text: {chunk['text']}\n"
        )
    return "\n".join(context_parts)


def build_rag_prompt(user_query, top_k=5):
    chunks = retrieve_chunks(user_query, top_k=top_k)
    context = build_context(chunks)

    prompt = f"""{SYSTEM_RULES}

Retrieved Context:
{context}

User Question:
{user_query}
"""
    return prompt, chunks