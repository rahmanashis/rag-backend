import json
from pathlib import Path

input_file = Path("data/processed/chunk.json")
output_file = Path("data/processed/chunk_with_ids.json")

with open(input_file, "r", encoding="utf-8") as f:
    chunks = json.load(f)

doc_map = {}
doc_counter = 1
chunk_counter_per_doc = {}

reordered_chunks = []

for item in chunks:
    filename = item.get("filename", "unknown_file")

    if filename not in doc_map:
        doc_map[filename] = f"doc_{doc_counter:04d}"
        chunk_counter_per_doc[filename] = 1
        doc_counter += 1

    doc_id = doc_map[filename]
    chunk_num = chunk_counter_per_doc[filename]
    chunk_id = f"{doc_id}_chunk_{chunk_num:04d}"

    # Create new dict with doc_id and chunk_id first, then other fields
    reordered_item = {
        "doc_id": doc_id,
        "chunk_id": chunk_id,
        **{k: v for k, v in item.items() if k not in ["doc_id", "chunk_id"]}
    }
    reordered_chunks.append(reordered_item)
    chunk_counter_per_doc[filename] += 1

chunks = reordered_chunks

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

print(f"Done. New file saved as: {output_file}")
print(f"Total chunks processed: {len(chunks)}")