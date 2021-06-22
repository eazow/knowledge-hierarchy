class AutoComplete:
    def __init__(self, client):
        self.client = client

    def feed(self, content, weight=1):
        for i in range(1, len(content)):
            key = "auto_complete_" + content[:i]
            self.client.zincrby(key, weight, content)

    def hint(self, prefix, count=10):
        key = "auto_complete_" + prefix
        return self.client.zrevrange(key, 0, count - 1)
