import abc

class Config_loader(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def load(file_path):
        pass
