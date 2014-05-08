# -*- coding: utf-8 -*-
import sqlite3
import muse.audio


class DB:

    def __init__(self, file_path):
        self._conn = sqlite3.connect(file_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.text_factory = sqlite3.OptimizedUnicode
        self.init()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self._conn.__exit__(*exc)

    def init(self):
        self._conn.execute(
            u'''create table if not exists musics (
                id integer primary key autoincrement,
                title string not null,
                artist string,
                album string,
                category string,
                cover_mime string,
                audio_mime string not null,
                cover_data longblob,
                audio_data longblob
            )'''
        )

    def add(self, audio_path):
        with open(audio_path, 'rb') as audio_stream:
            tags = muse.audio.read(audio_path)

            # テーブルに挿入
            cur = self._conn.execute(u'''
            insert into musics values(
                :id,
                :title,
                :artist,
                :album,
                :category,
                :cover_mime,
                :audio_mime,
                :cover_data,
                :audio_data
            )''', {
                'id': None,  # idはauto incrementなのでNone
                'title': tags['title'],
                'artist': tags['artist'],
                'album': tags['album'],
                'category': tags['category'],
                'cover_mime': tags['cover_mime'],
                'audio_mime': tags['audio_mime'],
                'cover_data': buffer(tags['cover']),
                'audio_data': buffer(audio_stream.read()),
            })

            return cur.lastrowid

    def search(self):
        cur = self._conn.execute(u'select id, title, artist, album, category from musics')
        return [dict(row) for row in cur.fetchall()]

    def get_audio(self, music_id):
        row = self._conn.execute(u'select audio_mime, audio_data from musics where id = ?', music_id).fetchone()
        return {
            'mime': row['audio_mime'],
            'data': row['audio_data'],
        }

    def get_cover(self, music_id):
        row = self._conn.execute(u'select cover_mime, cover_data from musics where id = ?', music_id).fetchone()
        return {
            'mime': row['cover_mime'],
            'data': row['cover_data'],
        }