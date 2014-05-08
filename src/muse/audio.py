# -*- coding: utf-8 -*-
import os
import mutagen
import mutagen.easyid3
import mutagen.easymp4
import mutagen.mp3
import mutagen.mp4


def _first_or_none(dic, key):
    """辞書オブジェクトに指定キーが存在すれば
    そのキーに対応するリストの最初の要素を返し，存在しなければ
    Noneを返す"""
    if key in dic and len(dic[key]) > 0:
        return dic[key][0]
    else:
        return None


def _get_basename_without_ext(path):
    return os.path.splitext(os.path.basename(path))[0]


class AudioFile:

    @staticmethod
    def create(path):
        audio = mutagen.File(path)
        if isinstance(audio, mutagen.mp3.MP3):
            return MP3Audio(path, mutagen.easyid3.EasyID3)
        elif isinstance(audio, mutagen.mp4.MP4):
            return MP4Audio(path, mutagen.easymp4.EasyMP4)
        else:
            raise Exception(u'AudioFileクラスが対応しているのはmp3, mp4(m4a)のみです')

    def __init__(self, path, easy_tag_class):
        self._path = path
        self._audio = mutagen.File(path)
        self._easy_tags = easy_tag_class(path)

    @property
    def title(self):
        title = _first_or_none(self._easy_tags, 'title')
        if title is None:
            title = _get_basename_without_ext(self._path)
        return title

    @property
    def artist(self):
        return _first_or_none(self._easy_tags, 'artist')

    @property
    def album(self):
        return _first_or_none(self._easy_tags, 'album')

    @property
    def cover_data(self):
        raise NotImplementedError()

    @property
    def cover_mime(self):
        raise NotImplementedError()

    @property
    def audio_mime(self):
        return self._audio.mime[0]


class MP3Audio(AudioFile):

    @property
    def cover_data(self):
        tags = self._audio.tags
        if u'APIC:' in tags:
            return tags[u'APIC:'].data
        else:
            return None

    @property
    def cover_mime(self):
        tags = self._audio.tags
        if u'APIC:' in tags:
            return tags[u'APIC:'].mime
        else:
            return None


class MP4Audio(AudioFile):

    @staticmethod
    def _get_mime_from_mp4_imageformat(imageformat):
        """mp4のメタデータのカバー画像形式番号をmimeタイプに変換する"""
        if imageformat == mutagen.mp4.MP4Cover.FORMAT_JPEG:
            return 'image/jpeg'
        elif imageformat == mutagen.mp4.MP4Cover.FORMAT_PNG:
            return 'image/png'
        else:
            raise Exception(u'mp4のカバー画像からJPEG/PNG以外のフォーマットが検出されました．明らかにおかしいです')

    @property
    def cover_data(self):
        tags = self._audio.tags
        if u'covr' in tags and len(tags[u'covr']) > 0:
            return tags[u'covr'][0]
        else:
            return None

    @property
    def cover_mime(self):
        tags = self._audio.tags
        if u'covr' in tags and len(tags[u'covr']) > 0:
            return MP4Audio._get_mime_from_mp4_imageformat(tags[u'covr'][0].imageformat)
        else:
            return None


def read(audio_file):
    """音声ファイル(mp3 or m4a)から情報を取る

    引数
    audio_file : 音声ファイルのパス

    返り値
    {
      title : 音楽のタイトル
      artist : アーティスト
      album : アルバム名
      category : カテゴリー（タイアップアニメ名）
      cover : カバー画像のバイナリ
      cover_mime : カバー画像のmime type
      audio_mime : 音声ファイルのmime type
    }"""
    audio = AudioFile.create(audio_file)

    return {
        'title': audio.title,
        'artist': audio.artist,
        'album': audio.album,
        'category': None,  # TODO: カテゴリは後に歌詞タイムからスクレイピングする予定
        'cover': audio.cover_data,
        'cover_mime': audio.cover_mime,
        'audio_mime': audio.audio_mime,
    }


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('Usage: audio.py <audio_file>')
        exit()

    info = read(sys.argv[1])
    print(u'title: {0}'.format(info['title']))
    print(u'artist: {0}'.format(info['artist']))
    print(u'album: {0}'.format(info['album']))
    print(u'mime: {0}'.format(info['audio_mime']))
    if info['cover'] is not None:
        print(u'cover_mime: {0}'.format(info['cover_mime']))
        img_exts = {
            'image/jpeg': '.jpg',
            'image/png': '.png',
        }
        with open(u'{0}{1}'.format(info['title'], img_exts[info['cover_mime']]), 'wb') as f:
            f.write(info['cover'])
