import abc
from logger.Txt_file_loger.Txt_file_loger import Txt_file_logger

class Consumer(abc.ABC):
    @abc.abstractmethod
    def __init__(self, queue, message_broker, storage):
        self.logger = Txt_file_logger()
        self.queue = queue
        self.message_broker = message_broker
        self.storage = storage


    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def run(self):
        pass