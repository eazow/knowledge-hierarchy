def make_edge_name_from_vertexs(start, end):
    return str(start) + "->" + str(end)


def decompose_vertexs_from_edge_name(name):
    return name.split("->")


class Graph:
    def __init__(self, client, key):
        self.client = client
        self.key = key

    def add_edge(self, start, end, weight):
        edge = make_edge_name_from_vertexs(start, end)
        self.client.hset(self.key, edge, weight)

    def remove_edge(self, start, end):
        edge = make_edge_name_from_vertexs(start, end)
        return self.client.hdel(self.key, edge)

    def get_edge_weight(self, start, end):
        edge = make_edge_name_from_vertexs(start, end)
        return self.client.hget(self.key, edge)

    def has_edge(self, start, end):
        edge = make_edge_name_from_vertexs(start, end)

        return self.client.hexists(self.key, edge)

    def add_multi_edges(self, *tuples):
        nodes_and_weights = {}

        for start, end, weight in tuples:
            edge = make_edge_name_from_vertexs(start, end)
            nodes_and_weights[edge] = weight

        self.client.hmset(self.key, nodes_and_weights)

    def get_multi_edge_weights(self, *tuples):
        edge_list = []

        for start, end in tuples:
            edge = make_edge_name_from_vertexs(start, end)
            edge_list.append(edge)

        return self.client.hmget(self.key, edge_list)

    def get_all_edges(self):
        edges = self.client.hkeys(self.key)

        result = set()
        for edge in edges:
            start, end = decompose_vertexs_from_edge_name(edge)
            result.add((start, end))

        return result

    def get_all_edges_with_weight(self):
        edges_and_weights = self.client.hgetall(self.key)

        result = set()

        for edge, weight in edges_and_weights.items():
            start, end = decompose_vertexs_from_edge_name(edge)
            result.add((start, end, weight))

        return result
