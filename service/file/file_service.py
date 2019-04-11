import abc
from logger.Txt_file_loger.Txt_file_loger import Txt_file_logger

class File_service(abc.ABC):

    _logger = Txt_file_logger()

    @abc.abstractmethod
    def __init__(self, file_path, mode):
        self.txt_file_path = file_path
        self.mode = mode

    @abc.abstractmethod
    def open_connection(self):
        pass

    def close_connection(self):
        pass