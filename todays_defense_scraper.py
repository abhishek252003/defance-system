#!/usr/bin/env python3
"""
ARGUS Today's Defense News Scraper
Specialized scraper for collecting only today's defense, security, and terrorism-related news.
Implements enhanced keyword filtering for precise defense relevance detection.
"""

import requests
from bs4 import BeautifulSoup
import time
import json
import os
from datetime import datetime, date
import concurrent.futures
import threading
from urllib.parse import urljoin, urlparse
import re

# High-impact defense and security keywords (must-have for relevance)
HIGH_IMPACT_KEYWORDS = [
    'defense', 'defence', 'military', 'army', 'navy', 'air force', 
    'terrorism', 'terrorist', 'attack', 'threat', 'security',
    'missile', 'drone', 'cyber', 'warfare', 'conflict',
    'border', 'infiltration', 'encounter', 'operation',
    'weapons', 'ammunition', 'explosive', 'ied',
    'intelligence', 'surveillance', 'reconnaissance',
    'nsg', 'crpf', 'bsf', 'itbp', 'cisf', 'raw', 'ib',
    'pakistan', 'china', 'kashmir', 'loc', 'lac'
]

# General defense keywords (need multiple for relevance)
GENERAL_KEYWORDS = [
    'soldier', 'troop', 'deployment', 'base', 'camp',
    'exercise', 'training', 'patrol', 'checkpoint',
    'smuggling', 'illegal crossing', 'refugee',
    'hijack', 'hostage', 'bomb', 'gun', 'rifle',
    'artillery', 'tank', 'aircraft', 'fighter jet',
    'warship', 'submarine', 'destroyer', 'frigate',
    'satellite', 'radar', 'sonar', 'missile system',
    'border security', 'coastal security', 'maritime security',
    'cyber attack', 'hacking', 'malware', 'ransomware',
    'data breach', 'cyber warfare', 'ddos', 'phishing',
    'extremist', 'radical', 'militant', 'insurgent',
    'suicide bomb', 'ied', ' improvised explosive device',
    'security alert', 'threat assessment', 'emergency response'
]

class TodaysDefenseNewsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.scraped_articles = []
        self.lock = threading.Lock()
        self.today_date = date.today().strftime('%Y-%m-%d')
    
    def is_defense_relevant(self, title, content):
        """Check if article is relevant using a tiered keyword approach."""
        text = (title + ' ' + content).lower()
        
        # Check for any high-impact keyword (highly likely to be relevant)
        for keyword in HIGH_IMPACT_KEYWORDS:
            if keyword.lower() in text:
                return True
        
        # If no high-impact keywords, check for a combination of general keywords
        general_keyword_count = sum(1 for keyword in GENERAL_KEYWORDS if keyword.lower() in text)
        
        # Require at least 3 general keywords to be considered relevant
        return general_keyword_count >= 3
    
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
                        # Only include links that might be from today
                        if self.is_potentially_today(full_url):
                            if full_url not in links:
                                links.append(full_url)
            
            return links[:15]  # Limit to 15 links per section
            
        except Exception as e:
            print(f"Error extracting links from {url}: {e}")
            return []
    
    def is_potentially_today(self, url):
        """Check if URL might contain today's content based on patterns."""
        # This is a simple heuristic - in a real implementation, you might check
        # the URL structure or make a HEAD request to check modification date
        return True  # For now, we'll check all URLs and filter by content date
    
    def scrape_article_content(self, url):
        """Scrape content from a single article."""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract publication date if available
            pub_date = self.extract_publication_date(soup, url)
            if pub_date and pub_date != self.today_date:
                print(f"⏭️  Skipping non-today article (published: {pub_date}): {url}")
                return None
            
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
                'source_domain': urlparse(url).netloc,
                'publication_date': pub_date or self.today_date
            }
            
            print(f"✓ Scraped defense article: {title[:60]}...")
            return article_data
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def extract_publication_date(self, soup, url):
        """Extract publication date from article."""
        # Try various selectors for publication date
        date_selectors = [
            'time',
            '.publish-date',
            '.published',
            '.date',
            '[datetime]',
            '.article-date',
            '.post-date'
        ]
        
        for selector in date_selectors:
            date_element = soup.select_one(selector)
            if date_element:
                # Try to get datetime attribute first
                if date_element.get('datetime'):
                    date_str = date_element.get('datetime')
                    return self.parse_date_string(date_str)
                
                # Try to get text content
                date_text = date_element.get_text(strip=True)
                if date_text:
                    parsed_date = self.parse_date_string(date_text)
                    if parsed_date:
                        return parsed_date
        
        # Try to find date in URL or meta tags
        return None
    
    def parse_date_string(self, date_str):
        """Parse various date string formats."""
        if not date_str:
            return None
        
        # Common date formats
        formats = [
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%d-%m-%Y',
            '%d/%m/%Y',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d %H:%M:%S',
            '%B %d, %Y',
            '%b %d, %Y',
            '%d %B %Y',
            '%d %b %Y'
        ]
        
        for fmt in formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return parsed_date.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
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
        print("🛡️ Starting Today's Defense News Intelligence Gathering")
        print("=" * 60)
        print(f"📅 Focusing on articles from: {self.today_date}")
        
        # Indian Defense and Security News Sources
        INDIAN_DEFENSE_SOURCES = {
            'Financial Express Defence': {
                'base_url': 'https://www.financialexpress.com/',
                'sections': ['defence']
            },
            'Economic Times Defence': {
                'base_url': 'https://economictimes.indiatimes.com/',
                'sections': ['news/defence']
            },
            'Hindustan Times India News': {
                'base_url': 'https://www.hindustantimes.com/',
                'sections': ['india-news']
            }
        }
        
        # International Security News Sources
        INTERNATIONAL_SOURCES = {
            'BBC Security': {
                'base_url': 'https://www.bbc.com/',
                'sections': ['news/world']
            },
            'CNN Security': {
                'base_url': 'https://edition.cnn.com/',
                'sections': ['world']
            }
        }
        
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
        
        print(f"\n✅ Today's defense intelligence gathering complete!")
        print(f"📊 Total defense articles found: {len(self.scraped_articles)}")
        
        return self.scraped_articles
    
    def save_articles(self, output_dir="todays_defense_data"):
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
            'scraping_date': self.today_date,
            'scraping_timestamp': timestamp,
            'sources_scraped': list(set(article['source_domain'] for article in self.scraped_articles)),
            'articles': [
                {
                    'title': article['title'],
                    'url': article['url'],
                    'source': article['source_domain'],
                    'word_count': article['word_count'],
                    'publication_date': article['publication_date']
                }
                for article in self.scraped_articles
            ]
        }
        
        summary_file = os.path.join(output_dir, f"todays_defense_summary_{timestamp}.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Summary saved: {summary_file}")

def run_todays_defense_scraper():
    """Run the today's defense news scraper."""
    scraper = TodaysDefenseNewsScraper()
    articles = scraper.scrape_defense_news()
    
    if articles:
        scraper.save_articles()
        
        print(f"\n🎯 TODAY'S DEFENSE INTELLIGENCE SUMMARY:")
        print(f"📅 Date: {scraper.today_date}")
        print(f"📊 Articles collected: {len(articles)}")
        print(f"🌐 Sources: {len(set(article['source_domain'] for article in articles))}")
        print(f"📝 Total words: {sum(article['word_count'] for article in articles):,}")
        
        print(f"\n📋 TOP DEFENSE HEADLINES:")
        for i, article in enumerate(articles[:5], 1):
            print(f"{i}. {article['title']}")
            print(f"   🔗 {article['source_domain']}")
            print(f"   📏 {article['word_count']} words\n")
        
        print(f"💡 Run 'python defense_intelligence.py --batch-process' to analyze these articles")
    else:
        print("No defense articles found for today. Try again later.")

if __name__ == "__main__":
    run_todays_defense_scraper()