#!/usr/bin/env python3
"""
Test Malayalam OCR with different configurations
"""

import sys
import os
from pathlib import Path
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions

def test_malayalam_ocr(input_file):
    """Test Malayalam OCR with different settings"""
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found")
        return
    
    print(f"Testing Malayalam OCR on: {input_file}")
    print("=" * 50)
    
    # Create results directory
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    input_path = Path(input_file)
    
    # Test 1: Default settings
    print("\n🔄 Test 1: Default OCR settings")
    try:
        converter = DocumentConverter()
        result = converter.convert(input_file)
        text = result.document.export_to_text()
        
        output_file = results_dir / f"{input_path.stem}_default.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"✅ Default: {len(text)} characters extracted")
        print(f"📝 Preview: {text[:100]}...")
        
    except Exception as e:
        print(f"❌ Default failed: {e}")
    
    # Test 2: With pipeline options
    print("\n🔄 Test 2: Custom pipeline options")
    try:
        pipeline_options = PdfPipelineOptions()
        # You can configure OCR options here
        converter = DocumentConverter(pipeline_options=pipeline_options)
        result = converter.convert(input_file)
        text = result.document.export_to_text()
        
        output_file = results_dir / f"{input_path.stem}_custom.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"✅ Custom: {len(text)} characters extracted")
        print(f"📝 Preview: {text[:100]}...")
        
    except Exception as e:
        print(f"❌ Custom failed: {e}")
    
    print(f"\n📁 Results saved in: {results_dir}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 malayalam_ocr_test.py <image_file>")
        sys.exit(1)
    
    test_malayalam_ocr(sys.argv[1])

if __name__ == "__main__":
    main()
