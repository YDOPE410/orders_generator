import abc
from orders_generator.constant import constants_logger

class Logger(abc.ABC):
    _log_lvl = 1

    @abc.abstractmethod
    def write_log(self, log_type, message):
        pass

    def set_log_lvl(self, log_lvl):
        print(f"Change log_lvl from {self._log_lvl} to {log_lvl}")
        self._log_lvl = log_lvl
