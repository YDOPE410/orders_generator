from orders_generator.service.db_service.db_service import Db_service
import pymysql

class Mysql_service(Db_service):

    def __init__(self, user, password, host, port, data_base):
        super(Mysql_service, self).__init__(user, password, host, port, data_base)
        self.uncommited = 0


    def open_connection(self):
        if not self._is_connected:
            try:

                self._connect = pymysql.connect(host=self.host,
                                                port=self.port,
                                                user=self.user,
                                                passwd=self.password,
                                                db=self.data_base)
                self._is_connected = True
                self._logger.debug(f"Connect to {self.data_base} is opened")
            except Exception as e:
                self._logger.error(f"{e}. Unable to connect to {self.data_base}")
        else:
            self._logger.debug(f"Connect to {self.data_base} is opened")

    def close_connection(self):
        if self._is_connected:
            try:
                self._connect.close()
                self._is_connected = False
                self._logger.debug(f"Connect to {self.data_base} closed")
            except Exception as e:
                self._logger.error(f"{e}. Unable to close connection to {self.data_base}")
        else:
            self._logger.debug(f"Connect to {self.data_base} closed")


    def execute(self, query):
        if self._is_connected:
            try:
                cursor = self._connect.cursor()
                cursor.execute(query)
                self.uncommited += 1
                return True
            except Exception as e:
                self._logger.error(f"{e}. {query} not executed")
                self._connect.rollback()
                self._logger.debug(f"rollback database")
                self.uncommited = 0
                return False
        else:
            self._logger.debug("Mysql connect is close. Can`t execute")
            return False

    def commit(self):
        try:
            self._connect.commit()
            self.uncommited = 0
        except Exception as e:
            self._logger.error(f"{e}. Unable to commit at {self.data_base}")

