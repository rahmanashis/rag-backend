import psycopg2
from pgvector.psycopg2 import register_vector
import json

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="104602"
)
cursor = conn.cursor()
register_vector(conn)

# Query: Get first 5 records with embeddings
cursor.execute("""
    SELECT id, filename, page_number, content, embedding 
    FROM documents 
    LIMIT 5
""")

records = cursor.fetchall()

print("=" * 80)
print("VECTOR EMBEDDINGS IN DATABASE")
print("=" * 80)

for i, record in enumerate(records, 1):
    id_, filename, page_num, content, embedding = record
    
    print(f"\n[Record {i}]")
    print(f"  ID: {id_}")
    print(f"  Filename: {filename}")
    print(f"  Page: {page_num}")
    print(f"  Content: {content[:100]}...")
    print(f"  Embedding dimension: {len(embedding)}")
    print(f"  First 5 values: {embedding[:5]}")
    print(f"  Last 5 values: {embedding[-5:]}")

cursor.close()
conn.close()

print("\n" + "=" * 80)
print("✓ All embeddings are stored in the 'documents' table in PostgreSQL")
print("=" * 80)
