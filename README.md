# ARGUS Intelligence Gathering System

**ARGUS** is a comprehensive intelligence gathering and analysis prototype that scrapes news articles, extracts entities using AI, and provides an interactive dashboard for analysis.

## 🌟 Features

- **Web Scraping**: Automatically extract content from news articles
- **AI-Powered Analysis**: Extract people, organizations, and locations using spaCy NLP
- **Database Storage**: Store articles and entities in SQLite database
- **Interactive Dashboard**: Streamlit-based web interface for data visualization
- **Full Pipeline Integration**: Complete end-to-end analysis workflow

## 📁 Project Structure

```
argus/
├── setup_env.py              # Environment setup script
├── requirements.txt          # Python dependencies
├── dashboard.py              # Main Streamlit dashboard
├── NLP_SETUP.md             # NLP setup instructions
├── argus_scraper/           # Core scraping and processing modules
│   ├── __init__.py
│   ├── scraper.py           # Web scraping functionality
│   └── process_text.py      # NLP processing and database operations
├── scraped_data/            # JSON files of scraped articles (auto-created)
└── intelligence.db          # SQLite database (auto-created)
```

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Navigate to the argus directory
cd argus

# Run the setup script
python setup_env.py

# Activate the virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

### 2. Test the Scraper

```bash
# Scrape a news article (replace with actual URL)
python argus_scraper/scraper.py https://www.bbc.com/news/technology-12345678
```

### 3. Process with AI

```bash
# Extract entities from the scraped article
python argus_scraper/process_text.py
```

### 4. Launch Dashboard

```bash
# Start the Streamlit dashboard
streamlit run dashboard.py
```

## 📖 Detailed Usage

### Web Scraping

The `scraper.py` module can extract article content from most news websites:

```python
from argus_scraper.scraper import scrape_article, save_to_json

# Scrape an article
article_data = scrape_article("https://example.com/news/article")

# Save to JSON file
save_to_json(article_data)
```

### Entity Extraction

The `process_text.py` module uses spaCy to extract named entities:

```python
from argus_scraper.process_text import extract_entities, save_to_db

# Extract entities from text
entities = extract_entities(article_content)

# Save to database
save_to_db(article_data, entities)
```

### Dashboard Features

The Streamlit dashboard provides:

- **URL Analysis**: Direct scraping and analysis from the web interface
- **Article Browser**: View all scraped articles
- **Entity Visualization**: Interactive charts and lists of extracted entities
- **Intelligence Overview**: Summary statistics and recent activity

## 🛠️ System Requirements

### Dependencies

- Python 3.8+
- requests (web scraping)
- beautifulsoup4 (HTML parsing)
- spacy (NLP processing)
- streamlit (web dashboard)
- sqlite3 (database - included with Python)

### Supported Websites

The scraper works with most news websites including:
- BBC News
- Reuters
- The Guardian
- CNN
- And many others

## 📊 Database Schema

### Articles Table
```sql
CREATE TABLE articles (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    scraped_timestamp TEXT NOT NULL,
    content_length INTEGER,
    word_count INTEGER
);
```

### Entities Table
```sql
CREATE TABLE entities (
    id INTEGER PRIMARY KEY,
    article_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    type TEXT NOT NULL,
    FOREIGN KEY (article_id) REFERENCES articles (id)
);
```

## 🔧 Configuration

### Scraper Settings

The scraper can be customized by modifying selectors in `scraper.py`:

```python
# Title selectors (in order of preference)
title_selectors = [
    'h1',
    'h2', 
    '.title',
    '.headline',
    '.article-title'
]

# Content selectors
content_selectors = [
    'article',
    '.article-body',
    '.content',
    '.story-body'
]
```

### Entity Types

The system extracts three main entity types:
- **PERSON**: People's names
- **ORG**: Organizations, companies, agencies
- **LOCATION**: Countries, cities, geographical locations

## 🚨 Troubleshooting

### Common Issues

1. **spaCy model not found**
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **Import errors**
   - Ensure virtual environment is activated
   - Install requirements: `pip install -r requirements.txt`

3. **Scraping fails**
   - Check URL is accessible
   - Some sites may block automated requests
   - Try different news websites

4. **Dashboard not loading**
   - Ensure Streamlit is installed: `pip install streamlit`
   - Run from the correct directory: `streamlit run dashboard.py`

## 🧪 Testing

### Test the Complete Pipeline

```bash
# 1. Scrape a test article
python argus_scraper/scraper.py https://www.bbc.com/news

# 2. Process with NLP
python argus_scraper/process_text.py

# 3. View in dashboard
streamlit run dashboard.py
```

### Sample Test URLs

For testing purposes, try these reliable news sources:
- BBC: `https://www.bbc.com/news/technology-*`
- Reuters: `https://www.reuters.com/technology/*`
- The Guardian: `https://www.theguardian.com/technology/*`

## 📈 Performance

### Optimization Tips

1. **Batch Processing**: Process multiple articles at once
2. **Database Indexing**: Already optimized for common queries
3. **Memory Usage**: spaCy model loads once and reuses
4. **Caching**: Streamlit automatically caches database queries

### Scaling Considerations

- For high-volume processing, consider PostgreSQL instead of SQLite
- Implement rate limiting for web scraping
- Use Docker for consistent deployment environments

## 🤝 Contributing

This is a prototype system. Key areas for enhancement:

1. **Additional NLP Features**
   - Sentiment analysis
   - Topic modeling
   - Relationship extraction

2. **Enhanced Scraping**
   - Support for more website types
   - PDF document processing
   - Social media integration

3. **Advanced Dashboard**
   - Real-time monitoring
   - Export capabilities
   - Advanced filtering

## 📄 License

This project is provided as an educational prototype. Use responsibly and respect website terms of service when scraping.

## ⚠️ Legal Notice

Always respect robots.txt files and website terms of service. This tool is for educational and research purposes. Ensure you have permission to scrape content from websites.

---

**ARGUS** - *Advanced Reconnaissance and General Understanding System*

# 🛡️ ARGUS Defense Intelligence System

## Advanced Reconnaissance and General Understanding System

ARGUS is a comprehensive defense intelligence monitoring system that provides real-time threat assessment and intelligence visualization for national security.

## 🚀 Features

### Real-time Monitoring
- Auto-refresh every 30 seconds
- Live data indicators showing new articles
- Continuous threat assessment updates

### Intelligence Analysis
- Threat level classification (High/Medium/Low)
- Defense entity extraction (military units, weapons)
- Security incident detection and alerts

### Data Visualization
- Interactive threat timeline (30-day view)
- Threat distribution charts
- Real-time metrics dashboard

### User Interface
- Professional military-grade design
- Responsive layout for all devices
- Intuitive controls and navigation

## 📋 Requirements

```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
```

## 🚀 Quick Start

### Local Deployment
```bash
# Clone the repository
git clone https://github.com/yourusername/argus-defense-dashboard.git
cd argus-defense-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

### Access the Dashboard
Open your browser to: http://localhost:8501

## ☁️ Streamlit Cloud Deployment

### One-click Deployment
[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

### Manual Deployment Steps
1. Fork this repository
2. Go to https://share.streamlit.io/
3. Click "New app"
4. Select your forked repository
5. Set main file path to `app.py`
6. Click "Deploy"

## 🎯 Usage

### Live Monitoring
- Enable auto-refresh for continuous updates
- Click "Start Live Monitor" to begin data collection
- Use "Process New Data" to analyze collected intelligence

### Data Analysis
- Filter by threat level (High/Medium/Low)
- Select time ranges (24h, 7d, 30d, All)
- View detailed threat reports and alerts

## 🔧 Configuration

The system can be customized through environment variables:

```
ARGUS_PORT=8501              # Dashboard port
ARGUS_REFRESH_INTERVAL=30     # Auto-refresh interval (seconds)
```

## 📊 Sample Data

When deployed without real data sources, the system will automatically initialize with sample defense intelligence data for demonstration purposes.

## 🛡️ Security

- All data processing is local
- No external data transmission
- Secure database storage

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Streamlit, Pandas, and Plotly
- Defense intelligence analysis powered by custom algorithms
