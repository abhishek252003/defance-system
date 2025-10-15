#!/usr/bin/env python3
"""
ARGUS System Test Script
Quick validation that all components are working correctly.
"""

import os
import sys
import sqlite3
from datetime import datetime

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import requests
        print("✓ requests")
    except ImportError:
        print("✗ requests - run: pip install requests")
        return False
    
    try:
        import bs4
        print("✓ beautifulsoup4")
    except ImportError:
        print("✗ beautifulsoup4 - run: pip install beautifulsoup4")
        return False
    
    try:
        import streamlit
        print("✓ streamlit")
    except ImportError:
        print("✗ streamlit - run: pip install streamlit")
        return False
    
    try:
        import spacy
        print("✓ spacy")
        
        # Test spaCy model
        try:
            nlp = spacy.load("en_core_web_sm")
            print("✓ en_core_web_sm model")
        except OSError:
            print("✗ en_core_web_sm model - run: python -m spacy download en_core_web_sm")
            return False
            
    except ImportError:
        print("✗ spacy - run: pip install spacy")
        return False
    
    return True

def test_modules():
    """Test that our custom modules can be imported."""
    print("\nTesting custom modules...")
    
    sys.path.append('argus_scraper')
    
    try:
        from argus_scraper.scraper import scrape_article, save_to_json
        print("✓ scraper module")
    except ImportError as e:
        print(f"✗ scraper module - {e}")
        return False
    
    try:
        from argus_scraper.process_text import extract_entities, save_to_db, init_db
        print("✓ process_text module")
    except ImportError as e:
        print(f"✗ process_text module - {e}")
        return False
    
    return True

def test_database():
    """Test database creation and basic operations."""
    print("\nTesting database functionality...")
    
    try:
        # Import after adding to path
        from argus_scraper.process_text import init_db
        
        # Initialize database
        conn = init_db()
        if conn:
            print("✓ Database initialization")
            
            # Test basic query
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM articles")
            count = cursor.fetchone()[0]
            print(f"✓ Database query (found {count} articles)")
            
            conn.close()
            return True
        else:
            print("✗ Database initialization failed")
            return False
            
    except Exception as e:
        print(f"✗ Database test failed - {e}")
        return False

def test_scraper():
    """Test basic scraping functionality."""
    print("\nTesting scraper with a simple page...")
    
    try:
        from argus_scraper.scraper import scrape_article
        
        # Test with a simple, reliable URL
        test_url = "https://httpbin.org/html"  # Simple test page
        result = scrape_article(test_url)
        
        if result and 'title' in result and 'content' in result:
            print("✓ Basic scraping functionality")
            return True
        else:
            print("✗ Scraping test failed")
            return False
            
    except Exception as e:
        print(f"✗ Scraper test failed - {e}")
        return False

def test_nlp():
    """Test NLP functionality."""
    print("\nTesting NLP processing...")
    
    try:
        from argus_scraper.process_text import extract_entities
        
        # Test with sample text
        test_text = "Apple Inc. is a technology company based in Cupertino, California. Tim Cook is the CEO."
        
        entities = extract_entities(test_text)
        
        if entities and isinstance(entities, dict):
            print("✓ Entity extraction")
            print(f"  Found: {sum(len(v) for v in entities.values())} entities")
            return True
        else:
            print("✗ Entity extraction failed")
            return False
            
    except Exception as e:
        print(f"✗ NLP test failed - {e}")
        return False

def main():
    """Run all tests."""
    print("ARGUS System Test")
    print("=" * 50)
    
    tests = [
        ("Package Dependencies", test_imports),
        ("Custom Modules", test_modules),
        ("Database System", test_database),
        ("Web Scraping", test_scraper),
        ("NLP Processing", test_nlp)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name))
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        icon = "✓" if result else "✗"
        print(f"{icon} {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 All tests passed! ARGUS system is ready to use.")
        print("\nNext steps:")
        print("1. Run: streamlit run dashboard.py")
        print("2. Or scrape an article: python argus_scraper/scraper.py <URL>")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")
        print("Install missing dependencies and run this test again.")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)