from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

text = "Artificial Intelligence in Skin Cancer Diagnosis is revolutionizing dermatology through deep learning and computer vision techniques."

embedding = model.encode(text)

print(f"Embedding vector length: {len(embedding)}")
print(f"First 5 values: {embedding[:5]}")
