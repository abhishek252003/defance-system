#!/usr/bin/env python3
"""
ARGUS Intelligence Dashboard
A Streamlit-based web interface for viewing and analyzing intelligence data.
"""

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
import sys

# Add the argus_scraper directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'argus_scraper'))

# Import our custom modules
try:
    from argus_scraper.scraper import scrape_article, save_to_json
    from argus_scraper.process_text import extract_entities, save_to_db
except ImportError as e:
    # Fallback for when modules are not available
    scrape_article = None
    save_to_json = None
    extract_entities = None
    save_to_db = None

# Configure Streamlit page
st.set_page_config(
    page_title="ARGUS Intelligence Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_db_connection():
    """
    Initialize database connection with error handling.
    
    Returns:
        sqlite3.Connection: Database connection or None if failed
    """
    try:
        conn = sqlite3.connect('intelligence.db')
        return conn
    except sqlite3.Error as e:
        st.error(f"Database connection failed: {e}")
        return None

def get_all_articles():
    """
    Retrieve all articles from the database.
    
    Returns:
        list: List of tuples (id, title, url, scraped_timestamp)
    """
    conn = init_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, title, url, scraped_timestamp, content_length, word_count
            FROM articles 
            ORDER BY scraped_timestamp DESC
        ''')
        articles = cursor.fetchall()
        return articles
    except sqlite3.Error as e:
        st.error(f"Error fetching articles: {e}")
        return []
    finally:
        conn.close()

def get_article_by_id(article_id):
    """
    Retrieve a specific article by ID.
    
    Args:
        article_id (int): The article ID
        
    Returns:
        tuple: Article data or None if not found
    """
    conn = init_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, title, content, url, scraped_timestamp, content_length, word_count
            FROM articles 
            WHERE id = ?
        ''', (article_id,))
        article = cursor.fetchone()
        return article
    except sqlite3.Error as e:
        st.error(f"Error fetching article: {e}")
        return None
    finally:
        conn.close()

def get_entities_by_article_id(article_id):
    """
    Retrieve all entities for a specific article.
    
    Args:
        article_id (int): The article ID
        
    Returns:
        dict: Dictionary with entities grouped by type
    """
    conn = init_db_connection()
    if not conn:
        return {}
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT text, type
            FROM entities 
            WHERE article_id = ?
            ORDER BY type, text
        ''', (article_id,))
        entities = cursor.fetchall()
        
        # Group entities by type
        grouped = {'PERSON': [], 'ORG': [], 'LOCATION': []}
        for text, entity_type in entities:
            if entity_type in grouped:
                grouped[entity_type].append(text)
        
        return grouped
        
    except sqlite3.Error as e:
        st.error(f"Error fetching entities: {e}")
        return {}
    finally:
        conn.close()

def get_database_stats():
    """
    Get overall database statistics.
    
    Returns:
        dict: Dictionary containing database statistics
    """
    conn = init_db_connection()
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
            ORDER BY COUNT(*) DESC
        ''')
        entity_stats = cursor.fetchall()
        
        # Get total entity count
        cursor.execute('SELECT COUNT(*) FROM entities')
        total_entities = cursor.fetchone()[0]
        
        # Get recent articles (last 7 days)
        cursor.execute('''
            SELECT COUNT(*) FROM articles 
            WHERE datetime(scraped_timestamp) >= datetime('now', '-7 days')
        ''')
        recent_articles = cursor.fetchone()[0]
        
        return {
            'total_articles': article_count,
            'total_entities': total_entities,
            'entity_breakdown': entity_stats,
            'recent_articles': recent_articles
        }
        
    except sqlite3.Error as e:
        st.error(f"Error fetching database stats: {e}")
        return None
    finally:
        conn.close()

def main():
    """Main dashboard application."""
    
    # Main title
    st.title("🔍 ARGUS Intelligence Dashboard")
    st.markdown("*Advanced intelligence gathering and analysis system*")
    
    # Check if database exists
    if not os.path.exists('intelligence.db'):
        st.warning("⚠️ No intelligence database found. Please scrape some articles first!")
        st.info("""
        To get started:
        1. Navigate to the project directory
        2. Run: `python argus_scraper/scraper.py <news_article_url>`
        3. Run: `python argus_scraper/process_text.py`
        4. Refresh this dashboard
        """)
        return
    
    # Sidebar
    st.sidebar.header("📊 ARGUS Control Panel")
    
    # URL Analysis Section
    st.sidebar.subheader("🎯 Analyze New URL")
    
    # URL input
    url_input = st.sidebar.text_input(
        "Enter article URL:",
        placeholder="https://example.com/news/article",
        help="Paste the URL of a news article to scrape and analyze"
    )
    
    # Analyze button
    analyze_button = st.sidebar.button(
        "🚀 Analyze URL",
        type="primary",
        help="Scrape, process, and store the article"
    )
    
    # Handle URL analysis
    if analyze_button and url_input:
        if scrape_article and extract_entities and save_to_db:
            # Show progress
            with st.sidebar:
                with st.spinner('Analyzing URL...'):
                    # Step 1: Scrape the article
                    st.write("🔄 Step 1: Scraping article...")
                    article_data = scrape_article(url_input)
                    
                    if article_data and article_data['title'] != "Error: Failed to fetch URL":
                        st.success("✓ Article scraped successfully")
                        
                        # Step 2: Extract entities
                        st.write("🔄 Step 2: Extracting entities...")
                        entities_data = extract_entities(article_data['content'])
                        st.success("✓ Entities extracted")
                        
                        # Step 3: Save to database
                        st.write("🔄 Step 3: Saving to database...")
                        article_id = save_to_db(article_data, entities_data)
                        
                        if article_id:
                            st.success(f"✓ Analysis complete! Article ID: {article_id}")
                            st.balloons()
                            # Force a rerun to refresh the article list
                            st.rerun()
                        else:
                            st.error("✗ Failed to save to database")
                    else:
                        st.error("✗ Failed to scrape article")
                        if article_data:
                            st.error(f"Error: {article_data['content']}")
        else:
            st.sidebar.error("✗ Analysis modules not available. Please check your environment setup.")
    
    elif analyze_button and not url_input:
        st.sidebar.error("Please enter a URL to analyze")
    
    # Separator
    st.sidebar.markdown("---")
    
    # Get articles for sidebar
    articles = get_all_articles()
    
    if not articles:
        st.sidebar.warning("No articles found in database")
        st.warning("No articles available. Please scrape some articles first!")
        return
    
    # Create article selection radio buttons
    article_options = {}
    for article in articles:
        article_id, title, url, timestamp, content_length, word_count = article
        # Truncate long titles for display
        display_title = title[:50] + "..." if len(title) > 50 else title
        # Format timestamp
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            formatted_time = dt.strftime("%Y-%m-%d %H:%M")
        except:
            formatted_time = timestamp[:16]  # Fallback formatting
        
        display_label = f"{display_title} ({formatted_time})"
        article_options[display_label] = article_id
    
    # Article selection
    st.sidebar.subheader("📰 Select Article")
    selected_display = st.sidebar.radio(
        "Choose an article to analyze:",
        list(article_options.keys()),
        key="article_selector"
    )
    
    selected_article_id = article_options[selected_display]
    
    # Database statistics in sidebar
    st.sidebar.subheader("📈 Database Overview")
    stats = get_database_stats()
    if stats:
        st.sidebar.metric("Total Articles", stats['total_articles'])
        st.sidebar.metric("Total Entities", stats['total_entities'])
        st.sidebar.metric("Recent Articles (7d)", stats['recent_articles'])
        
        if stats['entity_breakdown']:
            st.sidebar.write("**Entity Types:**")
            for entity_type, count in stats['entity_breakdown']:
                st.sidebar.write(f"• {entity_type}: {count}")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📋 Dashboard Overview")
        
        # Welcome message
        st.markdown("""
        Welcome to the ARGUS Intelligence Dashboard! 
        
        This system helps you:
        - 🔍 **Scrape** news articles from various sources
        - 🧠 **Analyze** content using AI-powered NLP
        - 📊 **Visualize** extracted intelligence data
        - 🗃️ **Store** and organize information systematically
        
        Select an article from the sidebar to view detailed analysis.
        """)
        
        # Quick stats
        if stats:
            st.subheader("📊 Quick Statistics")
            
            # Create metrics columns
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            
            with metric_col1:
                st.metric(
                    label="Articles Analyzed",
                    value=stats['total_articles'],
                    delta=f"+{stats['recent_articles']} this week"
                )
            
            with metric_col2:
                st.metric(
                    label="Entities Extracted",
                    value=stats['total_entities']
                )
            
            with metric_col3:
                persons = next((count for etype, count in stats['entity_breakdown'] if etype == 'PERSON'), 0)
                st.metric(
                    label="People Identified",
                    value=persons
                )
            
            with metric_col4:
                orgs = next((count for etype, count in stats['entity_breakdown'] if etype == 'ORG'), 0)
                st.metric(
                    label="Organizations Found",
                    value=orgs
                )
    
    with col2:
        st.header("🎯 System Status")
        
        # System health checks
        st.subheader("Health Checks")
        
        # Database check
        db_status = "✅ Connected" if os.path.exists('intelligence.db') else "❌ Not Found"
        st.write(f"**Database:** {db_status}")
        
        # Articles check
        article_status = f"✅ {len(articles)} articles" if articles else "⚠️ No articles"
        st.write(f"**Articles:** {article_status}")
        
        # Dependencies check (basic)
        st.write("**Dependencies:** ⚠️ Check console for spaCy/NLP status")
        
        # Quick actions
        st.subheader("🚀 Quick Actions")
        st.markdown("""
        **Next Steps:**
        1. Scrape more articles
        2. Analyze entity relationships
        3. Export intelligence reports
        4. Set up automated monitoring
        """)
        
        # Recent activity
        if articles:
            st.subheader("📈 Recent Activity")
            recent_articles = articles[:3]  # Show last 3 articles
            for article in recent_articles:
                article_id, title, url, timestamp, content_length, word_count = article
                with st.expander(f"📰 {title[:30]}..."):
                    st.write(f"**URL:** {url}")
                    st.write(f"**Scraped:** {timestamp}")
                    st.write(f"**Length:** {content_length} chars, {word_count} words")

    # Display selected article analysis
    if selected_article_id:
        st.header(f"📄 Article Analysis")
        
        # Get article details
        article_details = get_article_by_id(selected_article_id)
        if article_details:
            article_id, title, content, url, timestamp, content_length, word_count = article_details
            
            # Article header
            st.subheader(f"📰 {title}")
            
            # Article metadata
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Content Length", f"{content_length:,} chars")
            with col2:
                st.metric("Word Count", f"{word_count:,} words")
            with col3:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    formatted_time = timestamp
                st.metric("Scraped", formatted_time)
            
            # Article URL
            st.markdown(f"**Source URL:** [{url}]({url})")
            
            # Article content
            st.subheader("📃 Article Text")
            with st.expander("Click to view full article content", expanded=False):
                st.text_area(
                    "Full Article Content",
                    value=content,
                    height=300,
                    disabled=True,
                    label_visibility="collapsed"
                )
            
            # Content preview
            st.markdown("**Content Preview:**")
            preview_text = content[:500] + "..." if len(content) > 500 else content
            st.markdown(f"*{preview_text}*")
            
            # Intelligence Analysis
            st.subheader("🧠 Intelligence Analysis")
            
            # Get entities for this article
            entities = get_entities_by_article_id(selected_article_id)
            
            if any(entities.values()):
                # Create columns for different entity types
                entity_col1, entity_col2, entity_col3 = st.columns(3)
                
                with entity_col1:
                    st.markdown("**👤 Detected Persons**")
                    if entities['PERSON']:
                        with st.expander(f"View {len(entities['PERSON'])} persons", expanded=True):
                            for person in entities['PERSON']:
                                st.write(f"• {person}")
                    else:
                        st.info("No persons detected")
                
                with entity_col2:
                    st.markdown("**🏢 Detected Organizations**")
                    if entities['ORG']:
                        with st.expander(f"View {len(entities['ORG'])} organizations", expanded=True):
                            for org in entities['ORG']:
                                st.write(f"• {org}")
                    else:
                        st.info("No organizations detected")
                
                with entity_col3:
                    st.markdown("**📍 Detected Locations**")
                    if entities['LOCATION']:
                        with st.expander(f"View {len(entities['LOCATION'])} locations", expanded=True):
                            for loc in entities['LOCATION']:
                                st.write(f"• {loc}")
                    else:
                        st.info("No locations detected")
                
                # Entity summary
                total_entities = len(entities['PERSON']) + len(entities['ORG']) + len(entities['LOCATION'])
                st.success(f"🎯 **Total entities extracted:** {total_entities}")
                
                # Entity breakdown chart (if we have data)
                if total_entities > 0:
                    st.subheader("📊 Entity Distribution")
                    entity_data = {
                        'Entity Type': [],
                        'Count': []
                    }
                    
                    for entity_type, entity_list in entities.items():
                        if entity_list:
                            display_name = {
                                'PERSON': 'Persons',
                                'ORG': 'Organizations', 
                                'LOCATION': 'Locations'
                            }.get(entity_type, entity_type)
                            entity_data['Entity Type'].append(display_name)
                            entity_data['Count'].append(len(entity_list))
                    
                    if entity_data['Count']:
                        df = pd.DataFrame(entity_data)
                        st.bar_chart(df.set_index('Entity Type'))
            
            else:
                st.warning("⚠️ No entities found for this article. The NLP analysis may not have been run yet.")
                st.info("To analyze entities, run: `python argus_scraper/process_text.py`")

if __name__ == "__main__":
    main()