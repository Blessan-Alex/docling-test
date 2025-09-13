#!/usr/bin/env python3
"""
KMRL Document Processing Test Suite
Tests docling with real KMRL document types and scenarios
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime
import traceback

def test_docling_import():
    """Test if docling is properly imported"""
    print("🔍 Testing Docling Import")
    print("=" * 50)
    
    try:
        import docling
        print("✅ Docling imported successfully!")
        
        try:
            print(f"📦 Version: {docling.__version__}")
        except AttributeError:
            print("📦 Version: Available (version info not accessible)")
        
        from docling.document_converter import DocumentConverter
        print("✅ DocumentConverter imported successfully!")
        
        from docling.datamodel.base_models import InputFormat
        print("✅ InputFormat imported successfully!")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("Please ensure docling is installed: pip install --break-system-packages docling")
        return False

def get_test_documents():
    """Get all test documents from test-docs directory"""
    test_docs_dir = Path("test-docs")
    
    if not test_docs_dir.exists():
        print(f"❌ Test documents directory not found: {test_docs_dir}")
        return {}
    
    documents = {}
    
    # Categorize documents by type
    for file_path in test_docs_dir.iterdir():
        if file_path.is_file():
            file_ext = file_path.suffix.lower()
            file_name = file_path.name
            
            if file_ext in ['.jpg', '.jpeg', '.png']:
                # Images (OCR testing)
                if 'mal' in file_name.lower():
                    category = 'malayalam_ocr'
                elif 'handwrite' in file_name.lower() or 'handwritten' in file_name.lower():
                    category = 'handwritten_ocr'
                elif 'scan' in file_name.lower():
                    category = 'scanned_document'
                else:
                    category = 'image_ocr'
            elif file_ext == '.dwg':
                category = 'engineering_drawing'
            elif file_ext == '.docx':
                category = 'word_document'
            elif file_ext == '.pptx':
                category = 'powerpoint_presentation'
            elif file_ext == '.csv':
                category = 'data_file'
            else:
                category = 'other'
            
            if category not in documents:
                documents[category] = []
            
            documents[category].append({
                'path': str(file_path),
                'name': file_name,
                'size': file_path.stat().st_size,
                'extension': file_ext
            })
    
    return documents

def test_document_conversion(file_path, category, doc_info):
    """Test document conversion with docling"""
    print(f"\n🔄 Testing: {doc_info['name']}")
    print(f"   Category: {category}")
    print(f"   Size: {doc_info['size']:,} bytes")
    print(f"   Extension: {doc_info['extension']}")
    
    try:
        from docling.document_converter import DocumentConverter
        converter = DocumentConverter()
        
        # Convert document
        result = converter.convert(file_path)
        
        # Extract content
        markdown_content = result.document.export_to_markdown()
        text_content = result.document.export_to_text()
        
        # Analyze results
        success_info = {
            'file_name': doc_info['name'],
            'category': category,
            'file_size': doc_info['size'],
            'conversion_successful': True,
            'markdown_length': len(markdown_content),
            'text_length': len(text_content),
            'has_content': len(text_content.strip()) > 0,
            'preview': text_content[:200] + "..." if len(text_content) > 200 else text_content,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"   ✅ Conversion successful!")
        print(f"   📊 Markdown length: {len(markdown_content)} chars")
        print(f"   📊 Text length: {len(text_content)} chars")
        print(f"   📝 Has content: {'Yes' if success_info['has_content'] else 'No'}")
        
        if success_info['has_content']:
            print(f"   📝 Preview: {success_info['preview']}")
        else:
            print(f"   ⚠️  No text content extracted")
        
        return success_info
        
    except Exception as e:
        error_info = {
            'file_name': doc_info['name'],
            'category': category,
            'file_size': doc_info['size'],
            'conversion_successful': False,
            'error': str(e),
            'error_type': type(e).__name__,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"   ❌ Conversion failed: {e}")
        print(f"   🔍 Error type: {type(e).__name__}")
        
        return error_info

def test_category(category, documents):
    """Test all documents in a category"""
    print(f"\n📁 Testing Category: {category.upper()}")
    print("=" * 60)
    print(f"📊 Documents in category: {len(documents)}")
    
    results = []
    
    for doc_info in documents:
        result = test_document_conversion(doc_info['path'], category, doc_info)
        results.append(result)
    
    # Category summary
    successful = sum(1 for r in results if r['conversion_successful'])
    failed = len(results) - successful
    
    print(f"\n📊 Category Summary:")
    print(f"   ✅ Successful: {successful}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📈 Success rate: {(successful/len(results)*100):.1f}%")
    
    return results

def test_cli_interface():
    """Test docling CLI interface with sample documents"""
    print(f"\n🖥️  Testing CLI Interface")
    print("=" * 50)
    
    test_docs_dir = Path("test-docs")
    if not test_docs_dir.exists():
        print("❌ Test documents directory not found")
        return []
    
    # Find a simple text-based document for CLI testing
    cli_test_files = []
    for file_path in test_docs_dir.iterdir():
        if file_path.suffix.lower() in ['.txt', '.csv', '.md']:
            cli_test_files.append(file_path)
            if len(cli_test_files) >= 3:  # Test max 3 files
                break
    
    if not cli_test_files:
        print("⚠️  No suitable files found for CLI testing")
        return []
    
    cli_results = []
    
    for file_path in cli_test_files[:3]:  # Test up to 3 files
        try:
            import subprocess
            
            print(f"\n🔄 CLI Testing: {file_path.name}")
            
            # Test CLI command
            result = subprocess.run(
                [sys.executable, "-m", "docling", str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                cli_result = {
                    'file_name': file_path.name,
                    'cli_successful': True,
                    'output_length': len(result.stdout),
                    'preview': result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout
                }
                print(f"   ✅ CLI successful!")
                print(f"   📊 Output length: {len(result.stdout)} chars")
                cli_results.append(cli_result)
            else:
                cli_result = {
                    'file_name': file_path.name,
                    'cli_successful': False,
                    'error': result.stderr,
                    'return_code': result.returncode
                }
                print(f"   ❌ CLI failed: {result.stderr[:100]}...")
                cli_results.append(cli_result)
                
        except subprocess.TimeoutExpired:
            print(f"   ⏰ CLI timeout for {file_path.name}")
            cli_results.append({
                'file_name': file_path.name,
                'cli_successful': False,
                'error': 'Timeout'
            })
        except Exception as e:
            print(f"   ❌ CLI error: {e}")
            cli_results.append({
                'file_name': file_path.name,
                'cli_successful': False,
                'error': str(e)
            })
    
    return cli_results

def generate_kmrl_report(all_results, cli_results):
    """Generate comprehensive KMRL test report"""
    print(f"\n📋 KMRL DOCUMENT PROCESSING REPORT")
    print("=" * 60)
    
    # Overall statistics
    total_documents = sum(len(results) for results in all_results.values())
    total_successful = sum(
        sum(1 for r in results if r['conversion_successful'])
        for results in all_results.values()
    )
    total_failed = total_documents - total_successful
    
    print(f"📊 Overall Statistics:")
    print(f"   📄 Total documents tested: {total_documents}")
    print(f"   ✅ Successful conversions: {total_successful}")
    print(f"   ❌ Failed conversions: {total_failed}")
    print(f"   📈 Overall success rate: {(total_successful/total_documents*100):.1f}%")
    
    # Category breakdown
    print(f"\n📁 Category Breakdown:")
    for category, results in all_results.items():
        successful = sum(1 for r in results if r['conversion_successful'])
        total = len(results)
        success_rate = (successful/total*100) if total > 0 else 0
        
        print(f"   {category.replace('_', ' ').title()}: {successful}/{total} ({success_rate:.1f}%)")
        
        # Show failed documents
        failed_docs = [r for r in results if not r['conversion_successful']]
        if failed_docs:
            print(f"      ❌ Failed: {', '.join([d['file_name'] for d in failed_docs])}")
    
    # CLI results
    if cli_results:
        cli_successful = sum(1 for r in cli_results if r['cli_successful'])
        print(f"\n🖥️  CLI Interface:")
        print(f"   ✅ Successful: {cli_successful}/{len(cli_results)}")
        print(f"   📈 CLI success rate: {(cli_successful/len(cli_results)*100):.1f}%")
    
    # KMRL Readiness Assessment
    print(f"\n🎯 KMRL READINESS ASSESSMENT:")
    
    # Check critical categories
    critical_categories = ['word_document', 'powerpoint_presentation', 'data_file']
    critical_success = True
    
    for category in critical_categories:
        if category in all_results:
            results = all_results[category]
            successful = sum(1 for r in results if r['conversion_successful'])
            if successful == 0:
                critical_success = False
                print(f"   ❌ {category.replace('_', ' ').title()}: Not ready")
            else:
                print(f"   ✅ {category.replace('_', ' ').title()}: Ready")
    
    # OCR capabilities
    ocr_categories = ['malayalam_ocr', 'handwritten_ocr', 'scanned_document', 'image_ocr']
    ocr_success = 0
    ocr_total = 0
    
    for category in ocr_categories:
        if category in all_results:
            results = all_results[category]
            ocr_total += len(results)
            ocr_success += sum(1 for r in results if r['conversion_successful'])
    
    if ocr_total > 0:
        ocr_rate = (ocr_success/ocr_total*100)
        print(f"   📸 OCR Capability: {ocr_success}/{ocr_total} ({ocr_rate:.1f}%)")
        if ocr_rate >= 50:
            print(f"      ✅ OCR ready for KMRL Malayalam documents")
        else:
            print(f"      ⚠️  OCR may need improvement for Malayalam content")
    
    # Engineering drawings
    if 'engineering_drawing' in all_results:
        eng_results = all_results['engineering_drawing']
        eng_successful = sum(1 for r in eng_results if r['conversion_successful'])
        print(f"   🏗️  Engineering Drawings: {eng_successful}/{len(eng_results)}")
        if eng_successful > 0:
            print(f"      ✅ Basic CAD file support available")
        else:
            print(f"      ⚠️  CAD files (.dwg) not directly supported")
    
    # Final recommendation
    print(f"\n🚀 RECOMMENDATION:")
    if critical_success and total_successful >= total_documents * 0.7:
        print(f"   ✅ Docling is READY for KMRL deployment!")
        print(f"   📋 Next steps:")
        print(f"      1. Set up batch processing pipeline")
        print(f"      2. Configure Malayalam OCR settings")
        print(f"      3. Integrate with SharePoint/email systems")
        print(f"      4. Train staff on document processing workflow")
    else:
        print(f"   ⚠️  Docling needs additional configuration for KMRL")
        print(f"   📋 Recommended actions:")
        print(f"      1. Test with more KMRL-specific document samples")
        print(f"      2. Configure OCR for Malayalam text")
        print(f"      3. Set up document preprocessing pipeline")
        print(f"      4. Consider additional tools for CAD files")

def save_results(all_results, cli_results):
    """Save test results to JSON file"""
    report_data = {
        'test_timestamp': datetime.now().isoformat(),
        'docling_version': None,
        'total_documents': sum(len(results) for results in all_results.values()),
        'categories': all_results,
        'cli_results': cli_results,
        'summary': {
            'total_successful': sum(
                sum(1 for r in results if r['conversion_successful'])
                for results in all_results.values()
            ),
            'total_failed': sum(
                sum(1 for r in results if not r['conversion_successful'])
                for results in all_results.values()
            )
        }
    }
    
    try:
        import docling
        report_data['docling_version'] = docling.__version__
    except:
        pass
    
    with open('kmrl_docling_test_results.json', 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n💾 Results saved to: kmrl_docling_test_results.json")

def main():
    """Main test function"""
    print("🚀 KMRL DOCUMENT PROCESSING TEST SUITE")
    print("Testing docling with real KMRL document scenarios")
    print("=" * 60)
    
    # Test docling import
    if not test_docling_import():
        print("\n❌ Cannot proceed without docling. Please install it first.")
        return
    
    # Get test documents
    documents = get_test_documents()
    
    if not documents:
        print("\n❌ No test documents found. Please check test-docs directory.")
        return
    
    print(f"\n📁 Found {sum(len(docs) for docs in documents.values())} test documents")
    print(f"📊 Categories: {', '.join(documents.keys())}")
    
    # Test each category
    all_results = {}
    for category, docs in documents.items():
        results = test_category(category, docs)
        all_results[category] = results
    
    # Test CLI interface
    cli_results = test_cli_interface()
    
    # Generate report
    generate_kmrl_report(all_results, cli_results)
    
    # Save results
    save_results(all_results, cli_results)
    
    print(f"\n🎉 KMRL Document Processing Test Complete!")
    print(f"📋 Check 'kmrl_docling_test_results.json' for detailed results")

if __name__ == "__main__":
    main()
