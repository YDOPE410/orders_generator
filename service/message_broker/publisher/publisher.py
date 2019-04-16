import abc
from logger.Txt_file_loger.Txt_file_loger import Txt_file_logger


class Publisher(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        self.logger = Txt_file_logger()

    @abc.abstractmethod
    def publish(self, message):
        pass