import pytest
from main import Channel, Video, PLVideo

class TestChannel:

    def test_str(self):
        ch1 = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
        assert str(ch1) == "Youtube-канал: " + ch1.title

    def test_add(self):
        ch1 = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
        ch2 = Channel('UC1eFXmJNkjITxPFWTy6RsWg')
        assert (ch1 + ch2) == 14000000

    def test_gt_lt(self):
        ch1 = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
        ch2 = Channel('UC1eFXmJNkjITxPFWTy6RsWg')
        assert ch1 > ch2
        assert not ch1 < ch2

@pytest.fixture()
def video():
    return Video(video_id='9lO06Zxhu88')

@pytest.fixture
def pl_video():
    return PLVideo(video_id='BBotskuyw_M', playlist_id='PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')

class TestVideo:

    def test_str_video(self, video):
        assert str(video) == 'Как устроена IT-столица мира / Russian Silicon Valley (English subs)'

class TestPLVideo:

    def test_str_plv(self, pl_video):
        assert str(pl_video) == 'Пушкин: наше все? (Литература)'

    def test_playlist_title(self, pl_video):
        assert pl_video.get_playlist_title(pl_video.playlist_id) == "Литература"


