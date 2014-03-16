# -*- coding: utf8 -*-
import bottle
import os
import json
import muse

DB_PATH = '../data/musics.sqlite'
app = bottle.Bottle()


@app.post('/upload')
def upload_musics():
    upload = bottle.request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.mp3', '.m4a'):
        return 'File ext not allowed.'

    save_path = u'../.tmp/{0}'.format(upload.filename)
    upload.save(save_path)
    with muse.MuseDB(DB_PATH) as db:
        db.add(save_path)
    return 'OK'


@app.get('/musics')
def get_musics():
    bottle.response.content_type = 'application/json'
    with muse.MuseDB(DB_PATH) as db:
        return json.dumps(db.search())


@app.get('/pictures/<music_id>')
def get_images(music_id):
    url = '{0}.jpg'.format(music_id)
    return bottle.static_file(url, root='../data/pictures')



@app.get('/<filepath:path>')
def static(filepath):
    return bottle.static_file(filepath, root='../public')

bottle.run(app, host='localhost', port='8080')