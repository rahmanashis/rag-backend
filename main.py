#!/usr/bin/env python3
"""
RAG System - Main Application Entry Point
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config.settings import LOG_LEVEL, LOGS_DIR
from src.extract_pdfs import main as extract_main
from src.text_processor import TextProcessor
import json


# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / 'rag_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    """Main application function"""
    logger.info("=" * 50)
    logger.info("RAG System - Starting Application")
    logger.info("=" * 50)
    
    try:
        # Step 1: Extract PDFs
        logger.info("\n[Step 1] Extracting PDFs...")
        extract_main()
        
        # Step 2: Process text
        logger.info("\n[Step 2] Processing text...")
        processor = TextProcessor(chunk_size=512, overlap=50)
        
        # Load extracted data
        from config.settings import OUTPUT_JSON_PATH
        with open(OUTPUT_JSON_PATH, 'r', encoding='utf-8') as f:
            documents = json.load(f)
        
        logger.info(f"Loaded {len(documents)} documents")
        
        # Process documents
        processed_docs = processor.process_documents(documents)
        logger.info(f"Processed into {len(processed_docs)} chunks")
        
        logger.info("\n" + "=" * 50)
        logger.info("RAG System - Completed Successfully")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"Error in main application: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
