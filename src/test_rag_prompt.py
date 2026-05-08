from rag import build_rag_prompt

query = "What deep learning models are used for skin lesion classification?"
prompt, chunks = build_rag_prompt(query, top_k=3)

print(prompt[:3000])
print("\nChunks returned:", len(chunks))