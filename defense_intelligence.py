#!/usr/bin/env python3
"""
ARGUS Defense Intelligence Module
Enhanced intelligence gathering specifically designed for defense and security monitoring.
Detects threats, military activities, terrorism, and security incidents.
"""

import spacy
import json
import os
import sys
import sqlite3
import re
from collections import defaultdict
from pathlib import Path
from datetime import datetime

# Defense and security keywords for threat classification
DEFENSE_KEYWORDS = {
    'terrorism': [
        'terrorist', 'terrorism', 'jihad', 'suicide bomb', 'ied', 'isis', 'al qaeda',
        'taliban', 'extremist', 'radical', 'militant', 'insurgent', 'attack plan',
        'threat assessment', 'security alert', 'bomb threat', 'hijack', 'hostage'
    ],
    'military': [
        'military', 'army', 'navy', 'air force', 'defense', 'soldier', 'troop',
        'deployment', 'operation', 'mission', 'combat', 'warfare', 'strategy',
        'intelligence', 'surveillance', 'reconnaissance', 'base', 'camp'
    ],
    'weapons': [
        'weapon', 'missile', 'rocket', 'bomb', 'explosive', 'ammunition', 'gun',
        'rifle', 'artillery', 'tank', 'aircraft', 'drone', 'cyber weapon',
        'nuclear', 'chemical weapon', 'biological weapon', 'drone strike'
    ],
    'cyber_security': [
        'cyber attack', 'hacking', 'malware', 'ransomware', 'data breach',
        'cyber warfare', 'ddos', 'phishing', 'cyber espionage', 'hacker',
        'cybersecurity', 'vulnerability', 'zero day', 'backdoor'
    ],
    'border_security': [
        'border', 'smuggling', 'infiltration', 'illegal crossing', 'surveillance',
        'patrol', 'checkpoint', 'customs', 'immigration', 'refugee crisis'
    ],
    'violence': [
        'violence', 'riot', 'protest', 'unrest', 'conflict', 'clash', 'shooting',
        'stabbing', 'attack', 'assault', 'murder', 'killing', 'death toll'
    ]
}

# High-priority threat indicators
THREAT_INDICATORS = [
    'imminent attack', 'planned attack', 'security threat', 'credible threat',
    'intelligence warning', 'alert level', 'emergency response', 'evacuation',
    'lockdown', 'high alert', 'security breach', 'suspicious activity'
]

# Global variable to store the spaCy model
nlp = None

def load_spacy_model():
    """Load the spaCy English language model."""
    global nlp
    
    if nlp is None:
        try:
            print("Loading spaCy English language model...")
            nlp = spacy.load("en_core_web_sm")
            print("✓ spaCy model loaded successfully")
        except OSError:
            print("✗ Error: spaCy English model not found!")
            print("Please install it with: python -m spacy download en_core_web_sm")
            sys.exit(1)
    
    return nlp

def analyze_defense_relevance(text):
    """
    Analyze text for defense and security relevance.
    
    Args:
        text (str): Article content to analyze
        
    Returns:
        dict: Analysis results with relevance scores and detected categories
    """
    if not text:
        return {
            'is_defense_relevant': False,
            'relevance_score': 0,
            'detected_categories': [],
            'threat_level': 'LOW',
            'key_indicators': []
        }
    
    text_lower = text.lower()
    detected_categories = []
    category_scores = {}
    key_indicators = []
    
    # Check for defense keywords
    for category, keywords in DEFENSE_KEYWORDS.items():
        score = 0
        found_keywords = []
        
        for keyword in keywords:
            count = text_lower.count(keyword.lower())
            if count > 0:
                score += count
                found_keywords.append(keyword)
        
        if score > 0:
            detected_categories.append(category)
            category_scores[category] = score
    
    # Check for high-priority threat indicators
    for indicator in THREAT_INDICATORS:
        if indicator.lower() in text_lower:
            key_indicators.append(indicator)
    
    # Calculate overall relevance score
    total_score = sum(category_scores.values())
    relevance_score = min(total_score * 10, 100)  # Cap at 100
    
    # Determine threat level
    threat_level = 'LOW'
    if key_indicators or 'terrorism' in detected_categories:
        threat_level = 'HIGH'
    elif total_score > 5:
        threat_level = 'MEDIUM'
    
    return {
        'is_defense_relevant': len(detected_categories) > 0,
        'relevance_score': relevance_score,
        'detected_categories': detected_categories,
        'category_scores': category_scores,
        'threat_level': threat_level,
        'key_indicators': key_indicators
    }

def extract_defense_entities(text):
    """
    Extract entities with special focus on defense and security entities.
    
    Args:
        text (str): Article content to process
        
    Returns:
        dict: Enhanced entity extraction with defense classifications
    """
    if not text or not isinstance(text, str):
        return {
            'persons': [],
            'organizations': [],
            'locations': [],
            'military_units': [],
            'weapons': [],
            'defense_analysis': {}
        }
    
    model = load_spacy_model()
    doc = model(text)
    
    # Standard entity extraction
    persons = set()
    organizations = set()
    locations = set()
    military_units = set()
    weapons = set()
    
    # Extract entities
    for ent in doc.ents:
        entity_text = ent.text.strip()
        entity_label = ent.label_
        
        if len(entity_text) < 2:
            continue
        
        # Standard classification
        if entity_label == "PERSON":
            persons.add(entity_text)
        elif entity_label in ["ORG", "CORP"]:
            organizations.add(entity_text)
            
            # Check if it's a military organization
            if any(keyword in entity_text.lower() for keyword in 
                   ['army', 'navy', 'force', 'military', 'defense', 'regiment', 'brigade', 'battalion']):
                military_units.add(entity_text)
                
        elif entity_label in ["GPE", "LOC", "FAC"]:
            locations.add(entity_text)
    
    # Extract weapon mentions using pattern matching
    weapon_patterns = [
        r'\b\w*missile\w*\b', r'\b\w*rocket\w*\b', r'\b\w*bomb\w*\b',
        r'\b\w*gun\w*\b', r'\b\w*rifle\w*\b', r'\b\w*tank\w*\b',
        r'\b\w*aircraft\w*\b', r'\b\w*drone\w*\b'
    ]
    
    for pattern in weapon_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if len(match) > 3:  # Avoid very short matches
                weapons.add(match)
    
    # Perform defense analysis
    defense_analysis = analyze_defense_relevance(text)
    
    result = {
        'persons': sorted(list(persons)),
        'organizations': sorted(list(organizations)),
        'locations': sorted(list(locations)),
        'military_units': sorted(list(military_units)),
        'weapons': sorted(list(weapons)),
        'defense_analysis': defense_analysis
    }
    
    # Print summary
    total_entities = (len(result['persons']) + len(result['organizations']) + 
                     len(result['locations']) + len(result['military_units']) + 
                     len(result['weapons']))
    
    print(f"[ANALYSIS] Defense Intelligence Analysis:")
    print(f"  [STATS] Total entities: {total_entities}")
    print(f"  [PERSONS] Persons: {len(result['persons'])}")
    print(f"  [ORGS] Organizations: {len(result['organizations'])}")
    print(f"  [MILITARY] Military Units: {len(result['military_units'])}")
    print(f"  [LOCATIONS] Locations: {len(result['locations'])}")
    print(f"  [WEAPONS] Weapons: {len(result['weapons'])}")
    print(f"  [THREAT] Threat Level: {defense_analysis['threat_level']}")
    print(f"  [SCORE] Relevance Score: {defense_analysis['relevance_score']}/100")
    
    if defense_analysis['detected_categories']:
        print(f"  [CATEGORIES] Categories: {', '.join(defense_analysis['detected_categories'])}")
    
    if defense_analysis['key_indicators']:
        print(f"  [INDICATORS] Key Indicators: {', '.join(defense_analysis['key_indicators'])}")
    
    return result

def init_defense_db():
    """Initialize enhanced database with defense-specific tables."""
    try:
        conn = sqlite3.connect('defense_intelligence.db')
        cursor = conn.cursor()
        
        # Enhanced articles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                scraped_timestamp TEXT NOT NULL,
                content_length INTEGER,
                word_count INTEGER,
                threat_level TEXT DEFAULT 'LOW',
                relevance_score INTEGER DEFAULT 0,
                detected_categories TEXT,
                key_indicators TEXT
            )
        ''')
        
        # Enhanced entities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                type TEXT NOT NULL,
                entity_category TEXT DEFAULT 'STANDARD',
                FOREIGN KEY (article_id) REFERENCES articles (id)
            )
        ''')
        
        # Defense alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS defense_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER NOT NULL,
                alert_type TEXT NOT NULL,
                alert_level TEXT NOT NULL,
                alert_description TEXT,
                created_timestamp TEXT NOT NULL,
                FOREIGN KEY (article_id) REFERENCES articles (id)
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_articles_threat_level ON articles (threat_level)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_articles_relevance ON articles (relevance_score)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_entities_category ON entities (entity_category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_level ON defense_alerts (alert_level)')
        
        conn.commit()
        print("✓ Defense intelligence database initialized successfully")
        return conn
        
    except sqlite3.Error as e:
        print(f"✗ Database initialization error: {e}")
        return None

def save_defense_intelligence(article_data, entities_data):
    """Save article and enhanced defense intelligence to database."""
    conn = init_defense_db()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        
        # Prepare article data
        title = article_data.get('title', 'Untitled')
        content = article_data.get('content', '')
        url = article_data.get('url', '')
        scraped_timestamp = article_data.get('scraped_timestamp', datetime.now().isoformat())
        content_length = len(content)
        word_count = len(content.split()) if content else 0
        
        # Defense analysis data
        defense_analysis = entities_data.get('defense_analysis', {})
        threat_level = defense_analysis.get('threat_level', 'LOW')
        relevance_score = defense_analysis.get('relevance_score', 0)
        detected_categories = ','.join(defense_analysis.get('detected_categories', []))
        key_indicators = ','.join(defense_analysis.get('key_indicators', []))
        
        # Insert article
        try:
            cursor.execute('''
                INSERT INTO articles (title, content, url, scraped_timestamp, 
                                    content_length, word_count, threat_level, 
                                    relevance_score, detected_categories, key_indicators)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, content, url, scraped_timestamp, content_length, word_count,
                  threat_level, relevance_score, detected_categories, key_indicators))
            
            article_id = cursor.lastrowid
            print(f"✓ Article saved with ID: {article_id}")
            
        except sqlite3.IntegrityError:
            cursor.execute('SELECT id FROM articles WHERE url = ?', (url,))
            result = cursor.fetchone()
            if result:
                article_id = result[0]
                print(f"Article already exists with ID: {article_id}. Updating...")
                cursor.execute('DELETE FROM entities WHERE article_id = ?', (article_id,))
                cursor.execute('DELETE FROM defense_alerts WHERE article_id = ?', (article_id,))
            else:
                print("✗ Failed to handle duplicate URL")
                return None
        
        # Insert entities with categories
        entity_count = 0
        
        # Standard entities
        for person in entities_data.get('persons', []):
            cursor.execute('''
                INSERT INTO entities (article_id, text, type, entity_category)
                VALUES (?, ?, ?, ?)
            ''', (article_id, person, 'PERSON', 'STANDARD'))
            entity_count += 1
        
        for org in entities_data.get('organizations', []):
            cursor.execute('''
                INSERT INTO entities (article_id, text, type, entity_category)
                VALUES (?, ?, ?, ?)
            ''', (article_id, org, 'ORG', 'STANDARD'))
            entity_count += 1
        
        for loc in entities_data.get('locations', []):
            cursor.execute('''
                INSERT INTO entities (article_id, text, type, entity_category)
                VALUES (?, ?, ?, ?)
            ''', (article_id, loc, 'LOCATION', 'STANDARD'))
            entity_count += 1
        
        # Defense-specific entities
        for unit in entities_data.get('military_units', []):
            cursor.execute('''
                INSERT INTO entities (article_id, text, type, entity_category)
                VALUES (?, ?, ?, ?)
            ''', (article_id, unit, 'MILITARY_UNIT', 'DEFENSE'))
            entity_count += 1
        
        for weapon in entities_data.get('weapons', []):
            cursor.execute('''
                INSERT INTO entities (article_id, text, type, entity_category)
                VALUES (?, ?, ?, ?)
            ''', (article_id, weapon, 'WEAPON', 'DEFENSE'))
            entity_count += 1
        
        # Create defense alerts for high-threat articles
        if threat_level in ['HIGH', 'MEDIUM']:
            alert_description = f"Article contains {threat_level.lower()}-level security content"
            if key_indicators:
                alert_description += f". Key indicators: {', '.join(defense_analysis.get('key_indicators', []))}"
            
            cursor.execute('''
                INSERT INTO defense_alerts (article_id, alert_type, alert_level, 
                                          alert_description, created_timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (article_id, 'THREAT_DETECTION', threat_level, alert_description, 
                  datetime.now().isoformat()))
        
        conn.commit()
        print(f"✓ Saved {entity_count} entities to defense intelligence database")
        
        return article_id
        
    except sqlite3.Error as e:
        print(f"✗ Database save error: {e}")
        conn.rollback()
        return None
        
    finally:
        conn.close()

def generate_defense_report():
    """Generate a comprehensive defense intelligence report."""
    conn = init_defense_db()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        print("\n" + "🛡️" * 20)
        print("   DEFENSE INTELLIGENCE REPORT")
        print("[DEFENSE]" * 10)
        
        # High-threat articles
        cursor.execute('''
            SELECT COUNT(*) FROM articles WHERE threat_level = 'HIGH'
        ''')
        high_threat_count = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COUNT(*) FROM articles WHERE threat_level = 'MEDIUM'
        ''')
        medium_threat_count = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COUNT(*) FROM articles WHERE threat_level = 'LOW'
        ''')
        low_threat_count = cursor.fetchone()[0]
        
        print(f"\n[THREAT-SUMMARY] THREAT LEVEL SUMMARY:")
        print(f"   [HIGH] HIGH:   {high_threat_count} articles")
        print(f"   [MEDIUM] MEDIUM: {medium_threat_count} articles")
        print(f"   [LOW] LOW:    {low_threat_count} articles")
        
        # Recent high-threat articles
        if high_threat_count > 0:
            cursor.execute('''
                SELECT title, url, threat_level, key_indicators, scraped_timestamp
                FROM articles 
                WHERE threat_level = 'HIGH'
                ORDER BY scraped_timestamp DESC
                LIMIT 5
            ''')
            
            high_threat_articles = cursor.fetchall()
            print(f"\n[HIGH-THREATS] RECENT HIGH-THREAT ARTICLES:")
            
            for i, (title, url, threat_level, indicators, timestamp) in enumerate(high_threat_articles, 1):
                print(f"\n   {i}. {title}")
                print(f"      [URL] {url}")
                print(f"      [TIME] {timestamp}")
                if indicators:
                    print(f"      [INDICATORS] Indicators: {indicators}")
        
        # Defense entity statistics
        cursor.execute('''
            SELECT type, COUNT(*) 
            FROM entities 
            WHERE entity_category = 'DEFENSE'
            GROUP BY type
        ''')
        defense_entities = cursor.fetchall()
        
        if defense_entities:
            print(f"\n[DEFENSE-ENTITIES] DEFENSE ENTITIES DETECTED:")
            for entity_type, count in defense_entities:
                print(f"   {entity_type}: {count}")
        
        # Recent alerts
        cursor.execute('''
            SELECT COUNT(*) FROM defense_alerts 
            WHERE created_timestamp >= datetime('now', '-24 hours')
        ''')
        recent_alerts = cursor.fetchone()[0]
        
        print(f"\n[ALERTS] ALERTS (Last 24 hours): {recent_alerts}")
        
        print("\n" + "[DEFENSE]" * 10)
        
    except sqlite3.Error as e:
        print(f"Error generating report: {e}")
    finally:
        conn.close()

def process_all_defense_files():
    """Process all JSON files in defense_data directory."""
    defense_dir = Path("defense_data")
    
    if not defense_dir.exists():
        print("[X] defense_data directory not found.")
        return False
    
    # Get all JSON files except summaries
    json_files = [f for f in defense_dir.glob("*.json") if 'summary' not in f.name]
    
    if not json_files:
        print("[X] No article JSON files found in defense_data directory.")
        return False
    
    # Initialize database
    init_defense_db()
    
    processed_count = 0
    error_count = 0
    
    print(f"[PROCESSING] Processing {len(json_files)} defense articles...")
    print("=" * 60)
    
    for json_file in json_files:
        try:
            print(f"[FILE] Processing: {json_file.name}")
            
            # Load article data
            with open(json_file, 'r', encoding='utf-8') as f:
                article_data = json.load(f)
            
            content = article_data.get('content', '')
            if not content or len(content) < 100:
                print(f"[WARNING] Skipping {json_file.name}: insufficient content")
                continue
            
            # Analyze content
            entities_data = extract_defense_entities(content)
            
            # Store in database
            save_defense_intelligence(article_data, entities_data)
            processed_count += 1
            
        except Exception as e:
            print(f"[ERROR] Error processing {json_file.name}: {e}")
            error_count += 1
            continue
    
    print(f"\n[SUCCESS] Processing complete!")
    print(f"[STATS] Successfully processed: {processed_count} articles")
    if error_count > 0:
        print(f"[WARNING] Errors encountered: {error_count} files")
    
    return processed_count > 0
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '--report':
            generate_defense_report()
            sys.exit(0)
        elif sys.argv[1] == '--batch-process':
            success = process_all_defense_files()
            if success:
                generate_defense_report()
            sys.exit(0)
        
        json_file = sys.argv[1]
        if not os.path.exists(json_file):
            print(f"File not found: {json_file}")
            sys.exit(1)
    else:
        # Find the latest scraped file
        scraped_dir = "defense_data"  # Updated to use defense_data directory
        if os.path.exists(scraped_dir):
            json_files = list(Path(scraped_dir).glob("*.json"))
            # Filter out summary files to get individual articles
            article_files = [f for f in json_files if 'summary' not in f.name]
            if article_files:
                json_file = str(max(article_files, key=lambda f: f.stat().st_mtime))
            else:
                print("No article JSON files found in defense_data directory.")
                print("Usage: python defense_intelligence.py [json_file_path]")
                print("   or: python defense_intelligence.py --report")
                print("   or: python defense_intelligence.py --batch-process")
                sys.exit(1)
        else:
            print("defense_data directory not found.")
            print("Please run the defense scraper first or provide a JSON file path.")
            sys.exit(1)
    
    print(f"[ANALYZING] Analyzing: {json_file}")
    
    # Load and process the article
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            article_data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)
    
    content = article_data.get('content', '')
    title = article_data.get('title', 'Unknown Title')
    
    if not content:
        print("No content found in the JSON file.")
        sys.exit(1)
    
    print(f"\n[ARTICLE] Article: {title}")
    print(f"[LENGTH] Content length: {len(content)} characters")
    print("\n[ANALYSIS] Performing defense intelligence analysis...")
    
    # Extract defense intelligence
    entities = extract_defense_entities(content)
    
    # Save to defense database
    print("\n[SAVING] Saving to defense intelligence database...")
    article_id = save_defense_intelligence(article_data, entities)
    
    if article_id:
        print(f"✓ Defense intelligence saved with ID: {article_id}")
        
        # Generate mini-report for this article
        defense_analysis = entities['defense_analysis']
        if defense_analysis['is_defense_relevant']:
            print(f"\n[RELEVANCE] DEFENSE RELEVANCE CONFIRMED")
            print(f"   [SCORE] Relevance Score: {defense_analysis['relevance_score']}/100")
            print(f"   [THREAT] Threat Level: {defense_analysis['threat_level']}")
            print(f"   [CATEGORIES] Categories: {', '.join(defense_analysis['detected_categories'])}")
            
            if defense_analysis['key_indicators']:
                print(f"   [INDICATORS] Key Indicators:")
                for indicator in defense_analysis['key_indicators']:
                    print(f"      • {indicator}")
        else:
            print(f"\n[ASSESSMENT] Article assessed as low defense relevance")
    else:
        print("\n✗ Failed to save to defense database")
    
    print(f"\n[TIP] Tip: Run 'python defense_intelligence.py --report' for a comprehensive defense report")