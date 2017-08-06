from playhouse.shortcuts import model_to_dict
import muse.db


_API_HOST = 'http://localhost:8080'


def music_to_dict(music: muse.db.Music) -> dict:
    dic = model_to_dict(music)
    dic['artworkUrl'] = '{}/artworks/{}'.format(_API_HOST, music.id)
    dic['audioDataUrl'] = '{}/audio-data/{}'.format(_API_HOST, music.id)
    return dic


def musics_to_dict(musics) -> dict:
    return {
        'musics': [music_to_dict(m) for m in musics]
    }
