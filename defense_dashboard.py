#!/usr/bin/env python3
"""
ARGUS Defense Intelligence Dashboard
Specialized dashboard for monitoring defense, security, and terrorism threats.
Real-time threat assessment and intelligence visualization for Indian defense.
"""

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os
import sys
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import threading
import time
import subprocess
import json
from pathlib import Path

# Add the argus_scraper directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'argus_scraper'))

# Real-time monitoring configuration
class RealTimeMonitor:
    def __init__(self):
        self.is_monitoring = False
        self.last_update = datetime.now()
        self.update_interval = 30  # seconds
        
    def start_background_scraping(self):
        """Start background defense news scraping."""
        if not self.is_monitoring:
            self.is_monitoring = True
            # Start defense scraper in background
            try:
                # Get the full path to defense_scraper.py
                script_dir = os.path.dirname(os.path.abspath(__file__))
                scraper_path = os.path.join(script_dir, 'defense_scraper.py')
                
                subprocess.Popen([
                    sys.executable, 
                    scraper_path, 
                    '--monitor'
                ], cwd=script_dir, creationflags=subprocess.CREATE_NEW_CONSOLE)
                return True
            except Exception as e:
                st.error(f"Failed to start background monitoring: {e}")
                return False
        return True
    
    def check_for_new_data(self):
        """Check if new data has been collected."""
        defense_data_dir = Path('defense_data')
        if defense_data_dir.exists():
            # Get latest files
            json_files = list(defense_data_dir.glob('*.json'))
            if json_files:
                latest_file = max(json_files, key=os.path.getctime)
                file_time = datetime.fromtimestamp(os.path.getctime(latest_file))
                return file_time > self.last_update
        return False
    
    def should_refresh(self):
        """Check if dashboard should refresh based on time interval."""
        return (datetime.now() - self.last_update).seconds >= self.update_interval
    
    def update_timestamp(self):
        """Update the last update timestamp."""
        self.last_update = datetime.now()

# Initialize real-time monitor
if 'monitor' not in st.session_state:
    st.session_state.monitor = RealTimeMonitor()

# Configure Streamlit page
st.set_page_config(
    page_title="🛡️ ARGUS Defense Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for defense theme
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
    .threat-high {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        border-left: 6px solid #ffffff;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-radius: 10px;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.4);
    }
    .threat-high h4 {
        color: #ffffff !important;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .threat-high p {
        color: #ffffff !important;
        font-weight: 500;
        margin: 0.3rem 0;
    }
    .threat-high strong {
        color: #ffffff !important;
        font-weight: 700;
    }
    .threat-high a {
        color: #fecaca !important;
        text-decoration: underline;
        font-weight: bold;
    }
    .threat-medium {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        border-left: 6px solid #ffffff;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-radius: 10px;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
    }
    .threat-medium h4 {
        color: #ffffff !important;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .threat-medium p {
        color: #ffffff !important;
        font-weight: 500;
        margin: 0.3rem 0;
    }
    .threat-medium strong {
        color: #ffffff !important;
        font-weight: 700;
    }
    .threat-medium a {
        color: #fed7aa !important;
        text-decoration: underline;
        font-weight: bold;
    }
    .threat-low {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-left: 6px solid #ffffff;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-radius: 10px;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }
    .threat-low h4 {
        color: #ffffff !important;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .threat-low p {
        color: #ffffff !important;
        font-weight: 500;
        margin: 0.3rem 0;
    }
    .threat-low strong {
        color: #ffffff !important;
        font-weight: 700;
    }
    .threat-low a {
        color: #d1fae5 !important;
        text-decoration: underline;
        font-weight: bold;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .live-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: #ef4444;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

def init_defense_db_connection():
    """Initialize connection to defense intelligence database."""
    try:
        conn = sqlite3.connect('defense_intelligence.db')
        return conn
    except sqlite3.Error as e:
        st.error(f"Defense database connection failed: {e}")
        return None

def get_threat_summary():
    """Get threat level summary from database with real-time updates."""
    conn = init_defense_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        
        # Get threat level counts
        cursor.execute('''
            SELECT threat_level, COUNT(*) as count
            FROM articles 
            GROUP BY threat_level
        ''')
        threat_counts = dict(cursor.fetchall())
        
        # Get recent high threats (last 24 hours)
        cursor.execute('''
            SELECT COUNT(*) FROM articles 
            WHERE threat_level = 'HIGH' 
            AND datetime(scraped_timestamp) >= datetime('now', '-24 hours')
        ''')
        recent_high_threats = cursor.fetchone()[0]
        
        # Get total articles today
        cursor.execute('''
            SELECT COUNT(*) FROM articles 
            WHERE date(scraped_timestamp) = date('now')
        ''')
        today_articles = cursor.fetchone()[0]
        
        # Get very recent articles (last hour) for live indicator
        cursor.execute('''
            SELECT COUNT(*) FROM articles 
            WHERE datetime(scraped_timestamp) >= datetime('now', '-1 hour')
        ''')
        last_hour_articles = cursor.fetchone()[0]
        
        # Get latest timestamp to show freshness
        cursor.execute('''
            SELECT MAX(scraped_timestamp) FROM articles
        ''')
        latest_timestamp = cursor.fetchone()[0]
        
        return {
            'threat_counts': threat_counts,
            'recent_high_threats': recent_high_threats,
            'today_articles': today_articles,
            'last_hour_articles': last_hour_articles,
            'latest_timestamp': latest_timestamp,
            'refresh_time': datetime.now().strftime('%H:%M:%S')
        }
        
    except sqlite3.Error as e:
        st.error(f"Error fetching threat summary: {e}")
        return None
    finally:
        conn.close()

def get_defense_alerts():
    """Get recent defense alerts."""
    conn = init_defense_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.title, a.url, da.alert_level, da.alert_description, 
                   da.created_timestamp, a.threat_level
            FROM defense_alerts da
            JOIN articles a ON da.article_id = a.id
            ORDER BY da.created_timestamp DESC
            LIMIT 10
        ''')
        
        alerts = cursor.fetchall()
        return alerts
        
    except sqlite3.Error as e:
        st.error(f"Error fetching alerts: {e}")
        return []
    finally:
        conn.close()

def get_defense_entities():
    """Get defense-specific entities."""
    conn = init_defense_db_connection()
    if not conn:
        return {}
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT type, text, COUNT(*) as frequency
            FROM entities 
            WHERE entity_category = 'DEFENSE'
            GROUP BY type, text
            ORDER BY frequency DESC
        ''')
        
        entities = cursor.fetchall()
        
        # Group by type
        grouped = {}
        for entity_type, text, frequency in entities:
            if entity_type not in grouped:
                grouped[entity_type] = []
            grouped[entity_type].append((text, frequency))
        
        return grouped
        
    except sqlite3.Error as e:
        st.error(f"Error fetching defense entities: {e}")
        return {}
    finally:
        conn.close()

def get_threat_timeline():
    """Get threat timeline data for visualization."""
    conn = init_defense_db_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT date(scraped_timestamp) as date, 
                   threat_level, 
                   COUNT(*) as count
            FROM articles 
            WHERE scraped_timestamp >= datetime('now', '-30 days')
            GROUP BY date(scraped_timestamp), threat_level
            ORDER BY date
        ''')
        
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=['date', 'threat_level', 'count'])
        return df
        
    except sqlite3.Error as e:
        st.error(f"Error fetching timeline data: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def main():
    """Main defense dashboard application."""
    
    # Auto-refresh mechanism
    monitor = st.session_state.monitor
    
    # Create placeholder for auto-refresh
    if 'refresh_placeholder' not in st.session_state:
        st.session_state.refresh_placeholder = st.empty()
    
    # Force refresh if new data detected or time interval reached
    should_refresh = monitor.should_refresh() or monitor.check_for_new_data()
    
    if should_refresh:
        # Clear all cached data for fresh results
        if hasattr(st, 'cache_data'):
            st.cache_data.clear()
        
        # Update timestamp and increment refresh counter
        monitor.update_timestamp()
        if 'refresh_count' not in st.session_state:
            st.session_state.refresh_count = 0
        st.session_state.refresh_count += 1
        
        # Trigger rerun for fresh data
        if st.session_state.refresh_count > 1:  # Avoid infinite loops
            time.sleep(0.5)  # Small delay to prevent rapid refreshes
            st.rerun()
    
    # Header with live status
    current_time = datetime.now().strftime('%H:%M:%S')
    st.markdown(f"""
    <div class="defense-header">
        <h1>🛡️ ARGUS Defense Intelligence Dashboard</h1>
        <p>Real-time threat monitoring and intelligence analysis for Indian national security</p>
        <p style="font-size: 0.9rem; margin-top: 10px;">🔴 LIVE • Last Update: {current_time}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if defense database exists
    if not os.path.exists('defense_intelligence.db'):
        st.warning("⚠️ No defense intelligence database found.")
        st.info("""
        To get started with defense intelligence:
        1. Run: `python defense_scraper.py` to collect defense news
        2. Run: `python defense_intelligence.py` to analyze threats
        3. Refresh this dashboard
        """)
        
        # Quick start buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Start Defense News Collection", type="primary"):
                st.info("Please run: `python defense_scraper.py` in your terminal")
        
        with col2:
            if st.button("📊 Analyze Collected Data"):
                st.info("Please run: `python defense_intelligence.py` in your terminal")
        
        return
    
    # Sidebar controls with live monitoring
    st.sidebar.header("🎯 Defense Intelligence Controls")
    
    # Live monitoring controls
    st.sidebar.subheader("🔴 Live Monitoring")
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox(
        "Enable Auto-Refresh (30s)", 
        value=True,
        help="Automatically refresh dashboard every 30 seconds"
    )
    
    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Now", type="primary"):
        monitor.update_timestamp()
        st.cache_data.clear()
        st.rerun()
    
    # Start/Stop live monitoring
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🚀 Start Live Monitor"):
            if monitor.start_background_scraping():
                st.success("Live monitoring started!")
                time.sleep(1)
                st.rerun()
    
    with col2:
        if st.button("⏹️ Process New Data"):
            try:
                # Process any new JSON files using our quick processor
                script_dir = os.path.dirname(os.path.abspath(__file__))
                quick_processor_path = os.path.join(script_dir, 'quick_data_processor.py')
                
                result = subprocess.run([
                    sys.executable, 
                    quick_processor_path
                ], cwd=script_dir, capture_output=True, text=True, encoding='utf-8')
                
                if result.returncode == 0:
                    st.success("Data processed successfully!")
                    st.cache_data.clear()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Processing failed: {result.stderr}")
            except Exception as e:
                st.error(f"Failed to process data: {e}")
    
    # Live status indicators
    st.sidebar.markdown("---")
    new_data_available = monitor.check_for_new_data()
    if new_data_available:
        st.sidebar.markdown("🟢 **New data detected!**")
        st.sidebar.button("Process Now", key="process_new")
    else:
        st.sidebar.markdown("🟡 **System monitoring...**")
    
    # Threat level filter
    threat_filter = st.sidebar.selectbox(
        "Filter by Threat Level:",
        ["All", "HIGH", "MEDIUM", "LOW"]
    )
    
    # Time range filter
    time_range = st.sidebar.selectbox(
        "Time Range:",
        ["Last 24 hours", "Last 7 days", "Last 30 days", "All time"]
    )
    
    # Refresh button
    if st.sidebar.button("🔄 Refresh Intelligence"):
        st.cache_data.clear()
        st.rerun()
    
    # Main dashboard content
    
    # Threat Summary Metrics with manual refresh option
    col_header1, col_header2 = st.columns([3, 1])
    with col_header1:
        st.subheader("🚨 Threat Assessment Overview")
    with col_header2:
        if st.button("🔄 Refresh Metrics", key="refresh_metrics"):
            st.cache_data.clear()
            st.rerun()
    
    # Force fresh data fetch on every refresh
    if 'force_refresh' not in st.session_state:
        st.session_state.force_refresh = 0
    
    # Clear any cached data to ensure fresh results
    if hasattr(st, 'cache_data'):
        st.cache_data.clear()
    
    threat_summary = get_threat_summary()
    if threat_summary:
        # Display last refresh time
        st.caption(f"🔄 Last refreshed: {threat_summary['refresh_time']} | Latest data: {threat_summary.get('latest_timestamp', 'N/A')[:16] if threat_summary.get('latest_timestamp') else 'N/A'}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            high_threats = threat_summary['threat_counts'].get('HIGH', 0)
            delta_text = f"+{threat_summary['recent_high_threats']} (24h)"
            if threat_summary['last_hour_articles'] > 0:
                delta_text += f" | +{threat_summary['last_hour_articles']} (1h) 🔴"
            st.metric(
                "🔴 High Threats",
                high_threats,
                delta=delta_text
            )
        
        with col2:
            medium_threats = threat_summary['threat_counts'].get('MEDIUM', 0)
            st.metric(
                "🟡 Medium Threats",
                medium_threats
            )
        
        with col3:
            low_threats = threat_summary['threat_counts'].get('LOW', 0)
            st.metric(
                "🟢 Low Threats",
                low_threats
            )
        
        with col4:
            st.metric(
                "📰 Today's Articles",
                threat_summary['today_articles'],
                delta=f"+{threat_summary['last_hour_articles']} this hour" if threat_summary['last_hour_articles'] > 0 else None
            )
        
        # Show live data indicator if new data detected
        if threat_summary['last_hour_articles'] > 0:
            st.success(f"🟢 **LIVE DATA:** {threat_summary['last_hour_articles']} new articles detected in the last hour!")
    else:
        st.warning("No threat data available. Waiting for live monitoring data...")
    
    # Threat Timeline Visualization
    st.subheader("📈 Threat Timeline (Last 30 Days)")
    
    timeline_df = get_threat_timeline()
    if not timeline_df.empty:
        fig = px.line(
            timeline_df, 
            x='date', 
            y='count', 
            color='threat_level',
            title="Daily Threat Levels",
            color_discrete_map={
                'HIGH': '#dc2626',
                'MEDIUM': '#f59e0b', 
                'LOW': '#10b981'
            }
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Number of Articles",
            legend_title="Threat Level"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No timeline data available yet.")
    
    # Recent Defense Alerts
    st.markdown("""
    <div style="background: linear-gradient(90deg, #dc2626 0%, #b91c1c 100%); 
                color: white; padding: 15px; border-radius: 10px; margin: 15px 0; 
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
        <h2 style="color: white; margin: 0; font-size: 1.5rem;">🚨 Recent Defense Alerts</h2>
        <p style="color: #fecaca; margin: 5px 0 0 0; font-size: 0.9rem;">Live security incidents and threat notifications</p>
    </div>
    """, unsafe_allow_html=True)
    
    alerts = get_defense_alerts()
    if alerts:
        for alert in alerts[:5]:  # Show top 5 alerts
            title, url, alert_level, description, timestamp, threat_level = alert
            
            # Style alert based on level
            if alert_level == 'HIGH':
                alert_class = "threat-high"
                icon = "🔴"
            elif alert_level == 'MEDIUM':
                alert_class = "threat-medium"
                icon = "🟡"
            else:
                alert_class = "threat-low"
                icon = "🟢"
            
            st.markdown(f"""
            <div class="{alert_class}">
                <h4>{icon} {title}</h4>
                <p><strong>Alert Level:</strong> {alert_level}</p>
                <p><strong>Description:</strong> {description}</p>
                <p><strong>Time:</strong> {timestamp}</p>
                <p><strong>Source:</strong> <a href="{url}" target="_blank">View Article</a></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No defense alerts at this time.")
    
    # Defense Entities Analysis
    st.subheader("🎯 Defense Intelligence Entities")
    
    entities = get_defense_entities()
    if entities:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🪖 Military Units Detected:**")
            if 'MILITARY_UNIT' in entities:
                for unit, freq in entities['MILITARY_UNIT'][:10]:
                    st.write(f"• {unit} ({freq} mentions)")
            else:
                st.info("No military units detected yet.")
        
        with col2:
            st.write("**🔫 Weapons & Equipment:**")
            if 'WEAPON' in entities:
                for weapon, freq in entities['WEAPON'][:10]:
                    st.write(f"• {weapon} ({freq} mentions)")
            else:
                st.info("No weapons detected yet.")
    
    # Recent High-Priority Articles
    st.subheader("📋 High-Priority Intelligence Reports")
    
    conn = init_defense_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT title, url, threat_level, relevance_score, 
                       detected_categories, scraped_timestamp
                FROM articles 
                WHERE threat_level IN ('HIGH', 'MEDIUM')
                ORDER BY relevance_score DESC, scraped_timestamp DESC
                LIMIT 10
            ''')
            
            high_priority = cursor.fetchall()
            
            if high_priority:
                for article in high_priority:
                    title, url, threat_level, score, categories, timestamp = article
                    
                    with st.expander(f"{'🔴' if threat_level == 'HIGH' else '🟡'} {title}"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**Threat Level:** {threat_level}")
                            st.write(f"**Relevance Score:** {score}/100")
                            if categories:
                                st.write(f"**Categories:** {categories}")
                            st.write(f"**Time:** {timestamp}")
                        
                        with col2:
                            st.link_button("🔗 View Article", url)
            else:
                st.info("No high-priority articles found.")
                
        except sqlite3.Error as e:
            st.error(f"Error fetching articles: {e}")
        finally:
            conn.close()
    
    # System Status
    st.sidebar.markdown("---")
    st.sidebar.subheader("🖥️ System Status")
    
    # Database status
    db_status = "✅ Connected" if os.path.exists('defense_intelligence.db') else "❌ Not Found"
    st.sidebar.write(f"**Database:** {db_status}")
    
    # Articles count
    if threat_summary:
        total_articles = sum(threat_summary['threat_counts'].values())
        st.sidebar.write(f"**Total Articles:** {total_articles}")
    
    # Last update time
    st.sidebar.write(f"**Last Update:** {datetime.now().strftime('%H:%M:%S')}")
    
    # Quick Actions
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚡ Quick Actions")
    
    if st.sidebar.button("🎯 Generate Defense Report"):
        st.info("Run: `python defense_intelligence.py --report` for detailed analysis")
    
    if st.sidebar.button("🔍 Start Monitoring"):
        st.info("Run: `python defense_scraper.py --monitor` for continuous monitoring")
    
    # Intelligence Sources
    st.sidebar.markdown("---")
    st.sidebar.subheader("📡 Intelligence Sources")
    st.sidebar.write("""
    **Indian Sources:**
    • Indian Defence News
    • Economic Times Defence
    • Hindustan Times
    • Times of India
    
    **International:**
    • BBC Security
    • Reuters World
    • CNN International
    """)
    
    # Auto-refresh implementation
    if auto_refresh:
        # Create a placeholder for the refresh timer
        refresh_placeholder = st.sidebar.empty()
        
        # Display countdown timer
        if 'last_refresh_time' not in st.session_state:
            st.session_state.last_refresh_time = time.time()
        
        elapsed = time.time() - st.session_state.last_refresh_time
        remaining = max(0, 30 - int(elapsed))
        
        refresh_placeholder.metric(
            "⏱️ Next Refresh", 
            f"{remaining}s",
            delta="Auto-refresh enabled"
        )
        
        # Auto-refresh trigger
        if elapsed >= 30:
            st.session_state.last_refresh_time = time.time()
            monitor.update_timestamp()
            st.rerun()

if __name__ == "__main__":
    main()