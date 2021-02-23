import requests
import requests
import json
import time
import sqlite3
import helperFunctions

conn = sqlite3.connect('tracks.db')
c = conn.cursor()

# Step 0: set parameters
# Wether or not to insert tracks into the database that have already been inserted

apikey = open("apikey.txt").readline().rstrip()
reinsert = False

# Step 0.5: Helper Functions

# Sometimes a Trackname ist just the Track Name. Sometimes, it is "Artistname - Trackname"
# E.G. "Licence To Kill" and "Gladys Knight - Licence To Kill"

# Step 1: Download Audio Snippet from Stream and save to file
# 1000 blocks ~ 63 s, 10-30s of audio are optimal according to https://user.audiotag.info/
stream_url = 'http://62.138.23.169:8000/smartradio.mp3'

outfile = helperFunctions.downloadAudio(stream_url)

# Step 2: request the identification of the song
token = helperFunctions.triggerParseSong(apikey, outfile)

# Step 3: Fetch the result with the token
result = helperFunctions.fetchParseResult(token, apikey)

tracks = []


if(result["result"] == "found"):
    for data in result['data']:
        for result_track in data["tracks"]:
            if(not helperFunctions.findExists(result_track, tracks, False if reinsert else c)):
                tracks.append(helperFunctions.returnTitleAndArtist(
                    result_track) + result_track[2:])
print(tracks)
c.execute('''CREATE TABLE IF NOT EXISTS tracks 
             (created timestamp with timezone, title text, artist text, album text, year text)''')


helperFunctions.insertSongsIntoDatabase(tracks, c)

conn.commit()
conn.close()
