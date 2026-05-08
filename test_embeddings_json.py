import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

with open('data/processed/data.json', 'r') as f:
    data = json.load(f)

for item in data[:5]:
    filename = item['filename']
    page_number = item['page_number']
    text = item['text']
    
    embedding = model.encode(text)
    
    print(f"{filename} | page {page_number} | embedding length: {len(embedding)}")
