import sqlite3
import json
import bottle
import bottle_sqlite
from typing import List
import muse.audio

app = bottle.Bottle()
app.install(bottle_sqlite.Plugin(dbfile="test.db"))


@app.get("/debug/init")
def init(db):
    db.executescript(open("init.sql").read())
    return "init OK."


@app.get("/debug/test-upload")
def test_upload():
    return bottle.static_file('public/test_upload.html', root='.')


@app.get("/musics")
def get_musics(db):
    # todo: json responseはdecoratorにしたい
    bottle.response.content_type = 'application/json'
    rows = [dict(row) for row in db.execute("select id, title from musics").fetchall()]
    return json.dumps(rows)


@app.post('/musics')
def upload_musics(db):
    upload_files = filter(is_valid_upload_file, bottle.request.files.getlist('files'))  # type: List[bottle.FileUpload]
    for upload_file in upload_files:
        music = muse.audio.Music(upload_file.file)
        insert_music(db, music)
    return 'OK'


def is_valid_upload_file(upload_file):
    """
    :type upload_file: bottle.FileUpload
    :rtype: bool
    """
    return True  # todo: ちゃんとする


def insert_music(db, music):
    """
    :type db: sqlite3.Connection
    :type music: muse.audio.Music 
    """
    sql = "insert into musics(title, artist, album) values(?, ?, ?)"
    cur = db.execute(sql, (music.tags.title, music.tags.artist, music.tags.album))
    inserted_id = cur.lastrowid

    if inserted_id > 0 and music.artwork is not None:
        sql = "insert into artworks(music_id, mime_type, data) values(?, ?, ?)"
        db.execute(sql, (inserted_id, music.artwork.mime_type, music.artwork.data_bytes))

app.run(host="localhost", port=8080, debug=True)
