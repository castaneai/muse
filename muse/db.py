# -*- coding: utf-8 -*-
import os
import muse.audio
import peewee
import playhouse.shortcuts

DB_DIR = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../data/muse.db"))
_db = peewee.SqliteDatabase(DB_DIR)


class BaseModel(peewee.Model):
    class Meta:
        database = _db


class Music(BaseModel):
    title = peewee.CharField(unique=True)
    artist = peewee.CharField()
    album = peewee.CharField()


class Artwork(BaseModel):
    music_id = peewee.ForeignKeyField(Music, related_name='artwork')
    mime_type = peewee.CharField()
    data = peewee.BlobField()


class AudioData(BaseModel):
    music_id = peewee.ForeignKeyField(Music, related_name='audio_data')
    mime_type = peewee.CharField()
    data = peewee.BlobField()


def get_musics():
    return [playhouse.shortcuts.model_to_dict(model) for model in Music.select()]


@_db.atomic()
def add_music(music: muse.audio.Music):
    music_model = Music(title=music.tags.title, artist=music.tags.artist, album=music.tags.album)
    music_model.save()
    music_id = music_model.get_id()
    audio_data_model = AudioData(music_id=music_id, mime_type=music.mime_type, data=music.data_bytes)
    audio_data_model.save()
    if music.artwork is not None:
        add_artwork(music_id, music.artwork)


def add_artwork(music_id: int, artwork: muse.audio.Artwork):
    artwork_model = Artwork(music_id=music_id, mime_type=artwork.mime_type, data=artwork.data_bytes)
    artwork_model.save()


if __name__ == "__main__":
    _db.connect()
    _db.create_tables([Music, Artwork, AudioData], True)
    print("db init succeeded.")
    print("tables: " + str(_db.get_tables()))
