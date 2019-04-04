from orders_generator.service.file_service.file_service import File_service
import os

class Txt_file_service(File_service):

    def __init__(self, txt_file_path, mode):
        super(Txt_file_service, self).__init__(txt_file_path, mode)

    def open_connection(self):
        if not self._is_connected:
            if not os.path.exists(self.txt_file_path[:self.txt_file_path.rfind('/')]):
                os.makedirs(self.txt_file_path[:self.txt_file_path.rfind('/')])
            try:
                self._handle = open(self.txt_file_path, self.mode)
                self._is_connected = True
                self._logger.debug(f"Connect to {self.txt_file_path} is opened")
            except Exception as e:
                self._logger.error(f"{e}. Unable to open connect to {self.txt_file_path}")
        else:
            self._logger.debug(f"Connect to {self.txt_file_path} is open")

    def close_connection(self):
        if self._is_connected:
            try:
                self._handle.close()
                self._is_connected = False
                self._logger.debug(f"Connect to {self.txt_file_path} is closed")
            except Exception as e:
                self._logger.error(f"{e}. Unable to close connect to {self.txt_file_path}")
        else:
            self._logger.debug(f"Connect to {self.txt_file_path} is closed")

    def write(self, message):
        if self._is_connected:
            try:
                self._handle.write(message)
                return True
            except Exception as e:
                self._logger.error(f"{e}. Unable to write at {self.txt_file_path}")
                return False
        else:
            self._logger.debug(f"ValueEror: I/O operation on closed file")
            return False

    def read_all(self):
        if self._is_connected:
            try:
                return self._handle.readlines()
            except Exception as e:
                self._logger.error(f"{e}. Unable to read from {self.txt_file_path}")
        else:
            self._logger.debug(f"ValueEror: I/O operation on closed file")

    def change_mod(self, mode):
        try:
            self._handle = open(self.txt_file_path, mode)
            self._logger.debug(f"Changed mod {self.txt_file_path} to '{mode}'")
        except Exception as e:
            self._logger.error(f"{e}. Unable to change mod to {self.txt_file_path}")