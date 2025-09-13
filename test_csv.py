from docling.document_converter import DocumentConverter

print("Testing CSV file with docling...")
converter = DocumentConverter()
result = converter.convert('test-docs/market_data.csv')
text = result.document.export_to_text()
print(f"Success! Extracted {len(text)} characters")
print("Preview:", text[:200])
