# coding: utf-8
import unittest
import muse.audio


class AudioTest(unittest.TestCase):

    def test_parse_m4a_tags(self):
        m4a_path = r"C:\Users\phone\Desktop\01 覚醒~Alternative Heart~.m4a"
        m = muse.audio.Music(m4a_path)
        self.assertTrue(m.tags.title == "覚醒~Alternative Heart~")
        self.assertTrue(m.tags.artist == "広瀬こはる(CV:橋本ちなみ), オルタナティブガールズ, 水島愛梨(CV:遠藤ゆりか), 西園寺玲(CV:木戸衣吹), 悠木美弥花(CV:竹達彩奈), 天堂真知(CV:安済知佳) & 橘直美(CV:大空直美)")
        self.assertTrue(m.artwork.mime_type == "image/jpeg")

    def test_parse_mp3_tags(self):
        path = r"C:\Users\phone\Desktop\01. きらめきっ！の日.mp3"
        m = muse.audio.Music(path)
        self.assertTrue(m.tags.title == "きらめきっ！の日")
        self.assertTrue(m.tags.artist == "情報処理部")
        self.assertTrue(m.artwork.mime_type == "image/jpeg")
