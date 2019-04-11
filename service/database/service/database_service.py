import abc


class Database_service(abc.ABC):

    @abc.abstractmethod
    def __init__(self, connection):
        pass

    @abc.abstractmethod
    def execute(self, query):
        pass

    @abc.abstractmethod
    def commit(self):
        pass

