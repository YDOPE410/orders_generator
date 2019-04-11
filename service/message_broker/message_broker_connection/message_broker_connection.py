import abc

class Message_broker_connection(abc.ABC):

    @abc.abstractmethod
    def open_connection(self):
        pass

    @abc.abstractmethod
    def close_connection(self):
        pass
