import abc

class Message_broker(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def add_publisher(self,channel_number, publisher_name, exchange, exchange_type, queue, routing_keys):
        pass

    @abc.abstractmethod
    def add_consumer(self,channel_number, consumer_name, queue):
        pass