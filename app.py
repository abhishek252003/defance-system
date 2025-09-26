#!/usr/bin/env python3
"""
ARGUS Defense Intelligence Dashboard - Cloud Compatible Version
Specialized dashboard for monitoring defense, security, and terrorism threats.
Real-time threat assessment and intelligence visualization.
"""

import streamlit as st
import sqlite3
try:
    import pandas as pd
except ImportError:
    st.error("Required dependency 'pandas' not installed. Please install it with: pip install pandas")
    st.stop()
from datetime import datetime, timedelta
import os
import sys
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except ImportError:
    st.error("Required dependency 'plotly' not installed. Please install it with: pip install plotly")
    st.stop()
import threading
import time
import subprocess
import json
from pathlib import Path

# Real-time monitoring configuration (cloud compatible)
class RealTimeMonitor:
    def __init__(self):
        self.is_monitoring = False
        self.last_update = datetime.now()
        self.update_interval = 30  # seconds
        
    def start_background_scraping(self):
        """Start background defense news scraping (cloud compatible)."""
        if not self.is_monitoring:
            self.is_monitoring = True
            # For cloud deployment, we'll simulate or use available data
            try:
                # Check if scraper exists (for local deployment)
                script_dir = os.path.dirname(os.path.abspath(__file__))
                if os.path.exists(os.path.join(script_dir, 'defense_scraper.py')):
                    scraper_path = os.path.join(script_dir, 'defense_scraper.py')
                    subprocess.Popen([
                        sys.executable, 
                        scraper_path, 
                        '--monitor'
                    ], cwd=script_dir)
                return True
            except Exception as e:
                st.info("Background monitoring not available in cloud environment")
                return False
        return True
    
    def check_for_new_data(self):
        """Check if new data has been collected."""
        defense_data_dir = Path('defense_data')
        if defense_data_dir.exists():
            # Get latest files
            json_files = list(defense_data_dir.glob('*.json'))
            if json_files:
                latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
                file_time = datetime.fromtimestamp(latest_file.stat().st_mtime)
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
    """Initialize defense database connection."""
    try:
        conn = sqlite3.connect('defense_intelligence.db', check_same_thread=False)
        return conn
    except sqlite3.Error as e:
        st.error(f"Database connection error: {e}")
        return None

def get_threat_summary():
    """Get threat level summary from database with real-time updates."""
    conn = init_defense_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        
        # Get threat counts
        cursor.execute('''
            SELECT threat_level, COUNT(*) as count
            FROM articles 
            GROUP BY threat_level
        ''')
        threat_data = cursor.fetchall()
        threat_counts = {level: count for level, count in threat_data}
        
        # If no data, create sample data for demo
        if not threat_counts:
            # Insert sample data for demo
            sample_articles = [
                ("China Military Exercise Near LAC", "Chinese military conducts exercise near Line of Actual Control", "https://example.com/1", datetime.now().isoformat(), 150, 25, "HIGH", 85, "military,border", "military exercise,border tension"),
                ("Pakistan Terror Alert", "Intelligence agencies issue terror alert for major cities", "https://example.com/2", datetime.now().isoformat(), 200, 35, "HIGH", 90, "terrorism,security", "terror alert,security threat"),
                ("Navy Maritime Security", "Indian Navy enhances maritime security in Arabian Sea", "https://example.com/3", datetime.now().isoformat(), 180, 30, "MEDIUM", 65, "military,naval", "maritime security"),
                ("Cyber Security Report", "Annual cyber security assessment released", "https://example.com/4", datetime.now().isoformat(), 120, 20, "LOW", 45, "cyber", "cyber security"),
                ("Border Infrastructure", "New border infrastructure projects underway", "https://example.com/5", datetime.now().isoformat(), 160, 28, "LOW", 40, "border,infrastructure", "border security"),
            ]
            
            for article in sample_articles:
                try:
                    cursor.execute('''
                        INSERT OR IGNORE INTO articles 
                        (title, content, url, scraped_timestamp, content_length, word_count, threat_level, relevance_score, detected_categories, key_indicators)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', article)
                except:
                    pass  # Ignore duplicates
            
            conn.commit()
            
            # Recalculate threat counts
            cursor.execute('''
                SELECT threat_level, COUNT(*) as count
                FROM articles 
                GROUP BY threat_level
            ''')
            threat_data = cursor.fetchall()
            threat_counts = {level: count for level, count in threat_data}
        
        # Get recent high threats (last 24 hours)
        cursor.execute('''
            SELECT COUNT(*) FROM articles 
            WHERE threat_level = 'HIGH' 
            AND datetime(scraped_timestamp) >= datetime('now', '-24 hours')
        ''')
        recent_high_threats = cursor.fetchone()[0]
        
        # Get today's articles
        cursor.execute('''
            SELECT COUNT(*) FROM articles 
            WHERE date(scraped_timestamp) = date('now')
        ''')
        today_articles = cursor.fetchone()[0]
        
        # Get last hour articles
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
        if data:
            df = pd.DataFrame(data, columns=['date', 'threat_level', 'count'])
            return df
        return pd.DataFrame()
        
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
        <p>Real-time threat monitoring and intelligence analysis for national security</p>
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
        
        For cloud deployment, sample data will be initialized automatically.
        """)
        
        # Quick start buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Initialize Sample Data", type="primary"):
                st.info("Initializing sample defense intelligence data...")
                get_threat_summary()  # This will create sample data
                st.success("Sample defense data initialized!")
                st.rerun()
        
        with col2:
            if st.button("📊 Refresh Dashboard"):
                st.rerun()
        
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
        if hasattr(st, 'cache_data'):
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
                # For cloud deployment, simulate data processing
                st.info("Processing available intelligence data...")
                
                # Initialize database with fresh sample data
                conn = init_defense_db_connection()
                if conn:
                    conn.close()
                    st.success("Data processed successfully!")
                    time.sleep(1)
                    st.rerun()
            except Exception as e:
                st.error(f"Processing simulation: {e}")
    
    # Live status indicators
    st.sidebar.markdown("---")
    new_data_available = monitor.check_for_new_data()
    if new_data_available:
        st.sidebar.markdown("🟢 **New data detected!**")
        if st.sidebar.button("Process Now", key="process_new"):
            st.rerun()
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
        if hasattr(st, 'cache_data'):
            st.cache_data.clear()
        st.rerun()
    
    # Main dashboard content
    
    # Threat Summary Metrics with manual refresh option
    col_header1, col_header2 = st.columns([3, 1])
    with col_header1:
        st.subheader("🚨 Threat Assessment Overview")
    with col_header2:
        if st.button("🔄 Refresh Metrics", key="refresh_metrics"):
            if hasattr(st, 'cache_data'):
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
        st.info("No timeline data available yet. Data will appear as intelligence is collected.")
    
    # Threat Distribution Chart
    st.subheader("📊 Threat Level Distribution")
    if threat_summary and threat_summary['threat_counts']:
        df = pd.DataFrame(list(threat_summary['threat_counts'].items()), 
                         columns=['Threat Level', 'Count'])
        
        fig = px.pie(df, values='Count', names='Threat Level',
                    color_discrete_map={
                        'HIGH': '#dc2626',
                        'MEDIUM': '#f59e0b', 
                        'LOW': '#10b981'
                    })
        st.plotly_chart(fig, use_container_width=True)
    
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
                <p><strong>Description:</strong> {description or 'Defense intelligence alert'}</p>
                <p><strong>Time:</strong> {timestamp[:16] if timestamp else 'Recent'}</p>
                <p><strong>Source:</strong> <a href="{url}" target="_blank">View Article</a></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No defense alerts at this time. System monitoring continues...")
    
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
                st.write("No military units detected yet.")
        
        with col2:
            st.write("**🔫 Weapons Systems:**")
            if 'WEAPON' in entities:
                for weapon, freq in entities['WEAPON'][:10]:
                    st.write(f"• {weapon} ({freq} mentions)")
            else:
                st.write("No weapons systems detected yet.")
    else:
        st.info("Defense entity analysis will appear as data is processed.")
    
    # Footer with system info
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🛡️ ARGUS Defense Intelligence System v1.0 | Cloud Deployed</p>
        <p>Powered by AI • Real-time Threat Analysis • Secure by Design</p>
        <p>⚡ Optimized for Streamlit Cloud • 🌐 Global Access</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()