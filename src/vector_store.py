#!/usr/bin/env python3
"""
Vector Store Module
Handles vector embeddings and similarity search
"""

import logging
from typing import List, Dict, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStore:
    """Vector embedding and similarity search"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the vector store with a sentence transformer model.
        
        Args:
            model_name (str): Name of the sentence transformer model
        """
        logger.info(f"Loading model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embeddings = []
        self.documents = []
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a text.
        
        Args:
            text (str): Text to embed
            
        Returns:
            np.ndarray: Embedding vector
        """
        return self.model.encode(text, convert_to_numpy=True)
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts (list): List of texts to embed
            
        Returns:
            np.ndarray: Array of embedding vectors
        """
        logger.info(f"Embedding {len(texts)} texts...")
        return self.model.encode(texts, convert_to_numpy=True)
    
    def add_documents(self, documents: List[Dict]) -> None:
        """
        Add documents and their embeddings to the store.
        
        Args:
            documents (list): List of document dictionaries with 'text' key
        """
        texts = [doc.get('text', '') for doc in documents]
        self.embeddings = self.embed_texts(texts)
        self.documents = documents
        logger.info(f"Added {len(documents)} documents to vector store")
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """
        Search for similar documents.
        
        Args:
            query (str): Search query
            top_k (int): Number of top results to return
            
        Returns:
            list: List of (document, similarity_score) tuples
        """
        if not self.documents:
            logger.warning("Vector store is empty")
            return []
        
        query_embedding = self.embed_text(query)
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = [
            (self.documents[idx], float(similarities[idx]))
            for idx in top_indices
            if similarities[idx] > 0
        ]
        
        return results
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embeddings.
        
        Returns:
            int: Embedding dimension
        """
        return self.model.get_sentence_embedding_dimension()
