class MessageQueue:
    def __init__(self, client, queue_name):
        self.client = client
        self.queue_name = queue_name
        self.client.ltrim(self.queue_name, 1, 0)

    def add_message(self, message):
        self.client.rpush(self.queue_name, message)

    def get_message(self, timeout=0):
        result = self.client.blpop(self.queue_name, timeout)
        if result is not None:
            source_queue, poped_item = result
            return str(poped_item, encoding="utf8")
        return None

    def len(self):
        return self.client.llen(self.queue_name)

    def clear(self):
        return self.client.ltrim(self.queue_name, 1, 0)
