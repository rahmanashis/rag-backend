import os
import psycopg2
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

model = SentenceTransformer("all-MiniLM-L6-v2")

query = "What deep learning models are used for skin lesion classification?"
query_embedding = model.encode(query).tolist()

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cur = conn.cursor()

cur.execute("""
    SELECT doc_id, chunk_id, source_name, page_number, text
    FROM rag.document_chunks
    ORDER BY embedding <-> %s::vector
    LIMIT 5;
""", (str(query_embedding),))

rows = cur.fetchall()

for i, row in enumerate(rows, 1):
    print(f"\nResult {i}")
    print("doc_id:", row[0])
    print("chunk_id:", row[1])
    print("source_name:", row[2])
    print("page_number:", row[3])
    print("text:", row[4][:500])

cur.close()
conn.close()