from orders_generator.service.connection import Connection
import abc

class Db_service(Connection):

    def __init__(self, user, password, host, port, data_base):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.data_base = data_base

    @abc.abstractmethod
    def execute(self, query):
        pass
