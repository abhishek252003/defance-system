# Getting Started with ARGUS Defense Intelligence System

This guide will help you quickly set up and run the ARGUS Defense Intelligence System.

## Prerequisites

- Python 3.8 or higher
- Git (optional, for cloning the repository)

## Installation

### Option 1: Quick Setup (Recommended)

1. Download or clone the repository
2. Run the setup script for your operating system:
   - Linux/macOS: `chmod +x setup.sh && ./setup.sh`
   - Windows: Double-click `setup.bat` or run `setup.bat` in command prompt

### Option 2: Manual Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Linux/macOS: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download the spaCy English language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## First Run

1. **Collect Defense News**:
   ```bash
   python defense_scraper.py
   ```
   This will scrape defense and security news from multiple sources and save the articles in the `defense_data/` directory.

2. **Process Intelligence**:
   ```bash
   python defense_intelligence.py --batch-process
   ```
   This analyzes all collected articles, extracts entities, classifies threat levels, and stores the intelligence in the database.

3. **View the Dashboard**:
   ```bash
   streamlit run app.py
   ```
   This launches the real-time dashboard where you can monitor threats, view alerts, and analyze intelligence.

## Daily Usage

For daily intelligence gathering:

1. Run the specialized today's news scraper:
   ```bash
   python todays_defense_scraper.py
   ```

2. Process today's intelligence:
   ```bash
   python defense_intelligence.py --batch-process
   ```

3. Generate a daily report:
   ```bash
   python todays_defense_report.py
   ```

4. Monitor the dashboard for real-time updates.

## Key Features to Explore

- **Threat Filtering**: Use the sidebar controls to filter by threat level (HIGH, MEDIUM, LOW)
- **Date Filtering**: Toggle between all-time data and today's news
- **Detailed Article View**: Check "Show Detailed Article List" to see comprehensive article information
- **Real-time Updates**: The dashboard automatically refreshes every 30 seconds
- **Alert System**: High-priority security alerts are prominently displayed

## Troubleshooting

### Common Issues

1. **Missing spaCy model**:
   ```
   Error: spaCy English model not found!
   ```
   Solution: Run `python -m spacy download en_core_web_sm`

2. **Database connection errors**:
   Ensure the database file `defense_intelligence.db` exists. If not, run the intelligence processor first.

3. **Streamlit not found**:
   ```
   command not found: streamlit
   ```
   Solution: Make sure you've activated your virtual environment and installed requirements.

### Need Help?

- Check the documentation files in the repository
- Open an issue on GitHub
- Review the console output for error messages