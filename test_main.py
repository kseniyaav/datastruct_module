import pytest
from main import Channel

@pytest.fixture(params=['UCMCgOm8GZkHp8zJ6l7_hIuA', 'UCBPCXV9oYpYkGGK6DZHDGKw'])
def channel(request):
    return Channel(request.param)

class TestItem:

    def test_str(self, channel):
        assert str(channel) == "Youtube-канал: " + channel.title

    def test_add(self, channel):
        ch2 = Channel('UCBPCXV9oYpYkGGK6DZHDGKw')
        assert (channel + ch2) == channel.url + ' ' + ch2.url

    def test_gt_lt(self, channel):
        ch2 = Channel('UCBPCXV9oYpYkGGK6DZHDGKw')
        assert channel >= ch2
        assert not channel <= ch2


