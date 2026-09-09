import sqlite3

conn = sqlite3.connect("samyakavlokan.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS events(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    event_type TEXT,
    person_count INTEGER,
    alert_status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS live_stats(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_count INTEGER,
    object_count INTEGER
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")