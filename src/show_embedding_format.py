import psycopg2
from pgvector.psycopg2 import register_vector
import numpy as np

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="104602"
)
cursor = conn.cursor()
register_vector(conn)

# Get one embedding
cursor.execute("SELECT id, filename, content, embedding FROM documents LIMIT 1")
record = cursor.fetchone()

id_, filename, content, embedding = record

print("=" * 100)
print("WHAT DOES A VECTOR EMBEDDING LOOK LIKE?")
print("=" * 100)

print(f"\n📄 Original Text:")
print(f"   Filename: {filename}")
print(f"   Content: {content[:150]}...")

print(f"\n🔢 After Embedding with all-MiniLM-L6-v2:")
print(f"   Type: {type(embedding)}")
print(f"   Total numbers: {len(embedding)}")
print(f"   Each number is: Float (decimal)")

print(f"\n📊 Full Embedding Vector (384 decimal numbers):")
print(f"   {embedding}")

print(f"\n🔍 First 10 values:")
for i, val in enumerate(embedding[:10]):
    print(f"   [{i}] = {val}")

print(f"\n📈 Statistics:")
print(f"   Min value: {min(embedding):.6f}")
print(f"   Max value: {max(embedding):.6f}")
print(f"   Mean value: {np.mean(embedding):.6f}")
print(f"   Std deviation: {np.std(embedding):.6f}")

print(f"\n🎯 Size in Memory:")
print(f"   One embedding: ~1.5 KB")
print(f"   1,072 embeddings: ~1.6 MB")

print("\n" + "=" * 100)
print("VISUALIZED:")
print("=" * 100)
print("Text: 'A comprehensive analysis of deep learning and transfer learning...'")
print("  ↓ (goes through model)")
print("Vector: [-0.033, -0.019, 0.063, 0.030, 0.084, ... 384 more numbers ...0.113, -0.011, -0.007, -0.001, -0.033]")
print("\n✓ This vector represents the MEANING of the text in mathematical space!")

cursor.close()
conn.close()
