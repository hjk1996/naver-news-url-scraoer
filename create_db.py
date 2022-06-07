import sqlite3

if __name__ == "__main__":

    conn = sqlite3.connect("news_ovierviews.db", isolation_level=None)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS table1 (id integer PRIMARY KEY, press text, link text, title text)")