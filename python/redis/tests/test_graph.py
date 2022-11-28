from redis import Redis

from graph import Graph


class TestGraph:
    def setup_class(self):
        self.client = Redis()

        self.graph = Graph(self.client, "test-graph")

        self.graph.add_edge("a", "b", 30)
        self.graph.add_edge("c", "b", 25)
        self.graph.add_multi_edges(("b", "d", 70), ("d", "e", 19))

    def test_edge(self):
        assert self.graph.has_edge("a", "b")

        assert self.graph.get_edge_weight("a", "b") == 30

    def test_edges(self):
        assert self.graph.get_all_edges() == {
            ("a", "b"),
            ("c", "b"),
            ("b", "d"),
            ("d", "e"),
        }

        assert self.graph.get_all_edges_with_weight() == {
            ("a", "b", 30),
            ("c", "b", 25),
            ("b", "d", 70),
            ("d", "e", 19),
        }
