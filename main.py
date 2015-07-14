import cPickle as pickle
from flask import (Flask, request, make_response, jsonify, redirect)

app = Flask(__name__)

youtubes = pickle.load(open('/Users/yemyat/WebProject/Youtube/_pickled_youtube', 'r'))
facebook = pickle.load(open('/Users/yemyat/Desktop/x/_merged', 'r'))
movies = pickle.load(open('/Users/yemyat/WebProject/Youtube/_pickled_youtube_vid', 'r'))

customs = {}

@app.route('/')
def index():
	return make_response(open('templates/index.html').read())

@app.route('/songs')
def show_songs():
    songs = dict(data=[])
    for item in youtubes[:2]:
        v = item[1]
        splits = v.split()
        title, youtube_code = ' '.join(splits[:-1]), splits[-1][1:-1]
        songs['data'].append(dict(title=title, code=youtube_code))
    return jsonify(songs)

@app.route('/facebook')
def show_fb():
    songs = dict(data=[])
    for item in facebook:
        songs['data'].append(dict(idd=item[0], msg=item[1], time=item[2].split('T')[0]))
    return jsonify(songs)

@app.route('/new-playlist', methods=['POST'])
def new_playlist():
    global customs
    name =  request.get_json().get('list_name')
    new_id = len(customs)

    customs[str(new_id)] = {
        'id': new_id,
        'name': name,
        'clips': []
    }
    
    return jsonify(dict(id=new_id, name=name))

@app.route('/load-playlist')
def load_playlist():
    songs = dict(youtube=[])
    for item in youtubes[:2]:
        v = item[1]
        splits = v.split()
        title, youtube_code = ' '.join(splits[:-1]), splits[-1][1:-1]
        songs['youtube'].append(youtube_code)

    for k, v in customs.iteritems():
        songs[k] = map(lambda x: x.split('=')[-1], v['clips'])

    return jsonify(songs)

@app.route('/new-clip', methods=['POST'])
def new_clip():
    global customs
    name =  request.get_json().get('clip_name')
    idd =  request.get_json().get('id')
    customs[str(idd)]['clips'].append(name)
    vcode = name.split('=')[-1]
    return jsonify(dict(vid=vcode))

@app.route('/get-all-clips/<idd>', methods=['GET'])
def get_all_clips(idd):
    global customs
    data = {'data': []}
    for clp in customs[idd]['clips']:
        code = clp.split('=')[-1]
        title = 'TITLE'
        ysrc = clp
        data['data'].append(dict(title=title,
                                code=code,
                                ysrc=ysrc))
    return jsonify(data)

@app.route('/custom-playlist', methods=['GET'])
def custom_playlist():
    data = {}
    data['data'] = []
    for k, v in customs.iteritems():
        data['data'].append(dict(id=k, name=v['name'], clips=v['clips']))
    return jsonify(data)

@app.route('/one-playlist/<plid>', methods=['GET'])
def one_custom_playlist(plid):
    item = customs.get(plid, None)
    data = {'data': item}
    return jsonify(data)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')