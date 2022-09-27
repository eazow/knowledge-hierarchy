from redis import Redis

from recommendation import Recommendation


class TestRecommendation:
    def setup_class(self):
        self.client = Redis(decode_responses=True)

    def test_recommendation(self):
        recommendation = Recommendation(self.client)

        recommendation.forward_to("book1", "book2")
        recommendation.forward_to("book1", "book2")
        recommendation.forward_to("book1", "book2")
        recommendation.forward_to("book1", "book3")
        recommendation.forward_to("book1", "book3")
        recommendation.forward_to("book1", "book4")
        recommendation.forward_to("book1", "book5")
        recommendation.forward_to("book1", "book6")
        recommendation.forward_to("book1", "book6")

        assert recommendation.get_recommendations("book1", 1, 5) == [
            "book2",
            "book6",
            "book3",
            "book5",
            "book4",
        ]

        assert recommendation.get_recommendations("book1", 1, 5, with_time=True) == [
            ("book2", 3),
            ("book6", 2),
            ("book3", 2),
            ("book5", 1),
            ("book4", 1),
        ]

    def teardown_class(self):
        keys = [k for k in self.client.keys()]
        self.client.delete(*keys)
        self.client.close()
