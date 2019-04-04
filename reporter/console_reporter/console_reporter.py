from orders_generator.reporter.reporter import Report

class Console_reporter(Report):

    @staticmethod
    def write_report( data):
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

        print("----")