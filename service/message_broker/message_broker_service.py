from orders_generator.service.connection import Connection
import abc

class Message_broker_service(Connection):


    def __init__(self, user, password, host, virtual_host, port):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.virtual_host = virtual_host

    @abc.abstractmethod
    def get_channel(self):
        pass

    @abc.abstractmethod
    def close_channel(self, channel):
        pass