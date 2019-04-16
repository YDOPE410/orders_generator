from service.database.database import Database_service
import pymysql
import time
from constant.constants_reconnect import *


class Mysql_service(Database_service):
    def __init__(self, user, password, host, port, database):
        super(__class__, self).__init__(user, password, host, port, database)
        self.connection = None

    def open_connection(self):
        try:
            self.logger.debug(f"Trying open connection to {self.database}")
            self.connection = self._open_connection()
            self.logger.debug(f"Connected to {self.database}")
        except pymysql.MySQLError as e:
            self.logger.error(f"Cant connect to {self.database}")
            self.logger.error(e)
            self._reconnect()
            self.logger.debug(f"Reconnected to {self.database}")


    def _open_connection(self):
        return pymysql.connect(host=self.host, port=self.port, user=self.user,
                                              password=self.password, database=self.database)

    def _reconnect(self):
        self.logger.debug(f"Trying reconnect to {self.database}")
        for i in range(NUMBERS_TO_RECONNECT):
            try:
                self._open_connection()
                return
            except Exception as e:
                    self.logger.error(f"Reconnect failed. {e}")
                    if i+1 < NUMBERS_TO_RECONNECT:
                        self.logger.info(f"{RECONNECT_TIMEOUT} sec to reconnect")
                        time.sleep(RECONNECT_TIMEOUT)
        self.logger.fatal(f"Cant connect to {self.database} after {NUMBERS_TO_RECONNECT} reconnects")
        exit(1)

    def close_connection(self):
        try:
            self.connection.close()
            self.logger.debug(f"Connection to {self.database} closed")
        except Exception as e:
            self.logger.error(f"Cant close connection to {self.database}. {e}")

    def execute(self, query):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            self.logger.error(e)
            self._reconnect()
            self.logger.debug(f"Reconnected to {self.database}")
            return False
        except Exception as e:
            self.logger.error(f"Cant execute query {query}. {e}")
            return False



    def commit(self):
        try:
            self.connection.commit()
        except Exception as e:
            self.logger.error(e)

