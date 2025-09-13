#!/usr/bin/env python3
"""
Quick test of docling with KMRL documents
"""

from docling.document_converter import DocumentConverter
import os
from pathlib import Path

def test_single_document(file_path):
    """Test a single document"""
    print(f"🔄 Testing: {file_path}")
    
    try:
        converter = DocumentConverter()
        result = converter.convert(file_path)
        text = result.document.export_to_text()
        
        print(f"   ✅ Success! Length: {len(text)} chars")
        if len(text) > 0:
            print(f"   📝 Preview: {text[:100]}...")
        else:
            print(f"   ⚠️  No text extracted")
        
        return True
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

def main():
    print("🚀 Quick Docling Test for KMRL Documents")
    print("=" * 50)
    
    # Test documents in order of complexity
    test_files = [
        "test-docs/market_data.csv",
        "test-docs/Jiitak Resume.docx", 
        "test-docs/Working with Flow Operators.pptx",
        "test-docs/Stash - Decentralized Money Saving App.pptx"
    ]
    
    results = []
    
    for file_path in test_files:
        if os.path.exists(file_path):
            success = test_single_document(file_path)
            results.append((file_path, success))
        else:
            print(f"⚠️  File not found: {file_path}")
    
    # Summary
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n📊 Summary: {successful}/{total} successful")
    
    if successful > 0:
        print("✅ Docling is working with your KMRL documents!")
    else:
        print("❌ No documents processed successfully")

if __name__ == "__main__":
    main()
