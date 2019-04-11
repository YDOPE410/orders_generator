import abc
from decorator.benchmark import benchmark

class Report(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def write_report(data):
        pass

