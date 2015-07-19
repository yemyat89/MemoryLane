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

def getData2():
	path = 'data/pickles2'

	songs = {}

	for year in xrange(1960, 2006):
		data = pickle.load(open('%s/songs/_pickled_youtube_%s' % (path, year), 'r'))
		songs[year] = data

	return songs

