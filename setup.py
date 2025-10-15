#!/usr/bin/env python3
"""
ARGUS Setup and Installation Script
Easy one-click setup for users.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print ARGUS banner."""
    print("=" * 60)
    print("🛡️  ARGUS Defense Intelligence System Setup")
    print("   Advanced Reconnaissance and General Understanding System")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")

def create_virtual_environment():
    """Create virtual environment if it doesn't exist."""
    venv_path = Path(".venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    try:
        print("🔧 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("✅ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False

def get_pip_command():
    """Get the correct pip command for the platform."""
    if platform.system() == "Windows":
        return [".venv/Scripts/python.exe", "-m", "pip"]
    else:
        return [".venv/bin/python", "-m", "pip"]

def install_dependencies():
    """Install required dependencies."""
    try:
        print("📦 Installing dependencies...")
        pip_cmd = get_pip_command()
        
        # Upgrade pip first
        subprocess.run(pip_cmd + ["install", "--upgrade", "pip"], check=True)
        
        # Install core requirements
        core_requirements = [
            "requests>=2.31.0",
            "beautifulsoup4>=4.12.0", 
            "streamlit>=1.28.0",
            "pandas>=2.0.0",
            "plotly>=5.15.0"
        ]
        
        for req in core_requirements:
            print(f"   Installing {req}...")
            subprocess.run(pip_cmd + ["install", req], check=True)
        
        print("✅ Core dependencies installed successfully")
        
        # Optional: Install NLP dependencies
        response = input("\n🤔 Install advanced NLP features? (requires ~2GB download) [y/N]: ")
        if response.lower() in ['y', 'yes']:
            print("📥 Installing NLP dependencies...")
            subprocess.run(pip_cmd + ["install", "spacy>=3.7.0"], check=True)
            
            # Download spaCy model
            print("📥 Downloading English language model...")
            if platform.system() == "Windows":
                python_cmd = [".venv/Scripts/python.exe"]
            else:
                python_cmd = [".venv/bin/python"]
            
            subprocess.run(python_cmd + ["-m", "spacy", "download", "en_core_web_sm"], check=True)
            print("✅ NLP features installed successfully")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_directories():
    """Setup required directories."""
    try:
        print("📁 Setting up directories...")
        Path("defense_data").mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
        print("✅ Directories created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create directories: {e}")
        return False

def test_installation():
    """Test if installation was successful."""
    try:
        print("🧪 Testing installation...")
        
        # Test imports
        if platform.system() == "Windows":
            python_cmd = [".venv/Scripts/python.exe"]
        else:
            python_cmd = [".venv/bin/python"]
        
        test_code = '''
import requests
import streamlit
import pandas
import plotly
print("✅ All core modules imported successfully")
'''
        
        result = subprocess.run(
            python_cmd + ["-c", test_code], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Installation test passed")
            return True
        else:
            print(f"❌ Installation test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Installation test error: {e}")
        return False

def show_usage_instructions():
    """Show usage instructions."""
    if platform.system() == "Windows":
        python_cmd = ".venv\\Scripts\\python.exe"
        activate_cmd = ".venv\\Scripts\\activate"
    else:
        python_cmd = ".venv/bin/python"
        activate_cmd = "source .venv/bin/activate"
    
    print("\n" + "="*60)
    print("🎉 ARGUS Setup Complete!")
    print("="*60)
    print("\n📋 Quick Start Guide:")
    print(f"1. Activate virtual environment: {activate_cmd}")
    print(f"2. Start the dashboard: {python_cmd} -m streamlit run defense_dashboard.py")
    print("3. Open browser to: http://localhost:8502")
    print("\n🚀 Advanced Usage:")
    print(f"• Start live monitoring: {python_cmd} live_monitor.py")
    print(f"• Process data manually: {python_cmd} quick_data_processor.py")
    print(f"• Generate reports: {python_cmd} defense_intelligence.py --report")
    print("\n📚 Documentation:")
    print("• README.md - Full documentation")
    print("• LIVE_MONITORING_GUIDE.md - Live monitoring setup")
    print("\n🆘 Support:")
    print("• Check logs in 'logs/' directory for troubleshooting")
    print("• Ensure Python 3.8+ is installed")
    print("• All data is stored locally in 'defense_data/' directory")

def main():
    """Main setup function."""
    print_banner()
    
    # Check system requirements
    check_python_version()
    
    # Setup steps
    if not create_virtual_environment():
        sys.exit(1)
    
    if not install_dependencies():
        sys.exit(1)
    
    if not setup_directories():
        sys.exit(1)
    
    if not test_installation():
        sys.exit(1)
    
    # Show usage instructions
    show_usage_instructions()
    
    print("\n✅ ARGUS Defense Intelligence System is ready to use!")

if __name__ == "__main__":
    main()