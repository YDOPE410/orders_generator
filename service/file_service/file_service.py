import abc
from orders_generator.service.connection import Connection
from orders_generator.logger.Txt_file_loger.Txt_file_loger import Txt_file_logger

class File_service(Connection):

    _logger = Txt_file_logger()

    @abc.abstractmethod
    def __init__(self, file_path, mode):
        self.txt_file_path = file_path
        self.mode = mode