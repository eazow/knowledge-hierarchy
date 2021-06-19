def get_item_key(item):
    return "inverted_index_" + item + "_keywords"


def get_keyword_key(keyword):
    return "inverted_index_" + keyword + "_items"


class InvertedIndex:
    def __init__(self, client):
        self.client = client

    def add_index(self, item, *keywords):
        item_key = get_item_key(item)
        result = self.client.sadd(item_key, *keywords)

        for keyword in keywords:
            keyword_key = get_keyword_key(keyword)
            self.client.sadd(keyword_key, item)
        return result

    def remove_index(self, item, *keywords):
        item_key = get_item_key(item)
        result = self.client.srem(item_key, *keywords)

        for keyword in keywords:
            keyword_key = get_keyword_key(keyword)
            self.client.srem(keyword_key, item)
        return result

    def get_keywords(self, item):
        return self.client.smembers(get_item_key(item))

    def get_items(self, *keywords):
        keyword_keys = map(get_keyword_key, keywords)
        return self.client.sinter(*keyword_keys)
