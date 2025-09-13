#!/usr/bin/env python3
"""
Simple docling test - process one file and save results
Usage: python3 simple_test.py input_file output_format
"""

import sys
import os
from pathlib import Path
from docling.document_converter import DocumentConverter

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 simple_test.py <input_file> <output_format>")
        print("Output formats: txt, md, json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_format = sys.argv[2]
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    # Create results directory
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    # Get output filename
    input_path = Path(input_file)
    output_filename = input_path.stem + f".{output_format}"
    output_path = results_dir / output_filename
    
    print(f"Processing: {input_file}")
    print(f"Output format: {output_format}")
    print(f"Output file: {output_path}")
    
    try:
        # Initialize converter
        converter = DocumentConverter()
        
        # Convert document
        result = converter.convert(input_file)
        
        # Extract content based on format
        if output_format == "txt":
            content = result.document.export_to_text()
        elif output_format == "md":
            content = result.document.export_to_markdown()
        elif output_format == "json":
            import json
            content = json.dumps({
                "file": input_file,
                "text": result.document.export_to_text(),
                "markdown": result.document.export_to_markdown()
            }, indent=2)
        else:
            print(f"Error: Unsupported format '{output_format}'")
            sys.exit(1)
        
        # Save results
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Success! Saved {len(content)} characters to {output_path}")
        
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
