#!/usr/bin/env python3
"""
ARGUS Project Setup Script
This script sets up the Python virtual environment and requirements for the ARGUS intelligence gathering system.
"""

import os
import subprocess
import sys
from pathlib import Path

def create_virtual_environment():
    """Create a Python virtual environment in the project root."""
    print("Creating Python virtual environment...")
    try:
        # Create virtual environment
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("✓ Virtual environment created successfully at .venv/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create virtual environment: {e}")
        return False

def create_requirements_file():
    """Generate requirements.txt with necessary dependencies."""
    print("Creating requirements.txt file...")
    
    requirements = [
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "spacy>=3.7.0",
        "torch>=2.0.0",
        "streamlit>=1.28.0"
    ]
    
    try:
        with open("requirements.txt", "w") as f:
            for req in requirements:
                f.write(f"{req}\n")
        print("✓ requirements.txt created successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to create requirements.txt: {e}")
        return False

def print_next_steps():
    """Print instructions for the user to complete the setup."""
    print("\n" + "="*60)
    print("ARGUS PROJECT SETUP COMPLETE!")
    print("="*60)
    print("\nNext steps to complete the environment setup:")
    print("\n1. Activate the virtual environment:")
    print("   Windows: .venv\\Scripts\\activate")
    print("   Linux/Mac: source .venv/bin/activate")
    
    print("\n2. Install the required packages:")
    print("   pip install -r requirements.txt")
    
    print("\n3. Download spaCy language model:")
    print("   python -m spacy download en_core_web_sm")
    
    print("\n4. Verify installation:")
    print("   python -c \"import requests, bs4, spacy, streamlit; print('All packages installed successfully!')\"")
    
    print("\nYour ARGUS project is ready for development!")
    print("="*60)

def main():
    """Main setup function."""
    print("ARGUS Intelligence Gathering System - Environment Setup")
    print("="*60)
    
    # Ensure we're in the project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Create virtual environment
    venv_success = create_virtual_environment()
    
    # Create requirements file
    req_success = create_requirements_file()
    
    if venv_success and req_success:
        print_next_steps()
        return 0
    else:
        print("\n✗ Setup encountered errors. Please check the output above.")
        return 1

if __name__ == "__main__":
    exit(main())