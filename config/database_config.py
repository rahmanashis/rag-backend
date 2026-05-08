#!/usr/bin/env python3
"""
Database Configuration
PostgreSQL connection settings and utilities
"""

import os
import logging
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class DatabaseConfig:
    """Database configuration and connection management"""
    
    def __init__(self):
        """Initialize database configuration from environment variables"""
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = int(os.getenv('DB_PORT', 5432))
        self.database = os.getenv('DB_NAME', 'rag_database')
        self.user = os.getenv('DB_USER', 'postgres')
        self.password = os.getenv('DB_PASSWORD', '')
    
    def get_connection(self):
        """
        Get a database connection.
        
        Returns:
            psycopg2.connection: Database connection object
        """
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            logger.info("Successfully connected to PostgreSQL database")
            return conn
        except psycopg2.Error as e:
            logger.error(f"Unable to connect to the database: {e}")
            raise
    
    def create_tables(self, conn):
        """
        Create necessary database tables.
        
        Args:
            conn: Database connection object
        """
        try:
            cursor = conn.cursor()
            
            # Create documents table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    filename VARCHAR(255),
                    page_number INT,
                    chunk_number INT,
                    content TEXT,
                    embedding BYTEA,
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """)
            
            # Create index
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_documents_filename 
                ON documents(filename);
            """)
            
            conn.commit()
            logger.info("Database tables created successfully")
            
        except psycopg2.Error as e:
            logger.error(f"Error creating tables: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()
    
    def insert_document(self, conn, document: dict, embedding: bytes) -> int:
        """
        Insert a document with its embedding.
        
        Args:
            conn: Database connection object
            document (dict): Document data
            embedding (bytes): Document embedding
            
        Returns:
            int: Document ID
        """
        try:
            cursor = conn.cursor()
            
            cursor.execute(
                sql.SQL("""
                    INSERT INTO documents 
                    (filename, page_number, chunk_number, content, embedding)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id;
                """),
                (
                    document.get('filename'),
                    document.get('page_number'),
                    document.get('chunk_number', 0),
                    document.get('text'),
                    embedding
                )
            )
            
            doc_id = cursor.fetchone()[0]
            conn.commit()
            return doc_id
            
        except psycopg2.Error as e:
            logger.error(f"Error inserting document: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()
