# RadioStreamListener

An application to listen to a radio stream and save the song information for later repurpose (e.g. add to a downloadable playlist)

The downloadSongs.py Script listens to a given radio Stream on the Internet.
It then makes API calls to get the name of the played song(s)

This is nothing advanced, I just implemented this in like an hour. And I guess im not that good of a programmer anyways. But it does the job, I hope.

# Usage

## 1. Register for API

You have to create an Account at https://audiotag.info/
Create an API Token and save it in apikey.txt
With their free plan, you get 10000s of free recognition per month. If you use 8s snippets (I have to do some more testing in order to confirm that thats enough in most cases), you would be able to analyse 1250 songs monthly, or 1 song every 35 Minutes.
Because this may not be sufficient, im currently looking for good, open source alternatives to audiotag. (Im Looking into acousticID, but I cant get it to work as of right now)


## 2. Create Database

Call createTracksTable.py in order to create the necessary sqlite database and table. The downloadSongs.py Script will try to create the table "tracks" if it doesnt exist yet, so this step is not really necessary.

## 3. Download Songs

Call downloadSongs.py
The script will listen to a radio Steam and save the recognised song information to the database.
The default Radio Stream is [Smartradio]: http://www.smartradio.de/, because i just love their music collection.
The MP3 Stream is at https://62.138.23.169:8000/smartradio.mp3.
I guess you can change it out for any radio Stream you like.

### Parameters

- Stream URL
- reinsert: Whether insert known tracks into the database

## 4. Enjoy

# TODO

- Add API calls for automatic creation of a Spotify playlist
- Maybe filter "Radio Edits", because they are basically the same song
- Add a new Table that tracks how often and when a given song has been played (for analytics one might want to do)
- Genre classification
- Switch API, maybe even local recognition with AcousticID Database if thats possible


# Known Issues

- Limited amount of seconds per month to analyse
- 2 Versions of a song are recognized as different songs, although they should be filtered
