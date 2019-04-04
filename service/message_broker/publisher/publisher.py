import abc
from orders_generator.logger.Txt_file_loger.Txt_file_loger import Txt_file_logger

class Publisher(abc.ABC):
    _logger = Txt_file_logger()

    @abc.abstractmethod
    def publish(self, exchange, routing_key, message):
        pass