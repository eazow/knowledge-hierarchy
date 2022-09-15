from redis import Redis

from message_queue import MessageQueue


class TestMessageQueue:
    def setup_class(self):
        self.client = Redis()

        self.mq = MessageQueue(self.client, "email_queue")

        self.mq.add_message("peter@example.com")
        self.mq.add_message("jack@spam.com")
        self.mq.add_message("tom@blah.com")

    def test_len(self):
        assert self.mq.len() == 3

    def test_consume(self):
        assert self.mq.get_message() == "peter@example.com"
        assert self.mq.get_message() == "jack@spam.com"
        assert self.mq.get_message() == "tom@blah.com"
