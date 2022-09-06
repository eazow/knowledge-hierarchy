from auto_complete import AutoComplete
from redis import Redis

from inverted_index import InvertedIndex


class TestAutoComplete:
    def setup_class(self):
        self.client = Redis(decode_responses=True)

    def test_auto_complete(self):
        auto_complete = AutoComplete(self.client)
        auto_complete.feed("黄晓明", 3)
        auto_complete.feed("黄建宏", 2)
        auto_complete.feed("黄晓军", 1)

        assert auto_complete.hint("黄") == ["黄晓明", "黄建宏", "黄晓军"]
        assert auto_complete.hint("黄晓") == ["黄晓明", "黄晓军"]

    def teardown_class(self):
        keys = [k for k in self.client.keys()]
        self.client.delete(*keys)
        self.client.close()
