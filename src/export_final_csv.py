import json
import csv
from pathlib import Path

# Read chunk data with doc_id and chunk_id
chunk_file = Path("data/processed/chunk.json")
embeddings_file = Path("embeddings_export.csv")
output_file = Path("data/final_embeddings_export.csv")

# Load chunks
with open(chunk_file, "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Load embeddings from CSV
embeddings_list = []
with open(embeddings_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        embeddings_list.append(row)

# Create a mapping of index to embedding
# Assuming the embeddings are in the same order as chunks
embeddings_dict = {idx: emb_row for idx, emb_row in enumerate(embeddings_list)}

# Prepare final data
final_rows = []
for idx, chunk in enumerate(chunks):
    doc_id = chunk.get("doc_id", "")
    chunk_id = chunk.get("chunk_id", "")
    text = chunk.get("text", "")
    filename = chunk.get("filename", "")
    page_number = chunk.get("page_number", "")
    
    # Get embedding from the embeddings file (assuming same order)
    if idx in embeddings_dict:
        # The embedding is typically the last column or named 'embedding'
        emb_row = embeddings_dict[idx]
        # Get the last value (which should be the embedding vector)
        embedding = list(emb_row.values())[-1]
    else:
        embedding = ""
    
    row = {
        "doc_id": doc_id,
        "chunk_id": chunk_id,
        "text": text,
        "source_name": filename,
        "page_number": page_number,
        "embedding": embedding
    }
    final_rows.append(row)

# Write to CSV
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f, 
        fieldnames=["doc_id", "chunk_id", "text", "source_name", "page_number", "embedding"]
    )
    writer.writeheader()
    writer.writerows(final_rows)

print(f"Done. Final CSV saved as: {output_file}")
print(f"Total rows exported: {len(final_rows)}")
