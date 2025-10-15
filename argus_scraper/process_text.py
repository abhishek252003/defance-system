#!/usr/bin/env python3
"""
ARGUS Text Processing Module
This module provides Natural Language Processing capabilities for extracting entities from article text.
"""

import spacy
import json
import os
import sys
import sqlite3
from collections import defaultdict
from pathlib import Path
from datetime import datetime

# Global variable to store the spaCy model
nlp = None

def load_spacy_model():
    """
    Load the spaCy English language model.
    
    Returns:
        spacy.lang.en.English: Loaded spaCy model
    """
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

def extract_entities(text):
    """
    Extract named entities from the given text using spaCy NLP.
    
    Args:
        text (str): The article content to process
        
    Returns:
        dict: Dictionary with three keys (persons, organizations, locations)
              Each key contains a list of unique entities found
    """
    
    if not text or not isinstance(text, str):
        return {
            'persons': [],
            'organizations': [],
            'locations': []
        }
    
    # Load the model if not already loaded
    model = load_spacy_model()
    
    try:
        # Process the text with spaCy
        doc = model(text)
        
        # Use sets to avoid duplicates, then convert to lists
        persons = set()
        organizations = set()
        locations = set()
        
        # Extract entities and classify them
        for ent in doc.ents:
            entity_text = ent.text.strip()
            entity_label = ent.label_
            
            # Skip very short entities (likely noise)
            if len(entity_text) < 2:
                continue
                
            # Classify entities by type
            if entity_label == "PERSON":
                persons.add(entity_text)
            elif entity_label in ["ORG", "CORP"]:
                organizations.add(entity_text)
            elif entity_label in ["GPE", "LOC", "FAC"]:
                # GPE: Geopolitical entities (countries, cities, states)
                # LOC: Locations (mountain ranges, bodies of water)
                # FAC: Facilities (airports, highways, bridges)
                locations.add(entity_text)
        
        # Convert sets to sorted lists for consistent output
        result = {
            'persons': sorted(list(persons)),
            'organizations': sorted(list(organizations)),
            'locations': sorted(list(locations))
        }
        
        # Print summary
        total_entities = len(result['persons']) + len(result['organizations']) + len(result['locations'])
        print(f"Extracted {total_entities} unique entities:")
        print(f"  - Persons: {len(result['persons'])}")
        print(f"  - Organizations: {len(result['organizations'])}")
        print(f"  - Locations: {len(result['locations'])}")
        
        return result
        
    except Exception as e:
        print(f"Error processing text: {e}")
        return {
            'persons': [],
            'organizations': [],
            'locations': []
        }

def get_all_entities_detailed(text):
    """
    Extract all entities with additional details for debugging/analysis.
    
    Args:
        text (str): The article content to process
        
    Returns:
        list: List of dictionaries with entity details
    """
    
    model = load_spacy_model()
    doc = model(text)
    
    entities = []
    for ent in doc.ents:
        entities.append({
            'text': ent.text,
            'label': ent.label_,
            'description': spacy.explain(ent.label_),
            'start': ent.start_char,
            'end': ent.end_char
        })
    
    return entities

def init_db():
    """
    Initialize the SQLite database with required tables.
    
    Returns:
        sqlite3.Connection: Database connection object
    """
    
    try:
        # Connect to the database (creates file if it doesn't exist)
        conn = sqlite3.connect('intelligence.db')
        cursor = conn.cursor()
        
        # Create articles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                scraped_timestamp TEXT NOT NULL,
                content_length INTEGER,
                word_count INTEGER
            )
        ''')
        
        # Create entities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                type TEXT NOT NULL,
                FOREIGN KEY (article_id) REFERENCES articles (id)
            )
        ''')
        
        # Create index for better performance
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_entities_article_id 
            ON entities (article_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_entities_type 
            ON entities (type)
        ''')
        
        conn.commit()
        print("✓ Database initialized successfully")
        return conn
        
    except sqlite3.Error as e:
        print(f"✗ Database initialization error: {e}")
        return None

def save_to_db(article_data, entities_data):
    """
    Save article and entity data to the SQLite database.
    
    Args:
        article_data (dict): Article data from scrape_article()
        entities_data (dict): Entity data from extract_entities()
        
    Returns:
        int: Article ID if successful, None if failed
    """
    
    conn = init_db()
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
        
        # Insert article (handle duplicate URLs)
        try:
            cursor.execute('''
                INSERT INTO articles (title, content, url, scraped_timestamp, content_length, word_count)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, content, url, scraped_timestamp, content_length, word_count))
            
            article_id = cursor.lastrowid
            print(f"✓ Article saved with ID: {article_id}")
            
        except sqlite3.IntegrityError:
            # URL already exists, get the existing article ID
            cursor.execute('SELECT id FROM articles WHERE url = ?', (url,))
            result = cursor.fetchone()
            if result:
                article_id = result[0]
                print(f"Article already exists with ID: {article_id}. Updating entities...")
                # Delete existing entities for this article
                cursor.execute('DELETE FROM entities WHERE article_id = ?', (article_id,))
            else:
                print("✗ Failed to handle duplicate URL")
                return None
        
        # Insert entities
        entity_count = 0
        
        # Insert persons
        for person in entities_data.get('persons', []):
            cursor.execute('''
                INSERT INTO entities (article_id, text, type)
                VALUES (?, ?, ?)
            ''', (article_id, person, 'PERSON'))
            entity_count += 1
        
        # Insert organizations
        for org in entities_data.get('organizations', []):
            cursor.execute('''
                INSERT INTO entities (article_id, text, type)
                VALUES (?, ?, ?)
            ''', (article_id, org, 'ORG'))
            entity_count += 1
        
        # Insert locations
        for loc in entities_data.get('locations', []):
            cursor.execute('''
                INSERT INTO entities (article_id, text, type)
                VALUES (?, ?, ?)
            ''', (article_id, loc, 'LOCATION'))
            entity_count += 1
        
        conn.commit()
        print(f"✓ Saved {entity_count} entities to database")
        
        return article_id
        
    except sqlite3.Error as e:
        print(f"✗ Database save error: {e}")
        conn.rollback()
        return None
        
    finally:
        conn.close()

def get_db_stats():
    """
    Get basic statistics from the database.
    
    Returns:
        dict: Dictionary containing database statistics
    """
    
    conn = init_db()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        
        # Get article count
        cursor.execute('SELECT COUNT(*) FROM articles')
        article_count = cursor.fetchone()[0]
        
        # Get entity count by type
        cursor.execute('''
            SELECT type, COUNT(*) 
            FROM entities 
            GROUP BY type
        ''')
        entity_stats = dict(cursor.fetchall())
        
        # Get total entity count
        cursor.execute('SELECT COUNT(*) FROM entities')
        total_entities = cursor.fetchone()[0]
        
        return {
            'articles': article_count,
            'total_entities': total_entities,
            'entity_breakdown': entity_stats
        }
        
    except sqlite3.Error as e:
        print(f"Database stats error: {e}")
        return None
        
    finally:
        conn.close()

def load_json_file(filepath):
    """
    Load and return the content of a JSON file.
    
    Args:
        filepath (str): Path to the JSON file
        
    Returns:
        dict: Loaded JSON data or None if error
    """
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading JSON file {filepath}: {e}")
        return None

def find_latest_scraped_file():
    """
    Find the most recently created JSON file in the scraped_data directory.
    
    Returns:
        str: Path to the latest JSON file or None if not found
    """
    
    scraped_dir = "scraped_data"
    
    if not os.path.exists(scraped_dir):
        print(f"Directory {scraped_dir} not found.")
        return None
    
    json_files = list(Path(scraped_dir).glob("*.json"))
    
    if not json_files:
        print(f"No JSON files found in {scraped_dir}")
        return None
    
    # Sort by modification time and return the latest
    latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
    return str(latest_file)

if __name__ == "__main__":
    print("ARGUS Text Processing Test")
    print("=" * 50)
    
    # Test the entity extraction
    if len(sys.argv) > 1:
        # If file path provided as command line argument
        json_file = sys.argv[1]
        if not os.path.exists(json_file):
            print(f"File not found: {json_file}")
            sys.exit(1)
    else:
        # Find the latest scraped file
        json_file = find_latest_scraped_file()
        if not json_file:
            print("No scraped JSON files found.")
            print("Please run the scraper first or provide a JSON file path.")
            print("Usage: python process_text.py [json_file_path]")
            sys.exit(1)
    
    print(f"Processing file: {json_file}")
    
    # Load the JSON data
    article_data = load_json_file(json_file)
    if not article_data:
        print("Failed to load article data.")
        sys.exit(1)
    
    # Extract article content
    content = article_data.get('content', '')
    title = article_data.get('title', 'Unknown Title')
    
    if not content:
        print("No content found in the JSON file.")
        sys.exit(1)
    
    print(f"\nArticle: {title}")
    print(f"Content length: {len(content)} characters")
    print("\nExtracting entities...")
    
    # Extract entities
    entities = extract_entities(content)
    
    # Save to database
    print("\nStep 3: Saving to database...")
    article_id = save_to_db(article_data, entities)
    
    if article_id:
        print(f"\n✓ Article and entities saved to database with ID: {article_id}")
        
        # Show database statistics
        stats = get_db_stats()
        if stats:
            print("\nDatabase Statistics:")
            print(f"  Total articles: {stats['articles']}")
            print(f"  Total entities: {stats['total_entities']}")
            print("  Entity breakdown:")
            for entity_type, count in stats['entity_breakdown'].items():
                print(f"    {entity_type}: {count}")
    else:
        print("\n✗ Failed to save to database")
    
    # Display results
    print("\n" + "=" * 50)
    print("EXTRACTED ENTITIES")
    print("=" * 50)
    
    if entities['persons']:
        print(f"\n👤 PERSONS ({len(entities['persons'])}):")
        for person in entities['persons']:
            print(f"  • {person}")
    
    if entities['organizations']:
        print(f"\n🏢 ORGANIZATIONS ({len(entities['organizations'])}):")
        for org in entities['organizations']:
            print(f"  • {org}")
    
    if entities['locations']:
        print(f"\n📍 LOCATIONS ({len(entities['locations'])}):")
        for loc in entities['locations']:
            print(f"  • {loc}")
    
    if not any(entities.values()):
        print("\nNo entities found in the article.")
    
    # Show detailed analysis if requested
    if '--detailed' in sys.argv:
        print("\n" + "=" * 50)
        print("DETAILED ENTITY ANALYSIS")
        print("=" * 50)
        detailed_entities = get_all_entities_detailed(content)
        for ent in detailed_entities:
            print(f"'{ent['text']}' -> {ent['label']} ({ent['description']})")