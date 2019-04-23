import threading
from constant.constants_sql_queryes import REPORT
import time


class Background_reporter(threading.Thread):
    def __init__(self, mysql, storage):
        threading.Thread.__init__(self)
        self.generated = 0
        self.published = 0
        self.inserted = 0
        self.consumed = 0
        self._storage = storage
        self._mysql = mysql

    def run(self):

        while True:
            self._mysql.open_connection()
            self.generated = self._storage.generated
            self.published = self._storage.published
            self.consumed = self._storage._pushed
            self.inserted = self._storage._popped

            report_from_sql = self._mysql.execute(REPORT)
            print(f"Records generated: {self.generated}")
            print(f"Records published to message broker: {self.published}")
            print(f"Records consumed from message broker: {self.consumed}")
            print(f"Records inserted to database: {self.inserted}")
            print(f"Orders count in database: {report_from_sql[0][0] if len(report_from_sql)>0 else 0}")
            print(f"Orders from green zone in database count: {report_from_sql[1][0] if len(report_from_sql)>1 else 0}")
            print(f"Orders from red zone in database count: {report_from_sql[2][0] if len(report_from_sql)>2 else 0}")
            print(f"Orders from blue zone in database count: {report_from_sql[3][0] if len(report_from_sql)>3 else 0}")
            if self.consumed == self.inserted and not self.consumed == 0:
                break
            time.sleep(3)

            self._mysql.close_connection()
