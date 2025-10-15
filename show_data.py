#!/usr/bin/env python3
"""
ARGUS Defense Data Summary Generator
Simple script to view all collected defense intelligence data.
"""

import json
import os
from pathlib import Path
from datetime import datetime

def load_and_display_defense_data():
    """Load and display all defense data in a simple format."""
    defense_data_dir = "defense_data"
    
    if not os.path.exists(defense_data_dir):
        print("❌ No defense_data directory found.")
        print("Please run: python defense_scraper.py")
        return
    
    print("🛡️ ARGUS Defense Intelligence Data Summary")
    print("=" * 60)
    
    articles = []
    summary_data = None
    
    # Load all JSON files
    for file_path in Path(defense_data_dir).glob("*.json"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Check if it's a summary file
                if 'total_articles' in data and 'articles' in data:
                    summary_data = data
                else:
                    # Regular article data
                    articles.append(data)
                    
        except Exception as e:
            print(f"Warning: Error loading {file_path}: {e}")
    
    # Display summary
    if summary_data:
        print(f"\n📊 COLLECTION SUMMARY:")
        print(f"   Total Articles Scraped: {summary_data.get('total_articles', 0)}")
        print(f"   Scraping Timestamp: {summary_data.get('scraping_timestamp', 'Unknown')}")
        print(f"   Sources Monitored:")
        for source in summary_data.get('sources_scraped', []):
            print(f"     • {source}")
    
    # Categorize articles
    high_priority = []
    medium_priority = []
    regular = []
    
    defense_keywords = {
        'high': ['nuclear', 'missile', 'agni', 'terrorism', 'attack', 'weapon', 'army', 'navy', 'air force', 'border', 'security'],
        'medium': ['defense', 'defence', 'military', 'intelligence', 'surveillance', 'police', 'government']
    }
    
    for article in articles:
        title = article.get('title', '').lower()
        content = article.get('content', '').lower()
        text = title + ' ' + content
        
        # Count keywords
        high_count = sum(1 for keyword in defense_keywords['high'] if keyword in text)
        medium_count = sum(1 for keyword in defense_keywords['medium'] if keyword in text)
        
        if high_count >= 2:
            high_priority.append(article)
        elif high_count >= 1 or medium_count >= 2:
            medium_priority.append(article)
        else:
            regular.append(article)
    
    print(f"\n📈 PRIORITY BREAKDOWN:")
    print(f"   🔴 High Priority: {len(high_priority)} articles")
    print(f"   🟡 Medium Priority: {len(medium_priority)} articles")
    print(f"   🟢 Regular: {len(regular)} articles")
    print(f"   📰 Total Loaded: {len(articles)} articles")
    
    # Display top high priority articles
    if high_priority:
        print(f"\n🚨 TOP HIGH PRIORITY DEFENSE INTELLIGENCE:")
        print("-" * 60)
        
        for i, article in enumerate(high_priority[:10], 1):  # Top 10
            title = article.get('title', 'Untitled')
            source = article.get('source_domain', 'Unknown Source')
            url = article.get('url', '#')
            word_count = article.get('word_count', 0)
            timestamp = article.get('scraped_timestamp', '')
            
            print(f"\n{i}. 🔴 {title}")
            print(f"    📍 Source: {source}")
            print(f"    📏 Words: {word_count}")
            print(f"    ⏰ Scraped: {timestamp}")
            print(f"    🔗 URL: {url}")
            
            # Content preview
            content = article.get('content', '')
            if content:
                preview = content[:200] + "..." if len(content) > 200 else content
                print(f"    📄 Preview: {preview}")
    
    # Display source breakdown
    source_stats = {}
    for article in articles:
        source = article.get('source_domain', 'Unknown')
        if source not in source_stats:
            source_stats[source] = {'count': 0, 'words': 0}
        source_stats[source]['count'] += 1
        source_stats[source]['words'] += article.get('word_count', 0)
    
    if source_stats:
        print(f"\n📊 SOURCES BREAKDOWN:")
        print("-" * 60)
        for source, stats in sorted(source_stats.items(), key=lambda x: x[1]['count'], reverse=True):
            print(f"📺 {source}")
            print(f"   Articles: {stats['count']}")
            print(f"   Total Words: {stats['words']:,}")
            print()
    
    # Display medium priority articles
    if medium_priority:
        print(f"\n🟡 MEDIUM PRIORITY ARTICLES (Top 5):")
        print("-" * 60)
        
        for i, article in enumerate(medium_priority[:5], 1):
            title = article.get('title', 'Untitled')
            source = article.get('source_domain', 'Unknown Source')
            print(f"{i}. 🟡 {title}")
            print(f"    📍 {source}")
            print()
    
    # Instructions
    print(f"\n💡 NEXT ACTIONS:")
    print("-" * 60)
    print("1. 🧠 Run AI Analysis:")
    print("   python defense_intelligence.py")
    print()
    print("2. 📊 Generate Full Report:")
    print("   python defense_intelligence.py --report")
    print()
    print("3. 🔄 Continue Monitoring:")
    print("   python defense_scraper.py --monitor")
    print()
    print("4. 🌐 View in Web Dashboard:")
    print("   streamlit run dashboard.py")

if __name__ == "__main__":
    load_and_display_defense_data()