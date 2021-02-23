import sqlite3
import requests
import time
import json


def returnTitleAndArtist(track):
    if(len(track[0].split('-')) == 2):
        return [part.strip() for part in track[0].split('-')][::-1]
    else:  # Either Trackname and Artist are Correct or something weird is going on
        return [track[0], track[1]]


def findExists(trackToCheck, prevTracks=[], databaseCursor=False):
    previousTracks = []
    if(len(prevTracks) > 0):
        previousTracks += [returnTitleAndArtist(track) for track in prevTracks]
    if(databaseCursor != False):
        databaseCursor.execute('SELECT title, artist FROM tracks')
        previousTracks += databaseCursor.fetchall()
    if(returnTitleAndArtist(trackToCheck) in previousTracks):
        return True
    else:
        return False


def downloadAudio(stram_url, duration=15, outputFile="stream.mp3"):
    r = requests.get(stram_url, stream=True)
    with open(outputFile, 'wb') as f:
        counter = 0
        # 1000 blocks ~ 63 s, 10-30s of audio are optimal according to https://user.audiotag.info/c
        for block in r.iter_content(1024):
            if(counter < duration * 15):
                f.write(block)
                counter += 1
            else:
                break
    return outputFile


def triggerParseSong(apikey, filepath,
                     api_url='https://audiotag.info/api'):
    payload = {'action': 'identify', 'apikey': apikey}
    result = requests.post(api_url, data=payload, files={
        'file': open(filepath, 'rb')})
    return result.json()['token']


def fetchParseResult(token, apikey, api_url='https://audiotag.info/api'):
    payload = {'action': 'get_result', 'apikey': apikey, 'token': token}
    result = requests.post(api_url, data=payload).json()

    while(result["result"] == "wait"):
        time.sleep(2)
        result = requests.post(api_url, data=payload).json()
    return result


def insertSongsIntoDatabase(tracks, databaseCursor):
    databaseCursor.executemany(
        "INSERT INTO tracks VALUES (strftime('%Y-%m-%d %H:%M:%S','now'),?,?,?,?)", tracks)


if __name__ == "__main__":
    conn = sqlite3.connect('tracks.db')
    c = conn.cursor()
    print(findExists(["TestArtist - TestTitle", "Album"], [
        ["TestTitle", "TestArtist"]], False))

    print(findExists(["TestTitle", "TestArtist"], [
        ["TestTitle", "TestArtist"]], False))
