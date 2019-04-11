import pymysql

from service.database.service.database_service import Database_service

class Mysql_service(Database_service):

    def __init__(self, connection):
        self.connection = connection
        self.uncommited = 0

    def execute(self, query):
        try:
            with self.connection.connection.cursor() as cursor:
                cursor.execute(query)
            self.uncommited += 1
            return True
        except Exception as e:
            print(e)
            self.connection.connection.rollback()
            return False

    def commit(self):
        try:
            self.connection.connection.commit()
            self.uncommited = 0
        except Exception as e:
            print("Cant commit")
