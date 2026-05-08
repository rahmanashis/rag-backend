#!/usr/bin/env python3
"""
Text Processing Module
Handles text cleaning, normalization, and chunking
"""

import re
import logging
from typing import List, Dict


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextProcessor:
    """Text processing and cleaning utilities"""
    
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        """
        Initialize the text processor.
        
        Args:
            chunk_size (int): Size of text chunks
            overlap (int): Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean text by removing extra whitespace and normalizing content.
        
        Args:
            text (str): Raw text to clean
            
        Returns:
            str: Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-]', '', text)
        # Strip leading and trailing whitespace
        text = text.strip()
        return text
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text (str): Text to chunk
            
        Returns:
            list: List of text chunks
        """
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk = ' '.join(words[i:i + self.chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks
    
    def process_documents(self, documents: List[Dict]) -> List[Dict]:
        """
        Process a list of documents.
        
        Args:
            documents (list): List of document dictionaries
            
        Returns:
            list: Processed documents with cleaned text
        """
        processed = []
        
        for doc in documents:
            cleaned_text = self.clean_text(doc.get('text', ''))
            chunks = self.chunk_text(cleaned_text)
            
            for chunk_idx, chunk in enumerate(chunks):
                processed.append({
                    'filename': doc.get('filename'),
                    'page_number': doc.get('page_number'),
                    'chunk_number': chunk_idx,
                    'text': chunk
                })
        
        logger.info(f"Processed {len(documents)} documents into {len(processed)} chunks")
        return processed
