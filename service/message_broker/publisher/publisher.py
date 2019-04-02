import abc


class Publisher(abc.ABC):

    def __init__(self, channel):
        self.channel = channel

    @abc.abstractmethod
    def publish(self, exchange, routing_key, message):
        pass