import csv
import os
import psycopg2
from psycopg2 import errors
from pgvector.psycopg2 import register_vector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database connection parameters from .env
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'ragdb')
db_user = os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD', 'your_password')

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )
    cursor = conn.cursor()
    print(f"Connected to {db_name} at {db_host}:{db_port}")
except psycopg2.Error as e:
    print(f"Error connecting to database: {e}")
    exit(1)

# Register pgvector
register_vector(conn)

# Read and parse embeddings from CSV
csv_file = 'data/final_embeddings_export.csv'
total_processed = 0
total_inserted = 0
total_failed = 0

try:
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row_num, row in enumerate(reader, 1):
            total_processed += 1
            
            try:
                doc_id = row.get('doc_id', '')
                chunk_id = row.get('chunk_id', '')
                text = row.get('text', '')
                source_name = row.get('source_name', '')
                page_number_str = row.get('page_number', '')
                embedding_str = row.get('embedding', '')
                
                # Convert page_number to int, handle empty/invalid values
                try:
                    page_number = int(page_number_str) if page_number_str else None
                except ValueError:
                    page_number = None
                
                # Parse embedding string to list
                try:
                    embedding = eval(embedding_str)  # Convert string representation to list
                except:
                    print(f"Row {row_num}: Failed to parse embedding for chunk_id {chunk_id}")
                    total_failed += 1
                    continue
                
                # Insert into database
                cursor.execute(
                    """INSERT INTO rag.document_chunks (doc_id, chunk_id, text, source_name, page_number, embedding)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (doc_id, chunk_id, text, source_name, page_number, embedding)
                )
                total_inserted += 1
                
                # Print progress every 100 rows
                if total_inserted % 100 == 0:
                    print(f"Inserted {total_inserted} rows...")
                    
            except errors.UniqueViolation:
                # Skip duplicate chunk_id
                conn.rollback()
                total_failed += 1
                continue
            except Exception as e:
                print(f"Row {row_num}: Error inserting chunk_id {chunk_id}: {e}")
                conn.rollback()
                total_failed += 1
                continue

except FileNotFoundError:
    print(f"Error: {csv_file} not found")
    cursor.close()
    conn.close()
    exit(1)
except Exception as e:
    print(f"Error reading CSV: {e}")
    cursor.close()
    conn.close()
    exit(1)

# Commit and close
conn.commit()
cursor.close()
conn.close()

# Print summary statistics
print(f"\n{'='*50}")
print(f"Import Complete!")
print(f"{'='*50}")
print(f"Total rows processed: {total_processed}")
print(f"Total rows inserted:  {total_inserted}")
print(f"Total failed rows:    {total_failed}")
print(f"{'='*50}")
