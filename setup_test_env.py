#!/usr/bin/env python3
"""
Setup script for docling test environment
Creates virtual environment and installs dependencies
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description}: SUCCESS")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}: FAILED")
        print(f"   Error: {e.stderr}")
        return False

def main():
    """Setup test environment"""
    print("🚀 Setting up docling test environment")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 9):
        print("❌ Python 3.9+ required for docling")
        return False
    
    # Create virtual environment
    venv_path = Path("docling_test_env")
    if not venv_path.exists():
        success = run_command(f"{sys.executable} -m venv {venv_path}", "Creating virtual environment")
        if not success:
            return False
    else:
        print("✅ Virtual environment already exists")
    
    # Determine activation script
    if os.name == 'nt':  # Windows
        activate_script = venv_path / "Scripts" / "activate.bat"
        pip_cmd = str(venv_path / "Scripts" / "pip.exe")
        python_cmd = str(venv_path / "Scripts" / "python.exe")
    else:  # Unix/Linux/macOS
        activate_script = venv_path / "bin" / "activate"
        pip_cmd = str(venv_path / "bin" / "pip")
        python_cmd = str(venv_path / "bin" / "python")
    
    # Upgrade pip
    success = run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip")
    if not success:
        return False
    
    # Install wheel
    success = run_command(f"{pip_cmd} install wheel", "Installing wheel")
    if not success:
        return False
    
    # Install docling
    success = run_command(f"{pip_cmd} install docling", "Installing docling")
    if not success:
        return False
    
    # Install additional dependencies for testing
    success = run_command(f"{pip_cmd} install -r requirements.txt", "Installing test dependencies")
    if not success:
        return False
    
    # Test installation
    success = run_command(f"{python_cmd} -c \"import docling; print('Docling version:', docling.__version__)\"", "Testing docling import")
    if not success:
        return False
    
    print("\n🎉 Environment setup completed!")
    print(f"📁 Virtual environment: {venv_path}")
    print(f"🐍 Python executable: {python_cmd}")
    print(f"📦 Pip executable: {pip_cmd}")
    
    print("\n📋 To activate the environment:")
    if os.name == 'nt':
        print(f"   {activate_script}")
    else:
        print(f"   source {activate_script}")
    
    print("\n🚀 To run tests:")
    print(f"   {python_cmd} test_docling.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
