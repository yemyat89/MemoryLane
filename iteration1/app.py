from random import shuffle
from flask import (Flask, request, make_response, jsonify, redirect)
from util import getData

app = Flask(__name__)

songs, movies = getData()

@app.route('/')
def index():
	return make_response(open('templates/index.html').read())

@app.route('/songs/<year>')
def getSongsOfYear(year):
	year = int(year)
	data = []
	the_songs = [x for x in songs[year]]
	shuffle(the_songs)
	for song in the_songs:
		code = song[1].split()[-1][1:-1]
		data.append(dict(title=song[0], youtube_code=code))
	return jsonify(dict(result=data))

@app.route('/movies/<year>')
def getMoviesOfYear(year):
	year = int(year)
	data = []
	the_movies = [x for x in movies[year]]
	shuffle(the_movies)
	for movie in the_movies:
		code = movie[1].split()[-1][1:-1]
		data.append(dict(title=movie[0], youtube_code=code))
	return jsonify(dict(result=data))

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')