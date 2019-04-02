import abc
from orders_generator.service.connection import Connection


class File_service(Connection):


    @abc.abstractmethod
    def __init__(self, file_path, mode):
        self.txt_file_path = file_path
        self.mode = mode