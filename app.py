import io
import json
import bottle
import fdsend
from typing import List
import muse.audio
import muse.db

app = bottle.Bottle()


# 開発時のcors対策: デバッグ時のみ
@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    bottle.response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    bottle.response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@app.get("/debug/test-upload")
def test_upload():
    return bottle.static_file('public/test_upload.html', root='.')


@app.get("/musics")
def get_musics():
    # todo: json responseはdecoratorにしたい
    bottle.response.content_type = 'application/json'
    musics = muse.db.get_musics()
    return json.dumps(muse.db.models_to_dicts(musics))


@app.post('/musics')
def upload_musics():
    upload_files = filter(is_valid_upload_file, bottle.request.files.getlist('files'))  # type: List[bottle.FileUpload]
    # todo: error handling

    saved_music_models = []
    for upload_file in upload_files:
        music = muse.audio.Music(upload_file.file)
        saved_music_models.append(muse.db.add_music(music))

    return json.dumps(muse.db.models_to_dicts(saved_music_models))


@app.delete('/musics/<music_id>')
def delete_music(music_id):
    deleted_music = muse.db.delete_music(music_id)
    return json.dumps(muse.db.model_to_dict(deleted_music))


@app.get('/artworks/<music_id>')
def get_music_artwork(music_id):
    artwork = muse.db.get_artwork(music_id)
    # todo: error handling
    buffer = io.BytesIO(artwork.data)
    return fdsend.send_file(buffer, ctype=artwork.mime_type)


@app.get('/audio-data/<music_id>')
def get_music_stream(music_id):
    audio_data = muse.db.get_audio_data(music_id)
    buffer = io.BytesIO(audio_data.data)
    return fdsend.send_file(buffer, ctype=audio_data.mime_type)


def is_valid_upload_file(upload_file):
    """
    :type upload_file: bottle.FileUpload
    :rtype: bool
    """
    return True  # todo: ちゃんとする


app.run(host="localhost", port=8080, debug=True)
