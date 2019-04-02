import abc

class Generator(abc.ABC):

    @abc.abstractmethod
    def generate(self):
        pass

    @abc.abstractmethod
    def generate_batch(self, amount):
        pass