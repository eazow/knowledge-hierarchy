def make_record_key(origin):
    return "forward_to_record_{0}".format(origin)


class Recommendation:
    def __init__(self, client):
        self.client = client

    def forward_to(self, origin, destination):
        key = make_record_key(origin)
        self.client.zincrby(key, 1, destination)

    def get_recommendations(self, origin, page, count, with_time=False):
        key = make_record_key(origin)
        start_index = (page - 1) * count
        end_index = page * count - 1
        return self.client.zrevrange(
            key, start_index, end_index, withscores=with_time, score_cast_func=int
        )
