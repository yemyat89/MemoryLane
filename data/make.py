import cPickle

DEVELOPER_KEY = None

with open('cred.mine', 'r') as f:
    for l in f:
        DEVELOPER_KEY = l.strip()
        break

assert DEVELOPER_KEY

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

    ths = trs[0].findAll('th')
    threshold = len(ths)
    tds = []
    for tr in trs:
        td = tr.findAll('td')
        if len(td) >= 5:
            tds.append(td)
    for tdx in tds:
        title_ix = 1 if len(tdx) >= threshold else 0
        singer_ix = 2 if len(tdx) >= threshold else 1

        sortkeys = tdx[title_ix].findAll('span', class_='sortkey')
        if sortkeys:
            title = sortkeys[0].text
        else:
            title = tdx[title_ix].text
        

        sortkeys = tdx[singer_ix].findAll('span', class_='sortkey')
        if sortkeys:
            singer = sortkeys[0].text
        else:
            singer = tdx[singer_ix].text
        
        songs.append(Song(title, singer))
    
    return songs


def getTopHundredsFromWiki2(year):

    songs = []

    from bs4 import BeautifulSoup
    import urllib
    import re

    def _cleanText(s):
        return re.sub(r'\t|\n', '', s)

    url = 'https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_%s' % year
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r)

    wikitable = soup.find_all('table', class_='wikitable')[0]
    trs = wikitable.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        if tds:
            ths = tr.find_all('th')

            title_ix = 0 if ths else 1
            singer_ix = 1 if ths else 2

            title = tds[title_ix].text.replace('"', '')
            singer = tds[singer_ix].text

            songs.append(Song(title, singer))
    
    return songs



def _disabled_getInfoFromWiki(song_names):

    print 'processing %s' % song_names

    if not isinstance(song_names, list):
        song_names = [song_names]

    from bs4 import BeautifulSoup
    import urllib
    import urllib2

    song_infos = []

    for song_name in song_names:

        qstring = urllib.urlencode(dict(q=song_name))
        
        url = 'http://www.google.com/search?%s' % qstring
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
                print 'PROBLEM: %s----%s' % (song_name, str(wikipedia))
                x = filter(lambda x: 'song' in x, wikipedia)
                if x:
                    right_wiki_url = x[0]
            else:
                right_wiki_url = wikipedia[0]

            if not right_wiki_url:
                right_wiki_url = wikipedia[0]
            
            r = urllib.urlopen(right_wiki_url).read()
            soup = BeautifulSoup(r)
            ps = soup.findAll('p')
            paragraph = ps[0].text

            if len(paragraph.split()) < 50:
                paragraph = '%s %s' % (paragraph, ps[1].text)
            song_infos.append(paragraph)
        else:
            print 'Cannot find the right URL for wikipedia (song name: %s)' % song_name

    return song_infos


def getInfoFromWiki_NoGoogle(song_names):

    if not isinstance(song_names, list):
        song_names = [song_names]

    from bs4 import BeautifulSoup
    import urllib
    import urllib2

    song_infos = []
    c = 0
    for song_name, singer_name in song_names:
        try:
            song_name = urllib.urlencode(dict(q=song_name)).split('=')[1]
            song_name = song_name.replace('+', '_')
            song_name = song_name.replace('%24', 's')

            singer_name = urllib.urlencode(dict(q=singer_name)).split('=')[1]
            singer_name = singer_name.replace('+', '_')
            singer_name = singer_name.replace('%24', 's')

            song_name = song_name
            song_name = song_name.replace('__', '_')

            song_song_name = '%s_(song)' % song_name
            song_song_name = song_song_name.replace('__', '_')

            song_singer_name = '%s_(%s_song)' % (song_name, singer_name)
            song_singer_name = song_singer_name.replace('__', '_')
            
            wurl0 = None
            wurl1 = None
            wurl2 = None

            wurl0 = 'https://en.wikipedia.org/wiki/%s' % song_song_name
            r = urllib.urlopen(wurl0).read()
            soup = BeautifulSoup(r)
            
            ps = soup.findAll('p')
            paragraph = ps[0].text

            if 'Other reasons this message may' in paragraph or 'may refer to' in paragraph:

                wurl1 = 'https://en.wikipedia.org/wiki/%s' % song_singer_name
                r = urllib.urlopen(wurl1).read()
                soup = BeautifulSoup(r)
                
                ps = soup.findAll('p')
                paragraph = ps[0].text

            if 'Other reasons this message may' in paragraph or 'may refer to' in paragraph:

                wurl2 = 'https://en.wikipedia.org/wiki/%s' % song_name
                r = urllib.urlopen(wurl2).read()
                soup = BeautifulSoup(r)
                
                ps = soup.findAll('p')
                paragraph = ps[0].text


            if 'Other reasons this message may' in paragraph or 'may refer to' in paragraph:
                print ('Cannot find:', wurl0, wurl1, wurl2)
                c += 1
                song_infos.append(None)
            else:
                song_infos.append(paragraph)
        except Exception as e:
            print (e, song_name, singer_name)
            c += 1
            song_infos.append(None)

    return c, song_infos


def getYoutubeVideos(songs):
    from apiclient.discovery import build
    
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
        else:
            print 'WARNING: No Item for (TITLE:%s, SINGER:%s)' % (song.title, song.singer)

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



# Songs Wiki
for year in xrange(2000, 2006):
    songs = getTopHundredsFromWiki2(year)
    results = getYoutubeVideos(songs[:2])
    print results
    break
    #cPickle.dump(results, open('pickles4/songs/_pickled_youtube_%s' % year, 'w'))




'''
# Wiki info test ( Error prone/ SKipped)
import cPickle as pickle

for year in xrange(1995, 2006):
    #songs = getTopHundredsFromWiki2(year)
    #pickle.dump(songs, open('ywiki_manual/_pck_%s' % year, 'w'))
    #continue

    data = pickle.load(open('ywiki_manual/_pck_%s' % year, 'r'))

    snames = []
    articles = ['a', 'an', 'of', 'the', 'to', 'is', 'on', 'in', 'at']
    for b in data:

        x = b.title.lower()
        x = x.replace('"', '').strip()
        d = []
        for t in x.split():
            if t in articles:
                d.append(t)
            elif t.lower()=='dj':
                d.append('DJ')
            else:
                d.append(t[0].upper()+t[1:])
        x = ' '.join(d)
        if x == 'Omg':
            x = x.upper()

        xx = b.singer.lower().strip()
        d = []
        for t in xx.split():
            d.append(t[0].upper()+t[1:])
        xx = ' '.join(d)
        
        xx3 = xx.split('Featuring')
        if len(xx3) == 1:
            xx3 = xx.split('featuring')
        if len(xx3) > 1:
            xx = xx3[0].strip()

        #x = x.replace(' ', '_')
        #xx = xx.replace(' ', '_')
        snames.append((x, xx))

    ec, y = getInfoFromWiki_NoGoogle(snames)

    pck_data = dict(original=data, wiki=y, year=year, ec=ec, total=len(snames))
    pickle.dump(pck_data, open('ywiki_manual_out/_pck_data_%s' % year, 'w'))

    print '*' * 10
    print (year, ec, len(snames))
    print '*' * 10
'''



'''
pck = pickle.load(open('ywiki_manual_out/_pck_data_%s' % 2012, 'r'))
for w in pck['wiki'][:10]:
    print w
    print '-' * 30
'''


'''
# Debug Wiki data scraping
import cPickle as pickle

for year in (2001, 1999, 1997):
    songs = getTopHundredsFromWiki(year)

    with open('temp/t_%s' % year, 'w') as f:
        for tt in songs:
            f.write(tt.title.encode('utf-8'))
            f.write('---------')
            f.write(tt.singer.encode('utf-8'))
            f.write('\n')

#results = getYoutubeVideos(songs)
#print (len(songs), len(results))

#cPickle.dump(results, open('_pickled_youtube_%s' % year, 'w'))
'''

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
#songs = {}

for year in xrange(2011, 2015):
    songs = {}
    print 'year %s' % year
    data = pickle.load(open('%s/pickles/songs/_pickled_youtube_%s' % (path, year), 'r'))
    t = getTopHundredsBillboard(year)
    
    assert len(data) == len(t), (len(data), len(t))

    youtube_to_wiki = {}

    for song_info, youtube_info in zip(t, data):
        youtube_code = youtube_info[1].split()[-1][1:-1]
        wiki_keyword = '%s (%s song)' % (song_info.title.strip(), song_info.singer.strip())

        wiki_info = _disabled_getInfoFromWiki(wiki_keyword)

        if wiki_info:
            wiki_info = wiki_info[0]
            youtube_to_wiki[youtube_code] = wiki_info
    songs[year] = youtube_to_wiki

    pickle.dump(songs, open('youtube_to_wiki/_pickled_ywiki_%s' % year, 'w'))

    print '-' * 20

for year in []: #xrange(1960, 2006):
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
    
    assert len(data) == len(t), (len(data), len(t), year)

    youtube_to_wiki = {}

    for song_info, youtube_info in zip(t, data):
        youtube_code = youtube_info[1].split()[-1][1:-1]
        wiki_keyword = '%s (%s song)' % (song_info.title.strip(), song_info.singer.strip())
        youtube_to_wiki[youtube_code] = wiki_keyword
    songs[year] = youtube_to_wiki
'''


#pickle.dump(songs, open('_pickled_ywiki_2006_2007', 'w'))

#print songs[2006]['pZG7IK99OvI']

#for youtube_code, you_wikikeywords_dict in songs.iteritems():


