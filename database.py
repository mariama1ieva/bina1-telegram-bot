import sqlite3

conn = sqlite3.connect("ads.db")
conn.execute("CREATE TABLE IF NOT EXISTS ads (url TEXT PRIMARY KEY)")

def is_new(url):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM ads WHERE url=?", (url,))
    if cur.fetchone():
        return False
    cur.execute("INSERT INTO ads VALUES (?)", (url,))
    conn.commit()
    return True
