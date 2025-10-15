#!/usr/bin/env python3
"""
ARGUS Defense Data Viewer
Complete viewer for all collected defense intelligence data from web crawling.
Shows comprehensive view of all scraped articles from multiple sources.
"""

import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
import sqlite3
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# Configure Streamlit page
st.set_page_config(
    page_title="🛡️ ARGUS Defense Data Viewer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .defense-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .article-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #1f2937;
    }
    .high-priority {
        border-left: 4px solid #dc2626;
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        color: #ffffff !important;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
    }
    .high-priority h4 {
        color: #ffffff !important;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .high-priority p {
        color: #ffffff !important;
        font-weight: 500;
    }
    .high-priority strong {
        color: #ffffff !important;
        font-weight: 700;
    }
    .high-priority a {
        color: #fecaca !important;
        text-decoration: underline;
    }
    .medium-priority {
        border-left: 4px solid #f59e0b;
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: #ffffff !important;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }
    .medium-priority h4 {
        color: #ffffff !important;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .medium-priority p {
        color: #ffffff !important;
        font-weight: 500;
    }
    .medium-priority strong {
        color: #ffffff !important;
        font-weight: 700;
    }
    .medium-priority a {
        color: #fed7aa !important;
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

def load_all_defense_data():
    """Load all defense data from the defense_data directory."""
    defense_data_dir = "defense_data"
    
    if not os.path.exists(defense_data_dir):
        return [], None
    
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
                    data['file_name'] = file_path.name
                    articles.append(data)
                    
        except Exception as e:
            st.warning(f"Error loading {file_path}: {e}")
    
    return articles, summary_data

def categorize_articles(articles):
    """Categorize articles by defense relevance."""
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
        
        # Count high priority keywords
        high_count = sum(1 for keyword in defense_keywords['high'] if keyword in text)
        medium_count = sum(1 for keyword in defense_keywords['medium'] if keyword in text)
        
        if high_count >= 2:
            high_priority.append(article)
        elif high_count >= 1 or medium_count >= 2:
            medium_priority.append(article)
        else:
            regular.append(article)
    
    return high_priority, medium_priority, regular

def display_article_card(article, priority="regular"):
    """Display an article in a card format."""
    css_class = "article-card"
    if priority == "high":
        css_class += " high-priority"
    elif priority == "medium":
        css_class += " medium-priority"
    
    title = article.get('title', 'Untitled')
    url = article.get('url', '#')
    source = article.get('source_domain', 'Unknown Source')
    word_count = article.get('word_count', 0)
    timestamp = article.get('scraped_timestamp', '')
    content_preview = article.get('content', '')[:200] + "..." if len(article.get('content', '')) > 200 else article.get('content', '')
    
    # Format timestamp
    try:
        if timestamp:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            formatted_time = dt.strftime("%Y-%m-%d %H:%M")
        else:
            formatted_time = "Unknown"
    except:
        formatted_time = timestamp[:16] if len(timestamp) > 16 else timestamp
    
    priority_icon = "🔴" if priority == "high" else ("🟡" if priority == "medium" else "🟢")
    
    st.markdown(f"""
    <div class="{css_class}">
        <h4>{priority_icon} {title}</h4>
        <p><strong>Source:</strong> {source}</p>
        <p><strong>Word Count:</strong> {word_count} | <strong>Scraped:</strong> {formatted_time}</p>
        <p><strong>Preview:</strong> {content_preview}</p>
        <p><a href="{url}" target="_blank">🔗 View Original Article</a></p>
    </div>
    """, unsafe_allow_html=True)

def get_source_statistics(articles):
    """Get statistics by source."""
    source_stats = {}
    for article in articles:
        source = article.get('source_domain', 'Unknown')
        if source not in source_stats:
            source_stats[source] = {'count': 0, 'words': 0}
        source_stats[source]['count'] += 1
        source_stats[source]['words'] += article.get('word_count', 0)
    
    return source_stats

def main():
    """Main application."""
    
    # Header
    st.markdown("""
    <div class="defense-header">
        <h1>🛡️ ARGUS Defense Intelligence Data Viewer</h1>
        <p>Complete view of all collected defense intelligence from auto-crawled web sources</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load all defense data
    with st.spinner("Loading all defense intelligence data..."):
        articles, summary_data = load_all_defense_data()
    
    if not articles:
        st.warning("⚠️ No defense data found. Please run the defense scraper first:")
        st.code("python defense_scraper.py")
        return
    
    # Sidebar filters
    st.sidebar.header("🎯 Data Filters")
    
    # Source filter
    sources = list(set(article.get('source_domain', 'Unknown') for article in articles))
    selected_sources = st.sidebar.multiselect(
        "Filter by Source:",
        sources,
        default=sources
    )
    
    # Date filter
    st.sidebar.subheader("📅 Date Range")
    show_last_hours = st.sidebar.selectbox(
        "Show articles from:",
        ["All time", "Last 24 hours", "Last 48 hours", "Last week"]
    )
    
    # Priority filter
    priority_filter = st.sidebar.selectbox(
        "Priority Level:",
        ["All", "High Priority", "Medium Priority", "Regular"]
    )
    
    # Filter articles
    filtered_articles = [
        article for article in articles 
        if article.get('source_domain', 'Unknown') in selected_sources
    ]
    
    # Categorize articles
    high_priority, medium_priority, regular = categorize_articles(filtered_articles)
    
    # Apply priority filter
    if priority_filter == "High Priority":
        display_articles = high_priority
    elif priority_filter == "Medium Priority":
        display_articles = medium_priority
    elif priority_filter == "Regular":
        display_articles = regular
    else:
        display_articles = filtered_articles
    
    # Main dashboard
    st.header("📊 Defense Intelligence Overview")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🔴 High Priority",
            len(high_priority),
            help="Articles with critical defense keywords"
        )
    
    with col2:
        st.metric(
            "🟡 Medium Priority", 
            len(medium_priority),
            help="Articles with moderate defense relevance"
        )
    
    with col3:
        st.metric(
            "📰 Total Articles",
            len(filtered_articles)
        )
    
    with col4:
        st.metric(
            "🌐 Sources",
            len(selected_sources)
        )
    
    # Source distribution chart
    st.subheader("📈 Data Collection by Source")
    source_stats = get_source_statistics(filtered_articles)
    
    if source_stats:
        source_df = pd.DataFrame([
            {'Source': source, 'Articles': stats['count'], 'Total Words': stats['words']}
            for source, stats in source_stats.items()
        ])
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.pie(source_df, values='Articles', names='Source', 
                         title="Articles by Source")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.bar(source_df, x='Source', y='Total Words',
                         title="Content Volume by Source")
            fig2.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig2, use_container_width=True)
    
    # Key Defense Topics
    st.subheader("🎯 Key Defense Intelligence Topics")
    
    if high_priority:
        st.markdown("""
        <div style="background: linear-gradient(90deg, #dc2626 0%, #b91c1c 100%); 
                    color: white; padding: 15px; border-radius: 10px; margin: 10px 0; 
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <h3 style="color: white; margin: 0;">🔴 HIGH PRIORITY DEFENSE INTELLIGENCE</h3>
            <p style="color: #fecaca; margin: 5px 0 0 0;">Critical defense and security information requiring immediate attention</p>
        </div>
        """, unsafe_allow_html=True)
        for article in high_priority[:10]:  # Show top 10
            display_article_card(article, "high")
    
    if medium_priority and priority_filter in ["All", "Medium Priority"]:
        st.markdown("""
        <div style="background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%); 
                    color: white; padding: 15px; border-radius: 10px; margin: 10px 0; 
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <h3 style="color: white; margin: 0;">🟡 MEDIUM PRIORITY INTELLIGENCE</h3>
            <p style="color: #fef3c7; margin: 5px 0 0 0;">Important defense and security developments</p>
        </div>
        """, unsafe_allow_html=True)
        for article in medium_priority[:10]:  # Show top 10
            display_article_card(article, "medium")
    
    # All articles view
    st.subheader(f"📋 All Articles ({len(display_articles)} total)")
    
    # Search functionality
    search_term = st.text_input("🔍 Search articles:", placeholder="Enter keywords...")
    
    if search_term:
        search_results = [
            article for article in display_articles
            if search_term.lower() in article.get('title', '').lower() or 
               search_term.lower() in article.get('content', '').lower()
        ]
        st.write(f"Found {len(search_results)} articles matching '{search_term}'")
        display_articles = search_results
    
    # Pagination
    articles_per_page = 20
    total_pages = (len(display_articles) + articles_per_page - 1) // articles_per_page
    
    if total_pages > 1:
        page = st.selectbox("📄 Page", range(1, total_pages + 1))
        start_idx = (page - 1) * articles_per_page
        end_idx = start_idx + articles_per_page
        page_articles = display_articles[start_idx:end_idx]
    else:
        page_articles = display_articles
    
    # Display articles
    for i, article in enumerate(page_articles):
        priority = "high" if article in high_priority else ("medium" if article in medium_priority else "regular")
        
        with st.expander(f"{i+1}. {article.get('title', 'Untitled')}", expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Source:** {article.get('source_domain', 'Unknown')}")
                st.write(f"**URL:** [{article.get('url', '#')}]({article.get('url', '#')})")
                st.write(f"**Scraped:** {article.get('scraped_timestamp', 'Unknown')}")
                st.write(f"**Word Count:** {article.get('word_count', 0)}")
                
                # Content preview
                content = article.get('content', '')
                if len(content) > 500:
                    st.write("**Content Preview:**")
                    st.text_area("Content Preview", content[:500] + "...", height=100, disabled=True, key=f"content_{i}", label_visibility="hidden")
                else:
                    st.write("**Full Content:**")
                    st.text_area("Full Content", content, height=150, disabled=True, key=f"full_content_{i}", label_visibility="hidden")
            
            with col2:
                priority_color = "#dc2626" if priority == "high" else ("#f59e0b" if priority == "medium" else "#10b981")
                st.markdown(f"""
                <div style="background: {priority_color}; color: white; padding: 10px; border-radius: 5px; text-align: center;">
                    <strong>Priority: {priority.upper()}</strong>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🔗 Open Article", key=f"open_{i}"):
                    st.markdown(f'<a href="{article.get("url", "#")}" target="_blank">Click here to open</a>', unsafe_allow_html=True)
    
    # Summary information
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Summary")
    
    if summary_data:
        st.sidebar.write(f"**Total Scraped:** {summary_data.get('total_articles', 0)}")
        st.sidebar.write(f"**Scraping Time:** {summary_data.get('scraping_timestamp', 'Unknown')}")
        
        if 'sources_scraped' in summary_data:
            st.sidebar.write("**Sources:**")
            for source in summary_data['sources_scraped']:
                st.sidebar.write(f"• {source}")
    
    st.sidebar.write(f"**Currently Showing:** {len(display_articles)} articles")
    st.sidebar.write(f"**High Priority:** {len(high_priority)}")
    st.sidebar.write(f"**Medium Priority:** {len(medium_priority)}")
    
    # Quick actions
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚡ Quick Actions")
    
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    
    if st.sidebar.button("📊 Run AI Analysis"):
        st.info("Run: `python defense_intelligence.py` to analyze articles with AI")
    
    if st.sidebar.button("🎯 Generate Report"):
        st.info("Run: `python defense_intelligence.py --report` for detailed analysis")

if __name__ == "__main__":
    main()