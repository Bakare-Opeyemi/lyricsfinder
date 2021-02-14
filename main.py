from flask import Flask, request
import lyricsgenius

genius = lyricsgenius.Genius("68aj4mGvY4POHax-MNwDFd94FTUAgQPilgALO-E1X6dYmJhnICjN7XKYb6NkoMUd", verbose=False)
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello bishes!'


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    fulfillmentText = ''
    query_result = req.get('queryResult')
    parameters = query_result.get('parameters')
    artist_name = parameters.get('music-artist')
    title = parameters.get('music-title')
    if len(artist_name) > 0:
        song = genius.search_song(title, artist_name)
        if song is None:
            print("No results found for your search request")
        else:
            print("Lyrics Found!")
            lyrics = song.lyrics
    if len(artist_name) == 0:
        song = genius.search_song(title)
        lyrics = song.lyrics

    return {
        'fulfillmentText': lyrics,
        'displayText': '25',
        'source': 'webhookdata'
    }