from orders_generator.service.connection import Connection
import abc
from orders_generator.logger.Txt_file_loger.Txt_file_loger import Txt_file_logger

class Db_service(Connection):

    _logger = Txt_file_logger()

    def __init__(self, user, password, host, port, data_base):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.data_base = data_base

    @abc.abstractmethod
    def execute(self, query):
        pass
