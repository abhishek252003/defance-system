#!/usr/bin/env python3
"""
Quick Defense Data Processor
Processes JSON files directly into database without heavy NLP requirements.
"""

import json
import sqlite3
import os
from pathlib import Path
from datetime import datetime
import re

def init_defense_db():
    """Initialize defense database."""
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
        
        conn.commit()
        print("✓ Defense intelligence database initialized successfully")
        return conn
        
    except sqlite3.Error as e:
        print(f"✗ Database initialization error: {e}")
        return None

def analyze_text_simple(text):
    """Simple text analysis without NLP requirements.""" 
    if not text:
        return {
            'threat_level': 'LOW',
            'relevance_score': 0,
            'detected_categories': [],
            'key_indicators': []
        }
    
    text_lower = text.lower()
    
    # Defense keywords for quick analysis
    defense_keywords = {
        'military': ['military', 'army', 'navy', 'defense', 'soldier', 'combat', 'operation'],
        'weapons': ['weapon', 'missile', 'bomb', 'gun', 'aircraft', 'drone'],
        'security': ['security', 'threat', 'attack', 'terrorism', 'alert', 'surveillance'],
        'cyber': ['cyber', 'hacking', 'malware', 'breach', 'ransomware']
    }
    
    high_threat_words = ['attack', 'threat', 'terrorism', 'bomb', 'missile', 'alert', 'emergency']
    
    detected_categories = []
    relevance_score = 0
    key_indicators = []
    
    # Check categories
    for category, keywords in defense_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                if category not in detected_categories:
                    detected_categories.append(category)
                relevance_score += 5
    
    # Check for high threat indicators
    for threat_word in high_threat_words:
        if threat_word in text_lower:
            key_indicators.append(threat_word)
            relevance_score += 10
    
    # Determine threat level
    threat_level = 'LOW'
    if key_indicators or relevance_score > 30:
        threat_level = 'HIGH'
    elif relevance_score > 15:
        threat_level = 'MEDIUM'
    
    return {
        'threat_level': threat_level,
        'relevance_score': min(relevance_score, 100),
        'detected_categories': detected_categories,
        'key_indicators': key_indicators
    }

def process_article_quick(article_data):
    """Quickly process article data."""
    content = article_data.get('content', '')
    analysis = analyze_text_simple(content)
    
    # Save to database
    conn = init_defense_db()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        
        # Prepare data
        title = article_data.get('title', 'Untitled')
        url = article_data.get('url', '')
        scraped_timestamp = article_data.get('scraped_timestamp', datetime.now().isoformat())
        content_length = len(content)
        word_count = len(content.split()) if content else 0
        
        # Analysis data
        threat_level = analysis['threat_level']
        relevance_score = analysis['relevance_score']
        detected_categories = ','.join(analysis['detected_categories'])
        key_indicators = ','.join(analysis['key_indicators'])
        
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
            conn.commit()
            return article_id
            
        except sqlite3.IntegrityError:
            # Article already exists, skip
            return None
            
    except sqlite3.Error as e:
        print(f"✗ Database error: {e}")
        return None
        
    finally:
        conn.close()

def process_all_quick():
    """Quickly process all JSON files."""
    defense_dir = Path("defense_data")
    
    if not defense_dir.exists():
        print("[ERROR] defense_data directory not found.")
        return False
    
    # Get all JSON files except summaries
    json_files = [f for f in defense_dir.glob("*.json") if 'summary' not in f.name]
    
    if not json_files:
        print("[ERROR] No article JSON files found.")
        return False
    
    processed_count = 0
    skipped_count = 0
    
    print(f"[PROCESSING] Quick processing {len(json_files)} defense articles...")
    print("=" * 60)
    
    for i, json_file in enumerate(json_files):
        if i % 100 == 0:
            print(f"[PROGRESS] Progress: {i}/{len(json_files)} files processed")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                article_data = json.load(f)
            
            content = article_data.get('content', '')
            if not content or len(content) < 50:
                skipped_count += 1
                continue
            
            article_id = process_article_quick(article_data)
            if article_id:
                processed_count += 1
            else:
                skipped_count += 1
                
        except Exception as e:
            print(f"[ERROR] Error processing {json_file.name}: {e}")
            skipped_count += 1
            continue
    
    print(f"\n[SUCCESS] Quick processing complete!")
    print(f"[STATS] Successfully processed: {processed_count} articles")
    print(f"[WARNING] Skipped: {skipped_count} files")
    
    # Show database stats
    conn = sqlite3.connect('defense_intelligence.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM articles")
    total_articles = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM articles WHERE threat_level = 'HIGH'")
    high_threats = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM articles WHERE threat_level = 'MEDIUM'") 
    medium_threats = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM articles WHERE datetime(scraped_timestamp) >= datetime('now', '-24 hours')")
    recent_articles = cursor.fetchone()[0]
    
    print(f"\n[DATABASE] DATABASE SUMMARY:")
    print(f"   [ARTICLES] Total articles: {total_articles}")
    print(f"   [HIGH] High threats: {high_threats}")
    print(f"   [MEDIUM] Medium threats: {medium_threats}")
    print(f"   [RECENT] Last 24 hours: {recent_articles}")
    
    conn.close()
    return processed_count > 0

if __name__ == "__main__":
    process_all_quick()