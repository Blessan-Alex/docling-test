#!/usr/bin/env python3
"""
Simple docling installation and testing script
This script demonstrates various ways to install and test docling
"""

import subprocess
import sys
import os
from pathlib import Path

def test_installation_methods():
    """Test different pip installation methods for docling"""
    print("🚀 DOCLING INSTALLATION TESTING")
    print("=" * 50)
    
    installation_methods = [
        {
            "name": "Basic Installation",
            "command": [sys.executable, "-m", "pip", "install", "docling"],
            "description": "Standard pip install"
        },
        {
            "name": "Verbose Installation", 
            "command": [sys.executable, "-m", "pip", "install", "-v", "docling"],
            "description": "Install with verbose output"
        },
        {
            "name": "Force Reinstall",
            "command": [sys.executable, "-m", "pip", "install", "--force-reinstall", "docling"],
            "description": "Force reinstall existing package"
        },
        {
            "name": "No Dependencies",
            "command": [sys.executable, "-m", "pip", "install", "--no-deps", "docling"],
            "description": "Install without dependencies"
        },
        {
            "name": "User Installation",
            "command": [sys.executable, "-m", "pip", "install", "--user", "docling"],
            "description": "Install to user directory"
        },
        {
            "name": "Break System Packages",
            "command": [sys.executable, "-m", "pip", "install", "--break-system-packages", "docling"],
            "description": "Override system package management"
        }
    ]
    
    results = {}
    
    for method in installation_methods:
        print(f"\n🔄 Testing: {method['name']}")
        print(f"   Description: {method['description']}")
        print(f"   Command: {' '.join(method['command'])}")
        
        try:
            result = subprocess.run(
                method['command'], 
                capture_output=True, 
                text=True, 
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                print("   ✅ SUCCESS")
                results[method['name']] = "SUCCESS"
            else:
                print("   ❌ FAILED")
                print(f"   Error: {result.stderr[:200]}...")
                results[method['name']] = "FAILED"
                
        except subprocess.TimeoutExpired:
            print("   ⏰ TIMEOUT")
            results[method['name']] = "TIMEOUT"
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            results[method['name']] = "ERROR"
    
    return results

def test_import():
    """Test importing docling modules"""
    print("\n🔍 TESTING DOCLING IMPORTS")
    print("=" * 50)
    
    import_tests = [
        ("docling", "Main docling module"),
        ("docling.document_converter", "DocumentConverter class"),
        ("docling.datamodel.base_models", "Base models"),
        ("docling.datamodel.pipeline_options", "Pipeline options")
    ]
    
    results = {}
    
    for module, description in import_tests:
        try:
            __import__(module)
            print(f"✅ {description}: SUCCESS")
            results[module] = "SUCCESS"
        except ImportError as e:
            print(f"❌ {description}: FAILED - {e}")
            results[module] = "FAILED"
        except Exception as e:
            print(f"❌ {description}: ERROR - {e}")
            results[module] = "ERROR"
    
    return results

def create_sample_files():
    """Create sample files for testing"""
    print("\n📁 CREATING SAMPLE TEST FILES")
    print("=" * 50)
    
    sample_files = {}
    
    # Create a simple text file
    txt_content = """Sample Document for Docling Testing
=====================================

This is a sample text document to test docling functionality.

Features to test:
- Text extraction
- Format preservation
- Document structure recognition

Testing various document processing capabilities.
"""
    
    with open("sample.txt", "w") as f:
        f.write(txt_content)
    sample_files['txt'] = "sample.txt"
    print("✅ Created sample.txt")
    
    # Create HTML file
    html_content = """<!DOCTYPE html>
<html>
<head><title>Sample HTML</title></head>
<body>
    <h1>Sample HTML Document</h1>
    <p>This is a test HTML document for docling.</p>
    <ul>
        <li>HTML parsing</li>
        <li>Structure extraction</li>
        <li>Content conversion</li>
    </ul>
</body>
</html>"""
    
    with open("sample.html", "w") as f:
        f.write(html_content)
    sample_files['html'] = "sample.html"
    print("✅ Created sample.html")
    
    # Create Markdown file
    md_content = """# Sample Markdown Document

This is a sample markdown document for testing docling.

## Features

- **Bold text**
- *Italic text*
- `Code snippets`

### Code Example

```python
def hello_world():
    print("Hello, Docling!")
```

### Table

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
"""
    
    with open("sample.md", "w") as f:
        f.write(md_content)
    sample_files['md'] = "sample.md"
    print("✅ Created sample.md")
    
    return sample_files

def test_docling_cli():
    """Test docling CLI interface"""
    print("\n🖥️  TESTING DOCLING CLI")
    print("=" * 50)
    
    cli_tests = [
        ("docling --help", "Help command"),
        ("docling --version", "Version command"),
        ("docling sample.txt", "Text file processing"),
        ("docling sample.html", "HTML file processing"),
        ("docling sample.md", "Markdown file processing")
    ]
    
    results = {}
    
    for command, description in cli_tests:
        try:
            result = subprocess.run(
                command.split(), 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"✅ {description}: SUCCESS")
                print(f"   Output: {result.stdout[:100]}...")
                results[command] = "SUCCESS"
            else:
                print(f"❌ {description}: FAILED")
                print(f"   Error: {result.stderr[:100]}...")
                results[command] = "FAILED"
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {description}: TIMEOUT")
            results[command] = "TIMEOUT"
        except Exception as e:
            print(f"❌ {description}: ERROR - {e}")
            results[command] = "ERROR"
    
    return results

def test_python_api():
    """Test docling Python API"""
    print("\n🐍 TESTING DOCLING PYTHON API")
    print("=" * 50)
    
    api_tests = [
        {
            "name": "Basic Document Conversion",
            "code": """
from docling.document_converter import DocumentConverter
converter = DocumentConverter()
result = converter.convert('sample.txt')
print('SUCCESS: Document converted')
print('Length:', len(result.document.export_to_text()))
"""
        },
        {
            "name": "Markdown Export",
            "code": """
from docling.document_converter import DocumentConverter
converter = DocumentConverter()
result = converter.convert('sample.html')
markdown = result.document.export_to_markdown()
print('SUCCESS: Markdown export')
print('Length:', len(markdown))
"""
        },
        {
            "name": "Text Export",
            "code": """
from docling.document_converter import DocumentConverter
converter = DocumentConverter()
result = converter.convert('sample.md')
text = result.document.export_to_text()
print('SUCCESS: Text export')
print('Length:', len(text))
"""
        }
    ]
    
    results = {}
    
    for test in api_tests:
        try:
            exec(test['code'])
            print(f"✅ {test['name']}: SUCCESS")
            results[test['name']] = "SUCCESS"
        except Exception as e:
            print(f"❌ {test['name']}: FAILED - {e}")
            results[test['name']] = "FAILED"
    
    return results

def cleanup():
    """Clean up test files"""
    print("\n🧹 CLEANUP")
    print("=" * 50)
    
    files_to_remove = ["sample.txt", "sample.html", "sample.md"]
    
    for file in files_to_remove:
        try:
            if os.path.exists(file):
                os.remove(file)
                print(f"✅ Removed {file}")
        except Exception as e:
            print(f"⚠️  Could not remove {file}: {e}")

def main():
    """Main test function"""
    print("🚀 DOCLING COMPREHENSIVE TEST SUITE")
    print("Testing installation and functionality")
    print("=" * 60)
    
    # Test installation methods
    install_results = test_installation_methods()
    
    # Test imports
    import_results = test_import()
    
    # Create sample files
    sample_files = create_sample_files()
    
    # Test CLI
    cli_results = test_docling_cli()
    
    # Test Python API
    api_results = test_python_api()
    
    # Cleanup
    cleanup()
    
    # Summary
    print("\n📊 TEST SUMMARY")
    print("=" * 60)
    
    print("\n🔧 Installation Results:")
    for method, result in install_results.items():
        print(f"   {method}: {result}")
    
    print("\n📦 Import Results:")
    for module, result in import_results.items():
        print(f"   {module}: {result}")
    
    print("\n🖥️  CLI Results:")
    for command, result in cli_results.items():
        print(f"   {command}: {result}")
    
    print("\n🐍 API Results:")
    for test, result in api_results.items():
        print(f"   {test}: {result}")
    
    print("\n🎉 Test suite completed!")
    print("\n📋 Next Steps:")
    print("1. If installation failed, try creating a virtual environment")
    print("2. If imports failed, check if docling is properly installed")
    print("3. If CLI failed, ensure docling is in your PATH")
    print("4. If API failed, check docling documentation for usage examples")

if __name__ == "__main__":
    main()
