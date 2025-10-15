#!/usr/bin/env python3
"""
ARGUS Web Scraper Module
This module provides functionality to scrape news articles from web pages.
"""

import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
import sys
import json
import os
from datetime import datetime
import re

def scrape_article(url):
    """
    Scrape article content from a given URL.
    
    Args:
        url (str): The URL of the article to scrape
        
    Returns:
        dict: Dictionary containing 'title' and 'content' of the article
        
    How to use the browser's Inspect tool to find the correct HTML tags:
    
    1. Right-click on the article title and select "Inspect" or "Inspect Element"
    2. Look for common title tags:
       - <h1> (most common for main titles)
       - <h2> (sometimes used for titles)
       - Tags with class names like "title", "headline", "article-title"
       
    3. Right-click on the article text and inspect:
       - Look for <p> tags inside <article>, <div class="content">, or <main>
       - Common article containers: <article>, <div class="article-body">, <div class="content">
       - Some sites use <div class="story-body"> or <div class="post-content">
       
    4. Look for semantic HTML5 tags:
       - <article> tag usually contains the main content
       - <main> tag often wraps the primary content
       - <section> tags may contain article sections
       
    5. Common class names to look for:
       - Title: .title, .headline, .article-title, .story-headline
       - Content: .content, .article-body, .story-body, .post-content, .entry-content
       
    6. Tips:
       - Avoid navigation, sidebar, and footer content
       - Look for the largest block of continuous text
       - Check if the site has a "reader mode" - inspect that for cleaner selectors
    """
    
    try:
        # Set a user agent to avoid being blocked by some websites
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"Fetching URL: {url}")
        
        # Make the HTTP request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the title
        title = ""
        
        # Try different title selectors in order of preference
        title_selectors = [
            'h1',                           # Most common
            'h2',                           # Sometimes used
            '.title',                       # Common class name
            '.headline',                    # News sites
            '.article-title',               # Specific article titles
            '.story-headline',              # Story headlines
            'title'                         # HTML title tag as fallback
        ]
        
        for selector in title_selectors:
            title_element = soup.select_one(selector)
            if title_element and title_element.get_text(strip=True):
                title = title_element.get_text(strip=True)
                break
        
        # If no title found, try the page title
        if not title:
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text(strip=True)
        
        # Extract the article content
        content = ""
        
        # Try different content selectors in order of preference
        content_selectors = [
            'article',                      # Semantic HTML5 article tag
            '.article-body',                # Common article body class
            '.content',                     # Generic content class
            '.story-body',                  # Story body class
            '.post-content',                # Blog post content
            '.entry-content',               # Entry content
            'main',                         # Main content area
            '.article-content',             # Article specific content
        ]
        
        content_paragraphs = []
        
        for selector in content_selectors:
            content_container = soup.select_one(selector)
            if content_container:
                # Find all paragraph tags within the container
                paragraphs = content_container.find_all('p')
                if paragraphs:
                    content_paragraphs = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
                    break
        
        # If no content found with container selectors, try direct paragraph search
        if not content_paragraphs:
            paragraphs = soup.find_all('p')
            # Filter out short paragraphs (likely navigation or metadata)
            content_paragraphs = [p.get_text(strip=True) for p in paragraphs 
                                if p.get_text(strip=True) and len(p.get_text(strip=True)) > 50]
        
        # Join all paragraphs into content
        content = '\n\n'.join(content_paragraphs)
        
        # Basic validation
        if not title:
            title = "No title found"
            
        if not content:
            content = "No content found"
            
        print(f"Successfully scraped article: '{title[:50]}...'")
        print(f"Content length: {len(content)} characters")
        
        return {
            'title': title,
            'content': content,
            'url': url
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return {
            'title': "Error: Failed to fetch URL",
            'content': f"Request failed: {str(e)}",
            'url': url
        }
    except Exception as e:
        print(f"Error parsing content: {e}")
        return {
            'title': "Error: Failed to parse content",
            'content': f"Parsing failed: {str(e)}",
            'url': url
        }

def save_to_json(data):
    """
    Save scraped article data to a JSON file.
    
    Args:
        data (dict): Dictionary containing article data from scrape_article()
        
    Returns:
        str: Path to the saved JSON file
    """
    
    try:
        # Create scraped_data directory if it doesn't exist
        data_dir = "scraped_data"
        os.makedirs(data_dir, exist_ok=True)
        
        # Generate clean filename from article title
        title = data.get('title', 'untitled')
        
        # Clean the title for use as filename
        # Remove special characters and replace spaces with underscores
        clean_title = re.sub(r'[^\w\s-]', '', title.lower())
        clean_title = re.sub(r'[-\s]+', '_', clean_title)
        
        # Limit filename length and remove leading/trailing underscores
        clean_title = clean_title[:50].strip('_')
        
        # If title is empty after cleaning, use timestamp
        if not clean_title:
            clean_title = f"article_{int(datetime.now().timestamp())}"
            
        # Create filename with timestamp to avoid duplicates
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{clean_title}_{timestamp}.json"
        filepath = os.path.join(data_dir, filename)
        
        # Add metadata to the data
        enriched_data = {
            'url': data.get('url', ''),
            'title': data.get('title', ''),
            'content': data.get('content', ''),
            'scraped_timestamp': datetime.now().isoformat(),
            'content_length': len(data.get('content', '')),
            'word_count': len(data.get('content', '').split())
        }
        
        # Save to JSON file with proper formatting
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(enriched_data, f, indent=2, ensure_ascii=False)
            
        print(f"Article saved to: {filepath}")
        print(f"File size: {os.path.getsize(filepath)} bytes")
        
        return filepath
        
    except Exception as e:
        print(f"Error saving to JSON: {e}")
        return None

if __name__ == "__main__":
    # Test the scraper with a sample news article URL
    print("ARGUS Web Scraper Test")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        # If URL provided as command line argument
        test_url = sys.argv[1]
        print(f"Testing with provided URL: {test_url}")
        print("\nStep 1: Scraping article...")
        
        result = scrape_article(test_url)
        print("\nScraping Results:")
        print(f"Title: {result['title']}")
        print(f"Content Preview: {result['content'][:200]}...")
        print(f"Full Content Length: {len(result['content'])} characters")
        
        print("\nStep 2: Saving to JSON...")
        saved_file = save_to_json(result)
        
        if saved_file:
            print(f"\n✓ Successfully saved article to: {saved_file}")
            
            # Display the saved JSON structure
            try:
                with open(saved_file, 'r', encoding='utf-8') as f:
                    saved_data = json.load(f)
                print("\nSaved JSON structure:")
                for key, value in saved_data.items():
                    if key == 'content':
                        print(f"  {key}: {value[:100]}...")
                    else:
                        print(f"  {key}: {value}")
            except Exception as e:
                print(f"Error reading saved file: {e}")
        else:
            print("\n✗ Failed to save article")
        
    else:
        print("No URL provided. Please run with: python scraper.py <URL>")
        print("\nExample usage:")
        print("python scraper.py https://www.bbc.com/news/technology-12345678")
        print("\nFor testing purposes, you can use any news article URL from:")
        print("- BBC News")
        print("- Reuters")
        print("- The Guardian")
        print("- Any other news website")
        print("\nNote: The scraped article will be automatically saved to the 'scraped_data/' folder.")