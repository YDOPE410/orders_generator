import abc
from logger.Txt_file_loger.Txt_file_loger import Txt_file_logger


class Message_broker(abc.ABC):
    @abc.abstractmethod
    def __init__(self, user, password, host, virtual_host, port):
        self.logger = Txt_file_logger()
        self.user = user
        self.password = password
        self.host = host
        self.virtual_host = virtual_host
        self.port = port

    @abc.abstractmethod
    def open_connection(self):
        pass

    @abc.abstractmethod
    def close_connection(self):
        pass

    @abc.abstractmethod
    def _reconnect(self):
        pass

    @abc.abstractmethod
    def add_publisher(self, publisher_name, exchange, exchange_type, queue, routing_keys):
        pass

    @abc.abstractmethod
    def add_consumer(self, consumer_name, queue):
        pass