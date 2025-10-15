import sqlite3
from datetime import datetime

def generate_todays_defense_report():
    """Generate a comprehensive report of today's defense intelligence."""
    # Connect to the database
    conn = sqlite3.connect('defense_intelligence.db')
    cursor = conn.cursor()
    
    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')
    
    print("=" * 80)
    print(f"🛡️ ARGUS DEFENSE INTELLIGENCE REPORT - {today}")
    print("=" * 80)
    
    # Get today's articles count
    cursor.execute("SELECT COUNT(*) FROM articles WHERE date(scraped_timestamp) = ?", (today,))
    todays_articles = cursor.fetchone()[0]
    print(f"📰 Total articles collected today: {todays_articles}")
    
    # Get today's articles by threat level
    cursor.execute("""
        SELECT threat_level, COUNT(*) 
        FROM articles 
        WHERE date(scraped_timestamp) = ? 
        GROUP BY threat_level
    """, (today,))
    threat_levels = cursor.fetchall()
    
    print("\n⚠️  TODAY'S THREAT LEVEL DISTRIBUTION:")
    for level, count in threat_levels:
        print(f"   {level}: {count}")
    
    # Get today's high-threat articles
    cursor.execute("""
        SELECT title, url, threat_level, relevance_score, detected_categories
        FROM articles 
        WHERE date(scraped_timestamp) = ? AND threat_level = 'HIGH'
        ORDER BY relevance_score DESC
        LIMIT 10
    """, (today,))
    high_threat_articles = cursor.fetchall()
    
    print(f"\n🔴 TOP HIGH-THREAT ARTICLES TODAY:")
    for i, (title, url, threat_level, score, categories) in enumerate(high_threat_articles, 1):
        print(f"   {i}. {title[:60]}...")
        print(f"      Threat Level: {threat_level} | Score: {score}/100")
        print(f"      Categories: {categories}")
        print(f"      URL: {url[:70]}...")
        print()
    
    # Get today's defense entities
    cursor.execute("""
        SELECT e.type, e.text, COUNT(*) as frequency
        FROM entities e
        JOIN articles a ON e.article_id = a.id
        WHERE date(a.scraped_timestamp) = ? AND e.entity_category = 'DEFENSE'
        GROUP BY e.type, e.text
        ORDER BY frequency DESC
        LIMIT 15
    """, (today,))
    defense_entities = cursor.fetchall()
    
    print("🎯 TODAY'S DEFENSE ENTITIES:")
    military_units = [(text, freq) for etype, text, freq in defense_entities if etype == 'MILITARY_UNIT']
    weapons = [(text, freq) for etype, text, freq in defense_entities if etype == 'WEAPON']
    
    if military_units:
        print("   🪖 Military Units:")
        for unit, freq in military_units[:5]:
            print(f"      • {unit} ({freq} mentions)")
    
    if weapons:
        print("   🔫 Weapons Systems:")
        for weapon, freq in weapons[:5]:
            print(f"      • {weapon} ({freq} mentions)")
    
    # Get today's defense alerts
    cursor.execute("""
        SELECT a.title, da.alert_level, da.alert_description
        FROM defense_alerts da
        JOIN articles a ON da.article_id = a.id
        WHERE date(a.scraped_timestamp) = ?
        ORDER BY da.created_timestamp DESC
        LIMIT 5
    """, (today,))
    alerts = cursor.fetchall()
    
    if alerts:
        print(f"\n🚨 TODAY'S DEFENSE ALERTS:")
        for title, alert_level, description in alerts:
            print(f"   🔴 {title[:50]}...")
            print(f"      Alert Level: {alert_level}")
            print(f"      Description: {description[:60]}...")
            print()
    
    # Close connection
    conn.close()
    
    print("=" * 80)
    print("🛡️ END OF DEFENSE INTELLIGENCE REPORT")
    print("=" * 80)

if __name__ == "__main__":
    generate_todays_defense_report()