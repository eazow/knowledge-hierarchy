from redis import Redis

from inverted_index import InvertedIndex


class TestInvertedIndex:
    def setup_class(self):
        self.client = Redis(decode_responses=True)

        self.laptops = laptops = InvertedIndex(self.client)
        laptops.add_index("MacBook Pro", "Apple", "MacOS", "13inch")
        laptops.add_index("MacBook Air", "Apple", "MacOS", "13inch")

        laptops.add_index("X1 Carbon", "ThinkPad", "Windows", "13inch")

        laptops.add_index("T450", "ThinkPad", "Windows", "14inch")

        laptops.add_index("XPS", "DELL", "Windows", "13inch")

    def test_get_keywords(self):
        assert {"Apple", "MacOS", "13inch"} == self.laptops.get_keywords("MacBook Pro")

    def test_get_items(self):
        assert self.laptops.get_items("13inch") == {"MacBook Pro", "MacBook Air", "X1 Carbon", "XPS"}
        assert self.laptops.get_items("13inch", "Apple") == {"MacBook Pro", "MacBook Air"}

    def teardown_class(self):
        self.client.close()
