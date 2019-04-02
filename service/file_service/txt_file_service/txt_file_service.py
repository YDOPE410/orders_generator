from orders_generator.service.file_service.file_service import File_service


class Txt_file_service(File_service):

    def __init__(self, txt_file_path, mode):
        super(Txt_file_service, self).__init__(txt_file_path, mode)

    def open_connection(self):
        if not self._is_connected:
            try:
                self._handle = open(self.txt_file_path, self.mode)
                self._is_connected = True
                print(f"Connect to {self.txt_file_path} is open")
            except Exception as e:
                print(f"{e}. Unable to open connect to {self.txt_file_path}")
        else:
            print(f"Connect to {self.txt_file_path} is open")

    def close_connection(self):
        if self._is_connected:
            try:
                self._handle.close()
                self._is_connected = False
                print(f"Connect to {self.txt_file_path} is closed")
            except Exception as e:
                print(f"{e}. Unable to close connect to {self.txt_file_path}")
        else:
            print(f"Connect to {self.txt_file_path} is closed")

    def write(self, message):
        if self._is_connected:
            try:
                self._handle.write(message)
                return True
            except Exception as e:
                print(f"{e}. Unable to write at {self.txt_file_path}")
                return False
        else:
            print(f"ValueEror: I/O operation on closed file")
            return False

    def read_all(self):
        if self._is_connected:
            try:
                return self._handle.readlines()
            except Exception as e:
                print(f"{e}. Unable to read from {self.txt_file_path}")
        else:
            print(f"ValueEror: I/O operation on closed file")