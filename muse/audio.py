# -*- coding: utf-8 -*-
import mutagen
import mutagen.mp3
import mutagen.mp4
import mutagen.id3
import mutagen.easyid3
import mutagen.easymp4

_SUPPORTED_MUTAGEN_FILE_TYPES = (
    mutagen.mp3.EasyMP3,
    mutagen.easymp4.EasyMP4,
)


def _id3tags_to_artwork(id3tags, _):
    tag = id3tags.get("APIC:", None)
    if not isinstance(tag, mutagen.id3.APIC):
        return None
    return Artwork(tag.mime, tag.data)


def _mp4tags_to_artwork(mp4tags, _):
    tag = mp4tags.get("covr", None)
    if not isinstance(tag, list) or len(tag) < 1:
        return None
    if not isinstance(tag[0], mutagen.mp4.MP4Cover):
        return None
    return Artwork(_mp4_cover_to_mime_type(tag[0]), tag)


def _mp4_cover_to_mime_type(mp4_cover):
    return {
        mutagen.mp4.MP4Cover.FORMAT_JPEG: "image/jpeg",
        mutagen.mp4.MP4Cover.FORMAT_PNG: "image/png",
    }.get(mp4_cover.imageformat, None)


def _get_mime_type(mutagen_file: mutagen.FileType):
    if len(mutagen_file.mime) > 0:
        return mutagen_file.mime[0]
    raise Exception("mime/type not found: " + mutagen_file.filename)


mutagen.easyid3.EasyID3.RegisterKey("artwork", _id3tags_to_artwork)
mutagen.easymp4.EasyMP4.RegisterKey("artwork", _mp4tags_to_artwork)


class Artwork:

    def __init__(self, mime_type, data_bytes):
        self.mime_type = mime_type
        self.data_bytes = data_bytes


class Music:

    def __init__(self, file):
        self._file = file
        mutagen_file = mutagen.File(file, easy=True)
        self.tags = Tags(mutagen_file)
        self.artwork = mutagen_file["artwork"]
        self.mime_type = _get_mime_type(mutagen_file)

    @property
    def data_bytes(self):
        return self._file.read()


class Tags:

    _DEFAULT_TAGS = {
        "title": "unknown",
        "artist": "unknown",
        "album": "unknown",
    }

    def __init__(self, mutagen_filetype):
        if not isinstance(mutagen_filetype, _SUPPORTED_MUTAGEN_FILE_TYPES):
            raise RuntimeError("filetype: {0} not supported".format(mutagen_filetype.__class__))
        mutagen_tags = mutagen_filetype.tags
        self.title = self._get_tag_from_mutagen_tags(mutagen_tags, "title", self._DEFAULT_TAGS["title"])
        self.artist = self._get_tag_from_mutagen_tags(mutagen_tags, "artist", self._DEFAULT_TAGS["artist"])
        self.album = self._get_tag_from_mutagen_tags(mutagen_tags, "album", self._DEFAULT_TAGS["artist"])

    @staticmethod
    def _get_tag_from_mutagen_tags(mutagen_tags, key, default_value):
        # mutagenではタグはlistで扱うが、museではタグは単一で扱う
        val = mutagen_tags.get(key, default_value)
        if isinstance(val, list):
            if len(val) > 0:
                return val[0]
            else:
                return default_value
