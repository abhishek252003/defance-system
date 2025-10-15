import sqlite3
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('defense_intelligence.db')
cursor = conn.cursor()

# Get total articles
cursor.execute('SELECT COUNT(*) FROM articles')
total_articles = cursor.fetchone()[0]
print(f"Total articles in database: {total_articles}")

# Get today's articles (using the date from the system)
today = datetime.now().strftime('%Y-%m-%d')
cursor.execute("SELECT COUNT(*) FROM articles WHERE date(scraped_timestamp) = ?", (today,))
todays_articles = cursor.fetchone()[0]
print(f"Today's articles ({today}): {todays_articles}")

# Get articles by threat level
cursor.execute("SELECT threat_level, COUNT(*) FROM articles GROUP BY threat_level")
threat_levels = cursor.fetchall()
print("\nArticles by threat level:")
for level, count in threat_levels:
    print(f"  {level}: {count}")

# Get recent high-threat articles
cursor.execute("SELECT title, url, scraped_timestamp FROM articles WHERE threat_level = 'HIGH' ORDER BY scraped_timestamp DESC LIMIT 5")
high_threat_articles = cursor.fetchall()
print("\nRecent high-threat articles:")
for title, url, timestamp in high_threat_articles:
    print(f"  {title[:50]}... ({timestamp[:16]})")

# Close connection
conn.close()