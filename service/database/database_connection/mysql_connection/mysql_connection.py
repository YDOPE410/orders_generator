import pymysql
import time
from service.database.database_connection.database_connection import Database_connection
from constant import constants_reconnect



class Mysql_connection(Database_connection):
    def __init__(self, user, password, host, port, database_name):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name
        self.connection = None

    def open_connection(self):
        try:
            self.connection = self._open_connection()
        except pymysql.MySQLError:
            self.connection = self._reconnect()


    def _open_connection(self):
        connection = pymysql.connect(user=self.user,
                                     password=self.password,
                                     host=self.host,
                                     port=self.port,
                                     database=self.database_name)
        return connection

    def close_connection(self):
        try:
            self.connection.close()
        except pymysql.MySQLError:
            print("Cant close connection")

    def _reconnect(self):
        for i in range(constants_reconnect.NUMBERS_TO_RECONNECT):
            try:
                connection = self._open_connection()
                return connection
            except:
                time.sleep(constants_reconnect.RECONNECT_TIMEOUT)
                print("reconnect myqsl")

