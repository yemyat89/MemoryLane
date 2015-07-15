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

# Movies
for year in (2009, 2008, 2007, 2006):
    movies = getTopHundredMovies(year)
    movies = map(_tempObj, movies)
    results = getYoutubeVideos(movies)
    cPickle.dump(results, open('pickles/movies/_pickled_youtube_%s' % year, 'w'))





