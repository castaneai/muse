# -*- coding: utf-8 -*-
import os
import muse.audio
import peewee

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
    return Music.select()


def get_artwork(music_id) -> Artwork:
    return Artwork.get(Artwork.music_id == music_id)


def get_audio_data(music_id) -> AudioData:
    return AudioData.get(AudioData.music_id == music_id)


@_db.atomic()
def add_music(music: muse.audio.Music):
    music_model = Music(title=music.tags.title, artist=music.tags.artist, album=music.tags.album)
    music_model.save()
    music_id = music_model.get_id()
    audio_data_model = AudioData(music_id=music_id, mime_type=music.mime_type, data=music.data_bytes)
    audio_data_model.save()
    if music.artwork is not None:
        add_artwork(music_id, music.artwork)

    return music_model


@_db.atomic()
def delete_music(music_id):
    music = Music.get(Music.id == music_id)
    music.delete_instance()

    try:
        artwork = Artwork.get(music_id == music_id)
        artwork.delete_instance()
    except Artwork.DoesNotExist:
        pass

    try:
        audio_data = AudioData.get(music_id == music_id)
        audio_data.delete_instance()
    except AudioData.DoesNotExist:
        pass

    return music


def add_artwork(music_id: int, artwork: muse.audio.Artwork):
    artwork_model = Artwork(music_id=music_id, mime_type=artwork.mime_type, data=artwork.data_bytes)
    artwork_model.save()


if __name__ == "__main__":
    _db.connect()
    _db.create_tables([Music, Artwork, AudioData], True)
    print("db init succeeded.")
    print("tables: " + str(_db.get_tables()))
