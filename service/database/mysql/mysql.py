from service.database.database import Database_service
import pymysql
import time
from constant.constants_reconnect import *
import threading


class Mysql_service(Database_service):
    def __init__(self, user, password, host, port, database):
        super(__class__, self).__init__(user, password, host, port, database)
        self.connections = dict()
        self.uncomminted = 0

    def open_connection(self):
        try:
            self.logger.debug(f"Trying open connection to {self.database}")
            self._open_connection()
            self.logger.debug(f"Connected to {self.database}")
        except pymysql.MySQLError as e:
            self.logger.error(f"Cant connect to {self.database}")
            self.logger.error(e)
            self._reconnect()
            self.logger.debug(f"Reconnected to {self.database}")

    def _get_connection(self):
        connection_id = threading.current_thread().name
        connection = None
        try:
            connection = self.connections[connection_id]
        except KeyError:
            self.logger.error(f"No connection for thread {connection_id}")
        return connection

    def _open_connection(self):
        connection_id = threading.current_thread().name
        if connection_id in self.connections:
            if self.connections[connection_id].open:
                self.logger.info(f"Connection already opened in thread {connection_id}")
                return
        connection = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                              password=self.password, database=self.database)
        self.connections[connection_id] = connection

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
            connection = self._get_connection()
            connection.close()
            self.logger.debug(f"Connection to {self.database} closed")
        except Exception as e:
            self.logger.error(f"Cant close connection to {self.database}. {e}")

    def execute(self, query):
        try:
            with self._get_connection().cursor() as cursor:
                cursor.execute(query)
                self.uncomminted += 1
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            self.logger.error(e)
            self._reconnect()
            self.logger.debug(f"Reconnected to {self.database}")
            with self._get_connection().cursor() as cursor:
                cursor.execute(query)
                self.uncomminted += 1
                return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"Cant execute query {query}. {e}")



    def commit(self):
        try:
            self._get_connection().commit()
            self.uncomminted = 0
        except Exception as e:
            self.logger.error(e)

