class Counter:
    def __init__(self, client, hash_key, counter_name):
        self.client = client
        self.hash_key = hash_key
        self.counter_name = counter_name

        def increase(self, n=1):
            return self.client.hincrby(self.hash_key, self.counter_name, n)

        def decrease(self, n=1):
            return self.client.hincrby(self.hash_key, self.counter_name, -n)

        def get(self):
            value = self.client.hget(self.hash_key, self.counter_name)
            return 0 if value is None else int(value)

        def reset(self):
            self.client.hset(self.hash_key, self.counter_name, 0)
