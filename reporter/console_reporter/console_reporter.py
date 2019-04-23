from reporter.reporter import Report
from constant.constants_sql_queryes import REPORT

class Console_reporter(Report):

    @staticmethod
    def write_report(data, mysql):
        print()
        for key in data:
            value = data[key]

            if len(value) > 1:
                max_value = max(value)
                min_value = min(value)
                avg_value = sum(value) / len(value)
                total = sum(value)

                print(key)
                print(f'Max: {max_value} ms')
                print(f'Min: {min_value} ms')
                print(f'Avg: {avg_value} ms')
                print(f'Totat: {total} ms')
            else:
                print(f'{key}: {value[0]} ms')

        report_from_sql = mysql.execute(REPORT)
        print(f"Orders count in database: {report_from_sql[0][0] if report_from_sql[0][0] else 0}")
        print(f"Orders from green zone in database count: {report_from_sql[1][0] if len(report_from_sql) > 0 else 0}")
        print(f"Orders from red zone in database count: {report_from_sql[2][0] if len(report_from_sql) > 1 else 0}")
        print(f"Orders from blue zone in database count: {report_from_sql[3][0] if len(report_from_sql) > 2 else 0}")
        print("----")