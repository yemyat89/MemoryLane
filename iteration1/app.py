from random import shuffle
from flask import (Flask, request, make_response, jsonify, redirect)
from util import getData, getData2
import os

app = Flask(__name__)

songs, movies = getData()
_t = getData2()
songs.update(_t)

song_indices = {}
for v in songs.itervalues():
	for each_song in v:
		index = str(each_song[1].split()[-1][1:-1])
		label = ' '.join(each_song[1].split()[:-1])
		song_indices[index] = label

@app.route('/')
def index():
	return make_response(open('templates/index.html').read())

# Debug only
@app.route('/get_song_indices')
def get_song_indices():
	return jsonify(dict(results=song_indices))

@app.route('/songs/<year>')
def getSongsOfYear(year):
	year = int(year)
	code_to_label = {}
	data = []
	the_songs = [x for x in songs[year]]
	#shuffle(the_songs)
	for song in the_songs:
		code = song[1].split()[-1][1:-1]
		data.append(dict(title=song[0], youtube_code=code))
		code_to_label[code] = song_indices[code]
	return jsonify(dict(result=data, labels=code_to_label))

@app.route('/movies/<year>')
def getMoviesOfYear(year):
	year = int(year)
	data = []
	the_movies = [x for x in movies[year]]
	#shuffle(the_movies)
	for movie in the_movies:
		code = movie[1].split()[-1][1:-1]
		data.append(dict(title=movie[0], youtube_code=code))
	return jsonify(dict(result=data))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port) #app.run(debug=True, host='0.0.0.0')