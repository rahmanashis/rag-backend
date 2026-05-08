#!/usr/bin/env python3
"""
RAG System - PDF Text Extraction Script
Extracts text from all PDFs in data/input_pdfs folder
and saves processed data to data/processed/data.json
"""

import os
import json
import re
from pathlib import Path
import fitz  # PyMuPDF


def clean_text(text):
    """
    Clean text by removing extra whitespace and normalizing content.
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove leading and trailing whitespace
    text = text.strip()
    return text


def extract_pdf_text(pdf_path):
    """
    Extract text from all pages of a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        list: List of dictionaries containing page data
    """
    pages_data = []
    
    try:
        # Open the PDF document
        doc = fitz.open(pdf_path)
        
        # Extract text from each page
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            cleaned_text = clean_text(text)
            
            # Only store pages with content
            if cleaned_text:
                pages_data.append({
                    "filename": os.path.basename(pdf_path),
                    "page_number": page_num,
                    "text": cleaned_text
                })
        
        doc.close()
        print(f"✓ Extracted {len(pages_data)} pages from {os.path.basename(pdf_path)}")
        
    except Exception as e:
        print(f"✗ Error processing {pdf_path}: {str(e)}")
    
    return pages_data


def main():
    """
    Main function to process all PDFs in the input folder.
    Uses hybrid approach: individual files + consolidated file + metadata index
    """
    # Define paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    input_folder = project_root / "data" / "input_pdfs"
    output_folder = project_root / "data" / "processed"
    pdfs_folder = output_folder / "pdfs"
    output_file = output_folder / "data.json"  # Consolidated
    metadata_file = output_folder / "metadata.json"  # Index
    
    # Create output folders if they don't exist
    output_folder.mkdir(parents=True, exist_ok=True)
    pdfs_folder.mkdir(parents=True, exist_ok=True)
    
    # Check if input folder exists
    if not input_folder.exists():
        print(f"✗ Input folder not found: {input_folder}")
        print(f"Creating input folder: {input_folder}")
        input_folder.mkdir(parents=True, exist_ok=True)
        return
    
    # Collect all PDF files
    pdf_files = list(input_folder.glob("*.pdf"))
    
    if not pdf_files:
        print(f"✗ No PDF files found in {input_folder}")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s) to process\n")
    
    # Process all PDFs
    all_data = []
    metadata = {
        "metadata": {
            "total_chunks": 0,
            "total_pdfs": len(pdf_files),
            "created_date": str(Path(__file__).parent.parent)
        },
        "pdfs": []
    }
    
    for pdf_file in pdf_files:
        pages_data = extract_pdf_text(str(pdf_file))
        all_data.extend(pages_data)
        
        # Save individual PDF chunks
        pdf_name = pdf_file.stem
        individual_file = pdfs_folder / f"{pdf_name}_chunks.json"
        
        try:
            with open(individual_file, 'w', encoding='utf-8') as f:
                json.dump(pages_data, f, indent=2, ensure_ascii=False)
            
            print(f"  ✓ Saved {len(pages_data)} chunks to {individual_file.name}")
            
            # Add to metadata
            metadata["pdfs"].append({
                "filename": pdf_file.name,
                "chunks_count": len(pages_data),
                "chunk_file": f"pdfs/{individual_file.name}"
            })
            
        except Exception as e:
            print(f"  ✗ Error saving individual file for {pdf_file.name}: {str(e)}")
    
    # Update metadata
    metadata["metadata"]["total_chunks"] = len(all_data)
    
    # Save consolidated JSON file (for training)
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Successfully saved {len(all_data)} pages to {output_file}")
        
    except Exception as e:
        print(f"✗ Error saving consolidated JSON file: {str(e)}")
    
    # Save metadata index
    try:
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Metadata saved to {metadata_file.name}")
        
    except Exception as e:
        print(f"✗ Error saving metadata: {str(e)}")
    
    print(f"\nTotal files processed: {len(pdf_files)}")


if __name__ == "__main__":
    main()
