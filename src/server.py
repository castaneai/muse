# -*- coding: utf8 -*-
import bottle
import os
import json
import muse.db

DB_PATH = '../data/muse.db'
app = bottle.Bottle()


@app.get('/')
def top():
    return bottle.static_file('index.html', root='../public')


@app.post('/upload')
def upload_music():
    upload = bottle.request.files.get('file')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.mp3', '.m4a'):
        return 'File ext not allowed.'

    temp_path = u'../.tmp/{0}'.format(upload.filename)
    try:
        upload.save(temp_path)
        with muse.db.DB(DB_PATH) as db:
            db.add(temp_path)
        return 'OK'
    finally:
        os.unlink(temp_path)


@app.get('/musics')
def get_musics():
    result = []
    with muse.db.DB(DB_PATH) as db:
        for music in db.search():
            music['audio_url'] = 'musics/{0}'.format(music['id'])
            music['cover_url'] = 'covers/{0}'.format(music['id'])
            result.append(music)
        bottle.response.content_type = 'application/json'
        return json.dumps(result)


@app.get('/musics/<music_id>')
def get_music(music_id):
    with muse.db.DB(DB_PATH) as db:
        audio = db.get_audio(music_id)

    path = '../.tmp/musics/{0}'.format(music_id)
    if not os.path.exists(path):
        with open(path, 'wb') as f:
            f.write(audio['data'])
    return open(path, 'rb')


@app.get('/covers/<music_id>')
def get_covers(music_id):
    with muse.db.DB(DB_PATH) as db:
        cover = db.get_cover(music_id)

    path = '../.tmp/covers/{0}'.format(music_id)
    if not os.path.exists(path):
        with open(path, 'wb') as f:
            f.write(cover['data'])
    return bottle.static_file('{0}'.format(music_id), root='../.tmp/covers', mimetype=cover['mime'])


@app.get('/<filepath:path>')
def static(filepath):
    return bottle.static_file(filepath, root='../public')


@app.get('/test')
def test():
    return bottle.static_file('1', root='../public', mimetype='audio/mp3')

bottle.run(app, host='localhost', port='6000')