#!/bin/bash

# ARGUS Defense Intelligence System Setup Script

echo "🛡️ Setting up ARGUS Defense Intelligence System..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Download spaCy English model
echo "Downloading spaCy English language model..."
python -m spacy download en_core_web_sm

echo "✅ Setup complete!"
echo ""
echo "To run the system:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the scraper: python defense_scraper.py"
echo "3. Process intelligence: python defense_intelligence.py --batch-process"
echo "4. Launch dashboard: streamlit run app.py"
echo ""
echo "For Windows users, use 'venv\Scripts\activate' to activate the virtual environment."