import cPickle

class Song(object):
    def __init__(self, title, singer):
        self.title = title
        self.singer = singer
        self.keywords = '%s %s' % (title, singer)
    def toDict(self):
        return dict(title=self.title, singer=self.singer, keywords=self.keywords)


def getTopHundredsBillboard(year):

    from bs4 import BeautifulSoup
    import urllib
    import re

    def _cleanText(s):
        return re.sub(r'\t|\n', '', s)

    url = 'http://www.billboard.com/charts/year-end/%s/hot-100-songs' % year
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r)
    songs = []
    articles = soup.find_all('article')

    for article in articles:
        div_titles = article.find_all('div', class_='row-title')[0]
        title = div_titles.h2.text
        if div_titles.h3.a:
            singer = div_titles.h3.a.text
        singer = div_titles.h3.text
        title, singer = tuple(map(_cleanText, (title, singer)))
        songs.append(Song(title, singer))

    return songs

def getTopHundredsFromWiki(year):

    songs = []

    from bs4 import BeautifulSoup
    import urllib
    import re

    def _cleanText(s):
        return re.sub(r'\t|\n', '', s)

    url = 'https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_top_10_singles_in_%s' % year
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r)

    wikitable = soup.find_all('table', class_='wikitable')
    wikitable = wikitable[0]
    trs = wikitable.findAll('tr')
    tds = []
    for tr in trs:
        td = tr.findAll('td')
        if len(td) >= 5:
            tds.append(td)
    for tdx in tds:
        title_ix = 1 if len(tdx) >= 6 else 0
        singer_id = 2 if len(tdx) >= 6 else 1
        songs.append(Song(tdx[title_ix].text, tdx[singer_id].text))
    
    return songs


def getInfoFromWiki(song_names):
    from bs4 import BeautifulSoup
    import urllib
    import urllib2

    song_infos = []

    for song_name in song_names:
        song_name = song_name.replace(' ', '+')
    
        url = 'http://www.google.com/search?q=%s' % song_name
        request = urllib2.Request(url, None, 
                    {'User-Agent':
                        'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'
                    }
                )
        urlfile = urllib2.urlopen(request)
        page = urlfile.read()
        soup = BeautifulSoup(page)
        li_gs = soup.findAll('li', attrs={'class': 'g'})
        
        wikipedia = []
        for x in li_gs:
            a_s = x.findAll('a')
            if 'wikipedia' in a_s[0]['href']:
                wikipedia.append(a_s[0]['href'])
        
        if wikipedia:
            right_wiki_url = None
            if len(wikipedia) > 1:
                right_wiki_url = filter(lambda x: 'song' in x, wikipedia)[0]
            else:
                right_wiki_url = wikipedia[0]

            assert right_wiki_url
            
            r = urllib.urlopen(right_wiki_url).read()
            soup = BeautifulSoup(r)
            ps = soup.findAll('p')
            paragraph = ps[0].text

            if len(paragraph.split()) < 50:
                paragraph = '%s %s' % (paragraph, ps[1].text)
            song_infos.append(paragraph)
        else:
            print 'Cannot find the right URL for wikipedia'

    return song_infos


def getYoutubeVideos(songs):
    from apiclient.discovery import build

    DEVELOPER_KEY = "AIzaSyBUAh2FKIXzn0goX6zXWjMwD-H4g6o0vM4"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, 
                developerKey=DEVELOPER_KEY)

    results = []
    videos = []


    for song in songs:
        
        search_response = youtube.search().list(
            q=song.keywords,
            part='id,snippet',
            type='video',
            maxResults=1
          ).execute()

        items = search_response.get('items', [])
        if items:
            item = items[0]
            videos.append("%s (%s)" % (item["snippet"]["title"],
                                         item["id"]["videoId"]))

    for song, video in zip(songs, videos):
        results.append((song.title, video))

    return results

def getTopHundredMovies(year):

    from bs4 import BeautifulSoup
    import urllib
    import re

    def _addKeyword(title):
        return '%s movie trailer' % title

    url = 'http://www.imdb.com/search/title?year=%(year)s,%(year)s&title_type=feature&sort=moviemeter,asc' % dict(year=year)
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r)
    songs = []
    tblResults = soup.find_all('table', class_='results')

    rows = tblResults[0].find_all('tr', class_='detailed')
    movies = []

    for row in rows:
        title = row.find_all('td', class_='title')[0].a.get_text()
        movies.append(title)

    return map(_addKeyword, movies)

def _tempObj(x):
    class _X(object):
        pass
    y = _X()
    y.title = x
    y.keywords = x
    return y

'''
# Songs
for year in ():
    songs = getTopHundredsBillboard(year)
    results = getYoutubeVideos(songs)
    cPickle.dump(results, open('pickles/songs/_pickled_youtube_%s' % year, 'w'))
'''

'''
# Movies
for year in (2009, 2008, 2007, 2006):
    movies = getTopHundredMovies(year)
    movies = map(_tempObj, movies)
    results = getYoutubeVideos(movies)
    cPickle.dump(results, open('pickles/movies/_pickled_youtube_%s' % year, 'w'))
'''

'''
# Songs Wiki
for year in (range(1960, 1970)):
    songs = getTopHundredsFromWiki(year)
    results = getYoutubeVideos(songs)
    cPickle.dump(results, open('pickles2/songs/_pickled_youtube_%s' % year, 'w'))
'''

'''
# Wiki info test
songs = getTopHundredsBillboard(2010)[:20]
song_names = ['%s (%s song)' % (x.title, x.singer) for x in songs]
infos = getInfoFromWiki(song_names)

for info in infos:
    print info
    print '-' * 20
'''

import cPickle as pickle

year = 1987
songs = getTopHundredsFromWiki(year)
results = getYoutubeVideos(songs)
print (len(songs), len(results))
cPickle.dump(results, open('_pickled_youtube_%s' % year, 'w'))

'''
data = pickle.load(open('_pickled_youtube_%s' % year, 'r'))

with open('data_', 'w') as f:
    for d in data:
        f.write(d[1].encode('utf-8'))
        f.write('\n')

with open('t_', 'w') as f:
    for tt in songs:
        f.write(tt.title.encode('utf-8'))
        f.write('\n')
'''


'''
# Get wiki infos (youtube to wiki)
import cPickle as pickle

path = '/Users/yemyat/WebProject/MemoryLane/data'
songs = {}

for year in xrange(2006, 2015):
    data = pickle.load(open('%s/pickles/songs/_pickled_youtube_%s' % (path, year), 'r'))
    t = getTopHundredsBillboard(year)
    
    assert len(data) == len(t), (len(data), len(t))

    youtube_to_wiki = {}

    for song_info, youtube_info in zip(t, data):
        youtube_code = youtube_info[1].split()[-1][1:-1]
        wiki_keyword = '%s (%s song)' % (song_info.title.strip(), song_info.singer.strip())
        youtube_to_wiki[youtube_code] = wiki_keyword
    songs[year] = youtube_to_wiki

for year in (1987,):
    data = pickle.load(open('%s/pickles2/songs/_pickled_youtube_%s' % (path, year), 'r'))
    t = getTopHundredsFromWiki(year)

    with open('data_', 'w') as f:
        for d in data:
            f.write(d[1].encode('utf-8'))
            f.write('\n')
    with open('t_', 'w') as f:
        for tt in t:
            f.write(tt.title.encode('utf-8'))
            f.write('\n')

    print (data[28][1], t[28].title)
    print (data[29][1], t[29].title)
    print (data[30][1], t[30].title)

    assert 0, 9
    
    assert len(data) == len(t), (len(data), len(t), year)

    youtube_to_wiki = {}

    for song_info, youtube_info in zip(t, data):
        youtube_code = youtube_info[1].split()[-1][1:-1]
        wiki_keyword = '%s (%s song)' % (song_info.title.strip(), song_info.singer.strip())
        youtube_to_wiki[youtube_code] = wiki_keyword
    songs[year] = youtube_to_wiki

print songs[1990].keys()
'''