#!/usr/bin/env python3
"""
Application Settings
Global configuration and constants
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Project directories
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
INPUT_PDF_DIR = DATA_DIR / "input_pdfs"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
LOGS_DIR = PROJECT_ROOT / "logs"

# Ensure directories exist
INPUT_PDF_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# File paths
INPUT_PDF_PATH = os.getenv('INPUT_PDF_PATH', str(INPUT_PDF_DIR))
OUTPUT_JSON_PATH = os.getenv('OUTPUT_JSON_PATH', str(PROCESSED_DATA_DIR / "data.json"))

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Vector store configuration
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50

# Search configuration
DEFAULT_TOP_K = 5

# Application version
APP_VERSION = "1.0.0"
