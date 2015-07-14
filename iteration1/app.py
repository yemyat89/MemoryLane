import cPickle as pickle
from flask import (Flask, request, make_response, jsonify, redirect)

app = Flask(__name__)

youtubes = pickle.load(open('/Users/yemyat/WebProject/Youtube/_pickled_youtube', 'r'))
movies = pickle.load(open('/Users/yemyat/WebProject/Youtube/_pickled_youtube_vid', 'r'))

customs = {}

@app.route('/')
def index():
	return make_response(open('templates/index.html').read())

@app.route('/songs/<year>')
def getSongsOfYear(year):
	data = []
	for song in youtubes:
		code = song[1].split()[-1][1:-1]
		data.append(dict(title=song[0], youtube_code=code))
	return jsonify(dict(result=data))

@app.route('/movies/<year>')
def getMoviesOfYear(year):
	data = []
	for movie in movies:
		code = movie[1].split()[-1][1:-1]
		data.append(dict(title=movie[0], youtube_code=code))
	return jsonify(dict(result=data))

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')