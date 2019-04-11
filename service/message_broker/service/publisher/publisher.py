import abc

class Publisher(abc.ABC):
    @abc.abstractmethod
    def __init__(self, channel, exchange, routing_keys):
        pass

    @abc.abstractmethod
    def publish(self, message):
        pass