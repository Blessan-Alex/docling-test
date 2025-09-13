#!/usr/bin/env python3
"""
Analyze image properties for OCR suitability
"""

import sys
from PIL import Image
import os

def analyze_image(image_path):
    """Analyze image properties"""
    
    if not os.path.exists(image_path):
        print(f"Error: File '{image_path}' not found")
        return
    
    try:
        with Image.open(image_path) as img:
            print(f"📸 Image Analysis: {image_path}")
            print("=" * 40)
            print(f"📏 Size: {img.size[0]} x {img.size[1]} pixels")
            print(f"🎨 Mode: {img.mode}")
            print(f"📊 Format: {img.format}")
            print(f"💾 File size: {os.path.getsize(image_path):,} bytes")
            
            # Check if image is suitable for OCR
            width, height = img.size
            
            if width < 500 or height < 500:
                print("⚠️  Image might be too small for good OCR")
            else:
                print("✅ Image size looks good for OCR")
            
            if img.mode != 'RGB':
                print("⚠️  Image mode is not RGB - might affect OCR")
            else:
                print("✅ Image mode is RGB - good for OCR")
                
    except Exception as e:
        print(f"Error analyzing image: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 analyze_image.py <image_file>")
        sys.exit(1)
    
    analyze_image(sys.argv[1])

if __name__ == "__main__":
    main()
