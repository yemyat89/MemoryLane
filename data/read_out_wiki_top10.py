import cPickle as pickle

# Read youtube results
for year in xrange(1960, 1993):
	pck = pickle.load(open('pickles4/songs/_pickled_youtube_%s' % year, 'r'))
	with open('temp/_pyyear_%s' % year, 'w') as f:
		for item in pck:
			f.write('TITLE: %s, YOUTUBE: %s' % (item[0].encode('utf-8'), item[1].encode('utf8')))
			f.write('\n')



'''
# Read wiki results
from make import getTopHundredsFromWiki2
for year in xrange(1960, 2006):
	data = getTopHundredsFromWiki2(year)
	with open('temp/_wiki_year_%s' % year, 'w') as f:
		for item in data:
			f.write('TITLE: %s, SINGER: %s, KEYWORDS: %s' % (item.title.encode('utf8'),
															item.singer.encode('utf8'),
															item.keywords.encode('utf8')))
			f.write('\n')
'''

