import pytest
import datetime
from unittest.mock import patch, Mock
from main import YoutubeAPI, Channel, Video, PLVideo, PlayList


@pytest.fixture
def video():
    return Video(video_id='9lO06Zxhu88')


@pytest.fixture
def pl_video():
    return PLVideo(video_id='BBotskuyw_M', playlist_id='PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')

class TestChannel:

    def test_str(self):
        ch1 = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
        assert str(ch1) == "Youtube-канал: " + ch1.title

    def test_add(self):
        ch1 = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
        ch2 = Channel('UC1eFXmJNkjITxPFWTy6RsWg')
        assert (ch1 + ch2) == 14010000

    def test_gt_lt(self):
        ch1 = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
        ch2 = Channel('UC1eFXmJNkjITxPFWTy6RsWg')
        assert ch1 > ch2
        assert not ch1 < ch2


class TestVideo:

    def test_str_video(self, video):
        assert str(video) == 'Как устроена IT-столица мира / Russian Silicon Valley (English subs)'


class TestPLVideo:

    def test_str_plv(self, pl_video):
        assert str(pl_video) == 'Пушкин: наше все? (Литература)'

    def test_playlist_title(self, pl_video):
        assert pl_video.get_playlist_title(pl_video.playlist_id) == "Литература"


class TestPlaylist:
    def test_create_playlist(self):
        playlist = PlayList("PLguYHBi01DWqQBZjoPuYZ0F-nTGUBNec8")
        assert playlist.title == "Редакция. Интервью"
        assert playlist.url == "https://www.youtube.com/playlist?list=PLguYHBi01DWqQBZjoPuYZ0F-nTGUBNec8"
        assert playlist.total_duration == datetime.timedelta(seconds=0)
        assert len(playlist._videos) == 0

    def test_create_playlist_not_found(self):
        with pytest.raises(ValueError):
            PlayList("PLguYHBi01DWqQBZjoPuYZ0F-nTGUBNec9")

    def test_add_video(self):
        playlist = PlayList("PLguYHBi01DWqQBZjoPuYZ0F-nTGUBNec8")
        playlist.add_video("LTTiQePlxf0")
        assert len(playlist._videos) == 1

    def test_total_duration(self):
        playlist = PlayList("PLguYHBi01DWqQBZjoPuYZ0F-nTGUBNec8")
        video1 = PLVideo("fO9VezVjenY", "PLguYHBi01DWqQBZjoPuYZ0F-nTGUBNec8", duration=datetime.timedelta(seconds=1930))
        video2 = PLVideo("2L5kjeGZOLc", "PLguYHBi01DWqQBZjoPuYZ0F-nTGUBNec8", duration=datetime.timedelta(seconds=2508))
        playlist._videos = [video1, video2]
        assert playlist.total_duration == datetime.timedelta(seconds=4530)

    def test_show_best_video(self):
        playlist = PlayList("PLguYHBi01DWqQBZjoPuYZ0F-nTGUBNec8")
        video1 = PLVideo("fO9VezVjenY", "PLguYHBi01DWqQBZjoPuYZ0F-nTGUBNec8", like_count=25000)
        video2 = PLVideo("2L5kjeGZOLc", "PLguYHBi01DWqQBZjoPuYZ0F-nTGUBNec8", like_count=27000)
        playlist._videos = [video1, video2]
        assert playlist.show_best_video() == "https://www.youtube.com/2L5kjeGZOLc"

