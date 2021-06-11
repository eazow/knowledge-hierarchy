from redis import Redis

from counter import Counter


class TestCounter:
    def setup_class(self):
        self.client = Redis()

    def test_increase(self):
        product_1_counter = Counter(self.client, "counter", "product_1")
        product_1_counter.reset()

        product_1_counter.increase()
        product_1_counter.increase()
        assert product_1_counter.get() == 2

    def test_decrease(self):
        product_2_counter = Counter(self.client, "counter", "product_2")
        product_2_counter.reset()

        product_2_counter.increase(100)
        product_2_counter.decrease()
        product_2_counter.decrease()
        assert product_2_counter.get() == 98
