from datetime import datetime
from orders_generator.reporter.metric_storage.metric_storage import Metric_storage


def benchmark(func):

    def wrapper(*args, **kwargs):
        storage = Metric_storage()
        start = datetime.now()
        res = func(*args, **kwargs)
        storage.add_to_storage(func.__name__, (datetime.now() - start).total_seconds() * 1000)
        return res

    return wrapper