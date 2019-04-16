import abc
from logger.Txt_file_loger.Txt_file_loger import Txt_file_logger


class Database_service(abc.ABC):
    @abc.abstractmethod
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.logger = Txt_file_logger()

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
    def execute(self, query):
        pass


