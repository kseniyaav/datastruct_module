from main import Channel

class TestChannel:

    def test_str(self):
        ch1 = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
        assert str(ch1) == "Youtube-канал: " + ch1.title

    def test_add(self):
        ch1 = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
        ch2 = Channel('UC1eFXmJNkjITxPFWTy6RsWg')
        assert (ch1 + ch2) == ch1.url + ' ' + ch2.url

    def test_gt_lt(self):
        ch1 = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
        ch2 = Channel('UC1eFXmJNkjITxPFWTy6RsWg')
        assert ch1 > ch2
        assert not ch1 < ch2


