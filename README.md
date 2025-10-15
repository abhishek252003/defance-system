# 🛡️ ARGUS Defense Intelligence System

**Real-time Defense and Security Intelligence Gathering System**

ARGUS is an advanced intelligence gathering system designed specifically for monitoring defense, security, and terrorism threats. It automatically scrapes news sources, analyzes content for defense relevance, categorizes threats, and provides real-time visualization through a comprehensive dashboard.

## 🚀 Features

- **Real-time News Scraping**: Automatically collects defense and security news from multiple sources
- **AI-Powered Analysis**: Uses NLP to identify threats, military activities, and security incidents
- **Threat Classification**: Categorizes articles into HIGH, MEDIUM, and LOW threat levels
- **Entity Extraction**: Identifies military units, weapons, organizations, and locations
- **Live Dashboard**: Real-time threat monitoring with interactive visualizations
- **Alert System**: Generates security alerts for high-risk content
- **Keyword Filtering**: Focuses on defense-relevant content using sophisticated keyword matching
- **Database Storage**: Stores processed intelligence for historical analysis

## 📚 Documentation

- [Getting Started Guide](GETTING_STARTED.md) - Quick start instructions
- [Component Overview](COMPONENTS.md) - Detailed information about system components
- [Deployment Options](DEPLOYMENT_OPTIONS.md) - Instructions for various deployment environments
- [Live Monitoring Guide](LIVE_MONITORING_GUIDE.md) - Information about real-time monitoring
- [NLP Setup](NLP_SETUP.md) - Natural Language Processing configuration
- [Streamlit Deployment](STREAMLIT_DEPLOY.md) - Deploying to Streamlit Cloud
- [Railway Deployment](RAILWAY_DEPLOY.md) - Deploying to Railway
- [Render Deployment](RENDER_DEPLOY.md) - Deploying to Render
- [Streamlit Cloud Deployment](STREAMLIT_CLOUD_DEPLOY.md) - Detailed Streamlit Cloud deployment

## 📊 System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌────────────────────┐
│   News Sources  │───▶│  Web Scrapers    │───▶│  Raw Data Storage  │
└─────────────────┘    └──────────────────┘    └────────────────────┘
                              │                         │
                              ▼                         ▼
                    ┌──────────────────┐    ┌────────────────────┐
                    │  NLP Analyzer    │◀──▶│  Defense Database  │
                    └──────────────────┘    └────────────────────┘
                              │                         │
                              ▼                         ▼
                    ┌──────────────────┐    ┌────────────────────┐
                    │ Alert Generator  │    │ Entity Extractor   │
                    └──────────────────┘    └────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Dashboard      │
                    └──────────────────┘
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Quick Setup (Recommended)

For Linux/macOS:
```bash
chmod +x setup.sh
./setup.sh
```

For Windows:
```cmd
setup.bat
```

### Manual Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/argus-defense-intelligence.git
cd argus-defense-intelligence
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download the spaCy English language model:
```bash
python -m spacy download en_core_web_sm
```

## ▶️ Usage

### 1. Initialize the System

First, run the defense scraper to collect news:
```bash
python defense_scraper.py
```

### 2. Process Intelligence

Analyze the collected articles:
```bash
python defense_intelligence.py --batch-process
```

### 3. View the Dashboard

Launch the real-time dashboard:
```bash
streamlit run app.py
```

### Command Line Options

- `python defense_scraper.py` - Run the scraper once
- `python defense_intelligence.py [json_file]` - Process a specific article
- `python defense_intelligence.py --batch-process` - Process all collected articles
- `python defense_intelligence.py --report` - Generate a defense intelligence report
- `streamlit run app.py` - Launch the dashboard

## 📁 Project Structure

```
argus/
├── app.py                 # Streamlit dashboard application
├── defense_scraper.py     # Web scraper for defense news
├── defense_intelligence.py # NLP analysis and threat classification
├── todays_defense_scraper.py # Specialized scraper for today's news
├── defense_intelligence.db # SQLite database for processed intelligence
├── defense_data/          # Directory for raw scraped JSON files
├── requirements.txt       # Python dependencies
├── check_db.py           # Database inspection tool
├── todays_defense_report.py # Daily intelligence reports
├── setup.sh              # Linux/macOS setup script
├── setup.bat             # Windows setup script
├── GETTING_STARTED.md    # Getting started guide
├── COMPONENTS.md         # Component documentation
├── DEPLOYMENT_OPTIONS.md # Deployment options
└── README.md             # This file
```

## 🔍 Threat Classification

The system classifies articles into three threat levels:

### HIGH Threat
- Terrorism-related content
- Imminent security threats
- Military conflicts
- Cyber attacks
- Weapons of mass destruction

### MEDIUM Threat
- Military exercises
- Border security issues
- Defense policy changes
- Security technology developments

### LOW Threat
- General defense news
- Military personnel updates
- Equipment acquisitions
- International defense cooperation

## 🎯 Key Components

### Defense Scraper (`defense_scraper.py`)
- Scrapes defense and security news from multiple Indian and international sources
- Focuses on sources like Times of India, The Hindu, Press Trust of India, etc.
- Saves raw articles as JSON files in the `defense_data/` directory

### Intelligence Analyzer (`defense_intelligence.py`)
- Uses spaCy NLP for entity extraction
- Analyzes content for defense relevance using keyword matching
- Classifies threat levels based on content analysis
- Extracts military units, weapons, organizations, and locations
- Stores processed intelligence in SQLite database

### Dashboard (`app.py`)
- Real-time threat monitoring dashboard built with Streamlit
- Interactive visualizations of threat levels over time
- Detailed article listings with filtering capabilities
- Security alerts display
- Entity analysis charts

## 📊 Dashboard Features

- **Real-time Updates**: Auto-refreshes every 30 seconds
- **Threat Metrics**: Visual display of HIGH, MEDIUM, and LOW threat counts
- **Timeline Charts**: Historical threat level visualization
- **Security Alerts**: Display of recent high-priority alerts
- **Entity Analysis**: Charts showing detected military units and weapons
- **Filtering Options**: Filter by threat level, date range, and article count
- **Detailed Article View**: Expanded view of collected intelligence

## 🔧 Configuration

### Customizing Keywords

The system uses keyword-based filtering in `defense_scraper.py`:
- `HIGH_IMPACT_KEYWORDS`: Keywords that automatically classify an article as HIGH threat
- `GENERAL_KEYWORDS`: Keywords that contribute to threat scoring

### Database Schema

The system uses SQLite with three main tables:
1. `articles`: Stores processed articles with threat levels
2. `entities`: Extracted entities (persons, organizations, locations, etc.)
3. `defense_alerts`: Generated security alerts

## 📈 Example Dashboard Views

### Threat Overview Dashboard
The main dashboard provides a comprehensive overview of current threat levels with real-time metrics and visualizations.

### Detailed Article Analysis
Users can filter articles by threat level and date to focus on specific intelligence requirements.

### Entity Relationship Mapping
The system identifies and tracks key entities such as military units, weapons systems, and organizations.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all news sources that provide public access to defense information
- Built with Python, Streamlit, spaCy, BeautifulSoup, and Plotly
- Inspired by the need for better automated defense intelligence systems

## 📞 Support

For support, please open an issue on the GitHub repository or contact the maintainers.

---
**ARGUS Defense Intelligence System** - Keeping watch on global defense and security threats