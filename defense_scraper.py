#!/usr/bin/env python3
"""
ARGUS Defense News Scraper
Specialized scraper for defense, security, and terrorism-related news sources.
Monitors multiple Indian and international defense news websites.
"""

import requests
from bs4 import BeautifulSoup
import time
import json
import os
from datetime import datetime
import concurrent.futures
import threading
from urllib.parse import urljoin, urlparse
import re

# Indian Defense and Security News Sources
INDIAN_DEFENSE_SOURCES = {
    'Indian Defence News': {
        'base_url': 'https://www.indiandefencenews.in/',
        'sections': [
            'defence',
            'security',
            'terrorism',
            'border-security'
        ]
    },
    'Financial Express Defence': {
        'base_url': 'https://www.financialexpress.com/',
        'sections': [
            'defence',
            'defence/security'
        ]
    },
    'Economic Times Defence': {
        'base_url': 'https://economictimes.indiatimes.com/',
        'sections': [
            'news/defence',
            'news/politics-and-nation'
        ]
    },
    'Hindustan Times India News': {
        'base_url': 'https://www.hindustantimes.com/',
        'sections': [
            'india-news',
            'india-news/terrorism',
            'world-news'
        ]
    },
    'Times of India India': {
        'base_url': 'https://timesofindia.indiatimes.com/',
        'sections': [
            'india',
            'world',
            'india/mumbai-terror-attacks'
        ]
    }
}

# International Security News Sources
INTERNATIONAL_SOURCES = {
    'BBC Security': {
        'base_url': 'https://www.bbc.com/',
        'sections': [
            'news/world',
            'news/uk',
            'news/technology'
        ]
    },
    'Reuters World': {
        'base_url': 'https://www.reuters.com/',
        'sections': [
            'world',
            'technology',
            'world/middle-east'
        ]
    },
    'CNN Security': {
        'base_url': 'https://edition.cnn.com/',
        'sections': [
            'world',
            'asia',
            'middleeast'
        ]
    }
}

# Defense and security keywords for filtering
DEFENSE_KEYWORDS = [
    'indian army', 'indian navy', 'indian air force', 'defense', 'defence',
    'military', 'border', 'pakistan', 'china', 'terrorism', 'terrorist',
    'security', 'intelligence', 'surveillance', 'threat', 'attack',
    'weapons', 'missile', 'drone', 'cyber', 'warfare', 'conflict',
    'kashmir', 'loc', 'lac', 'ceasefire', 'infiltration', 'encounter',
    'nsg', 'crpf', 'bsf', 'itbp', 'cisf', 'raw', 'ib', 'drdo', 'isro'
]

class DefenseNewsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.scraped_articles = []
        self.lock = threading.Lock()
    
    def is_defense_relevant(self, title, content):
        """Check if article is relevant to defense/security."""
        text = (title + ' ' + content).lower()
        
        # Count defense keywords
        keyword_count = sum(1 for keyword in DEFENSE_KEYWORDS if keyword.lower() in text)
        
        # High relevance if multiple keywords found
        return keyword_count >= 2
    
    def extract_article_links(self, url):
        """Extract article links from a news section page."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            links = []
            
            # Common link selectors for news sites
            link_selectors = [
                'a[href*="/news/"]',
                'a[href*="/article/"]',
                'a[href*="/story/"]',
                'a[href*="/world/"]',
                'a[href*="/india/"]',
                'a[href*="/defence/"]',
                'a[href*="/security/"]',
                '.headline a',
                '.title a',
                'h2 a',
                'h3 a'
            ]
            
            for selector in link_selectors:
                elements = soup.select(selector)
                for element in elements:
                    href = element.get('href')
                    if href and isinstance(href, str):
                        full_url = urljoin(url, href)
                        if full_url not in links:
                            links.append(full_url)
            
            return links[:20]  # Limit to 20 links per section
            
        except Exception as e:
            print(f"Error extracting links from {url}: {e}")
            return []
    
    def scrape_article_content(self, url):
        """Scrape content from a single article."""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = ""
            title_selectors = ['h1', 'h2', '.headline', '.title', '.article-title']
            for selector in title_selectors:
                title_element = soup.select_one(selector)
                if title_element and title_element.get_text(strip=True):
                    title = title_element.get_text(strip=True)
                    break
            
            if not title:
                title_tag = soup.find('title')
                if title_tag:
                    title = title_tag.get_text(strip=True)
            
            # Extract content
            content = ""
            content_selectors = [
                'article',
                '.article-body',
                '.story-body',
                '.content',
                '.post-content',
                '.entry-content',
                'main'
            ]
            
            content_paragraphs = []
            for selector in content_selectors:
                content_container = soup.select_one(selector)
                if content_container:
                    paragraphs = content_container.find_all('p')
                    if paragraphs:
                        content_paragraphs = [p.get_text(strip=True) for p in paragraphs 
                                            if p.get_text(strip=True) and len(p.get_text(strip=True)) > 30]
                        break
            
            if not content_paragraphs:
                paragraphs = soup.find_all('p')
                content_paragraphs = [p.get_text(strip=True) for p in paragraphs 
                                    if p.get_text(strip=True) and len(p.get_text(strip=True)) > 50]
            
            content = '\n\n'.join(content_paragraphs)
            
            # Basic validation
            if not title:
                title = "No title found"
            if not content or len(content) < 100:
                return None  # Skip articles with insufficient content
            
            # Check defense relevance
            if not self.is_defense_relevant(title, content):
                return None  # Skip non-defense articles
            
            article_data = {
                'title': title,
                'content': content,
                'url': url,
                'scraped_timestamp': datetime.now().isoformat(),
                'content_length': len(content),
                'word_count': len(content.split()),
                'source_domain': urlparse(url).netloc
            }
            
            print(f"✓ Scraped defense article: {title[:60]}...")
            return article_data
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def scrape_source_section(self, source_name, source_config, section):
        """Scrape articles from a specific source section."""
        section_url = urljoin(source_config['base_url'], section)
        print(f"🔍 Scanning {source_name} - {section}")
        
        try:
            # Get article links
            links = self.extract_article_links(section_url)
            
            for link in links:
                article = self.scrape_article_content(link)
                if article:
                    with self.lock:
                        self.scraped_articles.append(article)
                
                # Be respectful with delays
                time.sleep(1)
                
        except Exception as e:
            print(f"Error scraping section {section_url}: {e}")
    
    def scrape_defense_news(self, max_workers=3):
        """Scrape defense news from multiple sources."""
        print("🛡️ Starting Defense News Intelligence Gathering")
        print("=" * 60)
        
        all_sources = {**INDIAN_DEFENSE_SOURCES, **INTERNATIONAL_SOURCES}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            
            for source_name, source_config in all_sources.items():
                for section in source_config['sections']:
                    future = executor.submit(
                        self.scrape_source_section, 
                        source_name, 
                        source_config, 
                        section
                    )
                    futures.append(future)
            
            # Wait for all scraping to complete
            concurrent.futures.wait(futures)
        
        print(f"\n✅ Defense intelligence gathering complete!")
        print(f"📊 Total defense articles found: {len(self.scraped_articles)}")
        
        return self.scraped_articles
    
    def save_articles(self, output_dir="defense_data"):
        """Save scraped articles to JSON files."""
        if not self.scraped_articles:
            print("No articles to save.")
            return
        
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for i, article in enumerate(self.scraped_articles):
            # Create clean filename
            title = article['title']
            clean_title = re.sub(r'[^\w\s-]', '', title.lower())
            clean_title = re.sub(r'[-\s]+', '_', clean_title)
            clean_title = clean_title[:50].strip('_')
            
            if not clean_title:
                clean_title = f"defense_article_{i+1}"
            
            filename = f"{clean_title}_{timestamp}_{i+1}.json"
            filepath = os.path.join(output_dir, filename)
            
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(article, f, indent=2, ensure_ascii=False)
                
                print(f"💾 Saved: {filepath}")
                
            except Exception as e:
                print(f"Error saving {filepath}: {e}")
        
        # Create summary file
        summary = {
            'total_articles': len(self.scraped_articles),
            'scraping_timestamp': timestamp,
            'sources_scraped': list(set(article['source_domain'] for article in self.scraped_articles)),
            'articles': [
                {
                    'title': article['title'],
                    'url': article['url'],
                    'source': article['source_domain'],
                    'word_count': article['word_count']
                }
                for article in self.scraped_articles
            ]
        }
        
        summary_file = os.path.join(output_dir, f"defense_summary_{timestamp}.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Summary saved: {summary_file}")

def monitor_defense_news():
    """Continuous monitoring function for defense news."""
    print("🚨 ARGUS Defense Monitoring System Started")
    print("🔄 Monitoring defense and security news sources...")
    print("Press Ctrl+C to stop monitoring")
    
    scraper = DefenseNewsScraper()
    
    try:
        while True:
            print(f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Starting news scan...")
            
            # Scrape defense news
            articles = scraper.scrape_defense_news(max_workers=2)
            
            if articles:
                # Save articles
                scraper.save_articles()
                
                # Clear articles for next iteration
                scraper.scraped_articles = []
                
                print(f"💡 Next scan in 5 minutes...")
                time.sleep(300)  # Wait 5 minutes
            else:
                print("No new defense articles found. Waiting 5 minutes...")
                time.sleep(300)  # Wait 5 minutes
                
    except KeyboardInterrupt:
        print("\n🛑 Defense monitoring stopped by user")
    except Exception as e:
        print(f"Error in monitoring: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--monitor':
        monitor_defense_news()
    else:
        scraper = DefenseNewsScraper()
        articles = scraper.scrape_defense_news()
        
        if articles:
            scraper.save_articles()
            
            print(f"\n🎯 DEFENSE INTELLIGENCE SUMMARY:")
            print(f"📊 Articles collected: {len(articles)}")
            print(f"🌐 Sources: {len(set(article['source_domain'] for article in articles))}")
            print(f"📝 Total words: {sum(article['word_count'] for article in articles):,}")
            
            print(f"\n📋 TOP DEFENSE HEADLINES:")
            for i, article in enumerate(articles[:5], 1):
                print(f"{i}. {article['title']}")
                print(f"   🔗 {article['source_domain']}")
                print(f"   📏 {article['word_count']} words\n")
            
            print(f"💡 Run 'python defense_intelligence.py' to analyze these articles")
            print(f"💡 Use '--monitor' flag for continuous monitoring")
        else:
            print("No defense articles found. Try again later.")