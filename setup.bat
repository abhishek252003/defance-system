@echo off
title ARGUS Defense Intelligence System Setup

echo 🛡️ Setting up ARGUS Defense Intelligence System...
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Download spaCy English model
echo Downloading spaCy English language model...
python -m spacy download en_core_web_sm

echo.
echo ✅ Setup complete!
echo.
echo To run the system:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Run the scraper: python defense_scraper.py
echo 3. Process intelligence: python defense_intelligence.py --batch-process
echo 4. Launch dashboard: streamlit run app.py
echo.
pause