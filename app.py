import tempfile
import json
import bottle
from typing import List
import muse.audio
import muse.db

app = bottle.Bottle()


@app.get("/debug/test-upload")
def test_upload():
    return bottle.static_file('public/test_upload.html', root='.')


@app.get("/musics")
def get_musics():
    # todo: json responseはdecoratorにしたい
    bottle.response.content_type = 'application/json'
    music_models = muse.db.get_musics()
    return json.dumps(music_models)


@app.post('/musics')
def upload_musics():
    upload_files = filter(is_valid_upload_file, bottle.request.files.getlist('files'))  # type: List[bottle.FileUpload]
    for upload_file in upload_files:
        music = muse.audio.Music(upload_file.file)
        muse.db.add_music(music)
    return 'OK'


def is_valid_upload_file(upload_file):
    """
    :type upload_file: bottle.FileUpload
    :rtype: bool
    """
    return True  # todo: ちゃんとする


app.run(host="localhost", port=8080, debug=True)
