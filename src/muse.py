# -*- coding: utf8 -*-
import mutagenwrapper
import sqlite3
import shutil


def read_tag_or_none(tags, key):
    """音楽のタグ情報から指定したキーの情報を読み取り、リスト形式の場合は先頭1つのみ、
    情報がない場合はNoneを返す"""
    if key in tags and len(tags[key]) > 0:
        return tags[key][0]
    else:
        return None


def read_tags(music_url):
    """音楽ファイルのタグ情報を最低限分だけ読み込む"""
    tags = mutagenwrapper.read_tags(music_url)
    return {key: read_tag_or_none(tags, key) for key in ('title', 'artist', 'pictures')}


class MuseDB:

    DATA_DIR = '../data'
    MUSIC_DIR = DATA_DIR + '/musics'
    PICTURE_DIR = DATA_DIR + '/pictures'

    def __init__(self, db_url):
        self._conn = sqlite3.connect(db_url)
        self._conn.row_factory = sqlite3.Row

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self._conn.__exit__(*exc)

    def init(self):
        self._conn.execute(
            u'create table musics (id integer primary key autoincrement, title string not null, artist string not null)'
        )

    def search(self):
        rows = self._conn.execute(u'select * from musics').fetchall()
        return [dict(row) for row in rows]

    def add(self, music_url):
        tags = read_tags(music_url)
        cur = self._conn.execute(u'insert into musics values(?, ?, ?)', (None, tags['title'], tags['artist']))
        music_id = cur.lastrowid

        self._copy_music(music_url, music_id)
        if tags['pictures'] is not None:
            self._copy_picture(music_id, tags['pictures'])

    def _copy_music(self, src_url, music_id):
        shutil.copyfile(src_url, '{0}/{1}'.format(self.MUSIC_DIR, music_id))

    def _copy_picture(self, music_id, picture_bytes):
        with open('{0}/{1}'.format(self.PICTURE_DIR, music_id), 'wb') as stream:
            stream.write(picture_bytes)

if __name__ == '__main__':
    with MuseDB('../data/musics.sqlite') as db:
        db.add('../database.m4a')
