import abc
from orders_generator.decorator.benchmark import benchmark

class Report(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def write_report(data):
        pass

