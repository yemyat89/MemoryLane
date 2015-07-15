import cPickle as pickle

def getData():
	path = 'data/pickles'

	songs = {}
	movies = {}

	for year in xrange(2006, 2015):
		data = pickle.load(open('%s/songs/_pickled_youtube_%s' % (path, year), 'r'))
		songs[year] = data

		data = pickle.load(open('%s/movies/_pickled_youtube_%s' % (path, year), 'r'))
		movies[year] = data

	return songs, movies
