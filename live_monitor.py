#!/usr/bin/env python3
"""
ARGUS Live Defense Intelligence Monitor
Continuously monitors defense news sources and updates the dashboard in real-time.
"""

import time
import subprocess
import sys
import os
import threading
import sqlite3
from datetime import datetime
from pathlib import Path
import json

class LiveDefenseMonitor:
    def __init__(self):
        self.is_running = False
        self.scraper_process = None
        self.last_data_check = datetime.now()
        self.data_dir = Path('defense_data')
        
    def check_new_data_files(self):
        """Check for new JSON files that need processing."""
        if not self.data_dir.exists():
            return False
            
        json_files = list(self.data_dir.glob('*.json'))
        if not json_files:
            return False
            
        # Check if any files are newer than last check
        for file in json_files:
            if datetime.fromtimestamp(file.stat().st_mtime) > self.last_data_check:
                return True
        return False
    
    def process_new_data(self):
        """Process new defense data files."""
        try:
            print("📊 Processing new defense intelligence data...")
            result = subprocess.run([
                sys.executable, 
                'defense_intelligence.py'
            ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
            
            if result.returncode == 0:
                print("✅ Data processing completed successfully")
                self.last_data_check = datetime.now()
                return True
            else:
                print(f"❌ Data processing failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error processing data: {e}")
            return False
    
    def start_scraper(self):
        """Start the defense scraper in monitor mode."""
        try:
            print("🔍 Starting defense news scraper...")
            self.scraper_process = subprocess.Popen([
                sys.executable, 
                'defense_scraper.py', 
                '--monitor'
            ], cwd=os.path.dirname(__file__))
            
            print("✅ Defense scraper started in background")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start scraper: {e}")
            return False
    
    def stop_scraper(self):
        """Stop the defense scraper."""
        if self.scraper_process:
            try:
                self.scraper_process.terminate()
                self.scraper_process.wait(timeout=10)
                print("🛑 Defense scraper stopped")
            except Exception as e:
                print(f"⚠️ Error stopping scraper: {e}")
                try:
                    self.scraper_process.kill()
                except:
                    pass
    
    def get_database_stats(self):
        """Get current database statistics."""
        db_path = 'defense_intelligence.db'
        if not os.path.exists(db_path):
            return None
            
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get article count
            cursor.execute("SELECT COUNT(*) FROM articles")
            total_articles = cursor.fetchone()[0]
            
            # Get threat level distribution
            cursor.execute("""
                SELECT threat_level, COUNT(*) 
                FROM articles 
                GROUP BY threat_level
            """)
            threat_dist = dict(cursor.fetchall())
            
            # Get recent articles (last hour)
            cursor.execute("""
                SELECT COUNT(*) FROM articles 
                WHERE datetime(scraped_timestamp) >= datetime('now', '-1 hour')
            """)
            recent_articles = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_articles': total_articles,
                'threat_distribution': threat_dist,
                'recent_articles': recent_articles
            }
            
        except Exception as e:
            print(f"Error getting database stats: {e}")
            return None
    
    def monitor_loop(self):
        """Main monitoring loop."""
        print("🛡️ ARGUS Live Defense Intelligence Monitor")
        print("=" * 50)
        
        # Start scraper
        if not self.start_scraper():
            return False
        
        self.is_running = True
        cycle_count = 0
        
        try:
            while self.is_running:
                cycle_count += 1
                current_time = datetime.now().strftime('%H:%M:%S')
                
                print(f"\n⏰ [{current_time}] Monitor Cycle #{cycle_count}")
                
                # Check for new data
                if self.check_new_data_files():
                    print("🆕 New defense data detected!")
                    if self.process_new_data():
                        print("✅ Intelligence database updated")
                    else:
                        print("⚠️ Failed to process new data")
                else:
                    print("📡 No new data detected")
                
                # Display current statistics
                stats = self.get_database_stats()
                if stats:
                    print(f"📊 Database Stats:")
                    print(f"   Total Articles: {stats['total_articles']}")
                    print(f"   Recent (1h): {stats['recent_articles']}")
                    threat_dist = stats['threat_distribution']
                    if threat_dist:
                        print(f"   Threats: HIGH={threat_dist.get('HIGH', 0)} " +
                              f"MEDIUM={threat_dist.get('MEDIUM', 0)} " +
                              f"LOW={threat_dist.get('LOW', 0)}")
                
                print(f"💤 Waiting 60 seconds until next check...")
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            print("\n🛑 Monitor stopped by user")
        except Exception as e:
            print(f"\n❌ Monitor error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the monitoring system."""
        self.is_running = False
        self.stop_scraper()
        print("👋 Live monitoring system stopped")

def main():
    """Main function to start live monitoring."""
    monitor = LiveDefenseMonitor()
    
    print("🚀 Starting ARGUS Live Defense Intelligence Monitoring...")
    print("Press Ctrl+C to stop monitoring\n")
    
    try:
        monitor.monitor_loop()
    except KeyboardInterrupt:
        print("\n🛑 Monitoring interrupted by user")
    finally:
        monitor.stop()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("""
ARGUS Live Defense Intelligence Monitor

This script provides real-time monitoring of defense news sources
and automatically updates the intelligence dashboard.

Usage:
    python live_monitor.py           # Start live monitoring
    python live_monitor.py --help    # Show this help

Features:
- Continuous defense news scraping
- Automatic data processing
- Real-time database updates
- Dashboard-compatible output
- Statistics monitoring

The script will:
1. Start defense news scraper in background
2. Monitor for new data files
3. Process new intelligence data
4. Update the defense database
5. Display live statistics

Use Ctrl+C to stop monitoring gracefully.
        """)
    else:
        main()