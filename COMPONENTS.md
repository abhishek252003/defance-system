# ARGUS Defense Intelligence System Components

## Core Components

### 1. Defense Scraper (`defense_scraper.py`)

The defense scraper is responsible for collecting news articles from various defense and security sources.

**Key Features:**
- Multi-source scraping from Indian and international defense news sites
- Concurrent scraping using threading for improved performance
- Keyword-based filtering to focus on defense-relevant content
- JSON storage of raw articles in the `defense_data/` directory

**Configuration:**
- `HIGH_IMPACT_KEYWORDS`: Keywords that automatically classify an article as HIGH threat
- `GENERAL_KEYWORDS`: Keywords that contribute to threat scoring
- `DEFENSE_SOURCES`: List of news sources to scrape

**Usage:**
```bash
python defense_scraper.py
```

### 2. Defense Intelligence Analyzer (`defense_intelligence.py`)

The intelligence analyzer processes collected articles using NLP techniques to extract meaningful intelligence.

**Key Features:**
- spaCy-based entity extraction (persons, organizations, locations, military units, weapons)
- Threat classification into HIGH, MEDIUM, and LOW levels
- Relevance scoring based on keyword frequency and context
- Database storage of processed intelligence
- Alert generation for high-threat content

**Usage:**
```bash
# Process a single article
python defense_intelligence.py path/to/article.json

# Process all articles
python defense_intelligence.py --batch-process

# Generate a report
python defense_intelligence.py --report
```

### 3. Dashboard (`app.py`)

The Streamlit-based dashboard provides real-time visualization of defense intelligence.

**Key Features:**
- Real-time threat metrics with auto-refresh
- Interactive charts for threat level distribution
- Timeline visualization of threat trends
- Security alerts display
- Entity analysis charts
- Filtering by threat level and date
- Detailed article listing with content previews

**Usage:**
```bash
streamlit run app.py
```

### 4. Today's Defense Scraper (`todays_defense_scraper.py`)

A specialized scraper focused on collecting only today's defense news.

**Key Features:**
- Date-based filtering to collect only current news
- Enhanced keyword filtering with tiered approach
- Optimized for daily intelligence gathering
- Integration with the main defense intelligence system

**Usage:**
```bash
python todays_defense_scraper.py
```

### 5. Database (`defense_intelligence.db`)

SQLite database storing all processed intelligence.

**Schema:**
1. `articles`: Processed articles with threat classification
   - id, title, content, url, scraped_timestamp, content_length, word_count
   - threat_level, relevance_score, detected_categories, key_indicators

2. `entities`: Extracted entities from articles
   - id, article_id, text, type, entity_category

3. `defense_alerts`: Generated security alerts
   - id, article_id, alert_type, alert_level, alert_description, created_timestamp

## Supporting Components

### Database Inspection Tool (`check_db.py`)

Simple script to check database contents and statistics.

**Usage:**
```bash
python check_db.py
```

### Daily Report Generator (`todays_defense_report.py`)

Generates comprehensive reports of today's defense intelligence.

**Usage:**
```bash
python todays_defense_report.py
```

### Setup Scripts (`setup.sh`, `setup.bat`)

Automated setup scripts for Linux/macOS and Windows respectively.

## Data Flow

1. **Scraping**: `defense_scraper.py` collects articles from news sources
2. **Storage**: Raw articles saved as JSON files in `defense_data/`
3. **Analysis**: `defense_intelligence.py` processes articles and extracts intelligence
4. **Database**: Processed intelligence stored in `defense_intelligence.db`
5. **Visualization**: `app.py` displays intelligence through the dashboard
6. **Alerting**: High-threat articles generate alerts in the dashboard

## Customization

### Adding News Sources

Edit `defense_scraper.py` to add new sources to the `DEFENSE_SOURCES` list.

### Modifying Keywords

Adjust `HIGH_IMPACT_KEYWORDS` and `GENERAL_KEYWORDS` in `defense_scraper.py` to customize filtering.

### Adjusting Threat Classification

Modify the threat classification logic in `defense_intelligence.py`:
- `DEFENSE_KEYWORDS`: Categories and keywords for defense relevance
- `THREAT_INDICATORS`: High-priority threat indicators
- `analyze_defense_relevance()`: Main function for threat classification

## Performance Considerations

- The system uses concurrent scraping for improved performance
- Database indexes are created for efficient querying
- The dashboard auto-refreshes every 30 seconds to balance real-time updates with performance
- Entity extraction uses spaCy's efficient NLP models