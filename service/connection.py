import abc


class Connection(abc.ABC):
    _is_connected = False

    @abc.abstractmethod
    def open_connection(self):
        pass

    @abc.abstractmethod
    def close_connection(self):
        pass

    def is_connected(self):
        pass

