import sqlite3
conn = sqlite3.connect('tracks.db')
c = conn.cursor()


c.execute('SELECT * FROM tracks')
tracks = c.fetchall()
for track in tracks:
    print(track)

conn.close()
