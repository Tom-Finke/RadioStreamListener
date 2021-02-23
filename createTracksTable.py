
import sqlite3
conn = sqlite3.connect('tracks.db')
c = conn.cursor()

# Create table
c.execute("""CREATE TABLE IF NOT EXISTS tracks  (timestamp text, title text, artist text, album text, year text)""")
conn.commit()
conn.close()
