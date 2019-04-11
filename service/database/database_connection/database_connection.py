import abc


class Database_connection(abc.ABC):

    @abc.abstractmethod
    def __init__(self, user, password, host, port, database_name):
        pass

    @abc.abstractmethod
    def open_connection(self):
        pass

    @abc.abstractmethod
    def close_connection(self):
        pass

    @abc.abstractmethod
    def _reconnect(self):
        pass

