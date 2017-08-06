import os
import bottle
from typing import List
import muse.audio
import muse.db
import muse.dict
import muse.config


# DBのBLOBに埋め込んだバイナリをファイルキャッシュとして保存してからHTTP responseにする（ファイルにしたほうがストリーミングなどがしやすいから）
def static_cache_file(filename, mime_type, file_content_func: callable):
    if not os.path.exists(filename):
        with open(filename, 'wb') as f:
            f.write(file_content_func())
    return bottle.static_file(filename, root='.', mimetype=mime_type)


def artwork_static_cache_file(artwork: muse.db.Artwork):
    filename = '{}/muse_artwork_cache_{}'.format(muse.config.TEMP_FILE_DIR, artwork.music_id)
    return static_cache_file(filename, artwork.mime_type, lambda: artwork.data)


def audio_data_static_cache_file(audio_data: muse.db.AudioData):
    filename = '{}/muse_audio_data_cache_{}'.format(muse.config.TEMP_FILE_DIR, audio_data.music_id)
    return static_cache_file(filename, audio_data.mime_type, lambda: audio_data.data)


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
    musics = muse.db.get_musics()
    return muse.dict.musics_to_dict(musics)


@app.post('/musics')
def upload_musics():
    upload_files = filter(is_valid_upload_file, bottle.request.files.getlist('files'))  # type: List[bottle.FileUpload]
    # todo: error handling

    saved_music_models = []
    for upload_file in upload_files:
        music = muse.audio.Music(upload_file.file)
        saved_music_models.append(muse.db.add_music(music))

    return muse.dict.musics_to_dict(saved_music_models)


@app.delete('/musics/<music_id>')
def delete_music(music_id):
    deleted_music = muse.db.delete_music(music_id)
    return muse.dict.music_to_dict(deleted_music)


@app.get('/artworks/<music_id>')
def get_music_artwork(music_id):
    artwork = muse.db.get_artwork(music_id)
    return artwork_static_cache_file(artwork)


@app.get('/audio-data/<music_id>')
def get_music_stream(music_id):
    audio_data = muse.db.get_audio_data(music_id)
    return audio_data_static_cache_file(audio_data)


def is_valid_upload_file(upload_file):
    """
    :type upload_file: bottle.FileUpload
    :rtype: bool
    """
    return True  # todo: ちゃんとする


app.run(host="localhost", port=8080, debug=True)
