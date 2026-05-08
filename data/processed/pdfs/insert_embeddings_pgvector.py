import json
import psycopg2
from sentence_transformers import SentenceTransformer
from pgvector.psycopg2 import register_vector

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="ragdb",
    user="postgres",
    password="your_password"
)
cursor = conn.cursor()

# Register pgvector
register_vector(conn)

# Load JSON data
with open('data/processed/data.json', 'r') as f:
    data = json.load(f)

# Insert embeddings
for i, item in enumerate(data, 1):
    filename = item['filename']
    page_number = item['page_number']
    text = item['text']
    
    # Generate embedding
    embedding = model.encode(text)
    
    # Insert into database
    cursor.execute(
        "INSERT INTO documents (filename, page_number, content, embedding) VALUES (%s, %s, %s, %s)",
        (filename, page_number, text, embedding)
    )
    
    # Print progress every 100 rows
    if i % 100 == 0:
        print(f"Inserted {i} documents...")

# Commit and close
conn.commit()
cursor.close()
conn.close()

print(f"Completed! Total documents inserted: {len(data)}")
