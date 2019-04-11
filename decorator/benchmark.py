import time
from reporter.metric_storage.metric_storage import Metric_storage
from constant.constants_date import ONE_SECOND_IN_MILLISECONDS


def benchmark(func):

    def wrapper(*args, **kwargs):
        storage = Metric_storage()
        start = time.perf_counter()
        res = func(*args, **kwargs)
        storage.add_to_storage(func.__name__, (time.perf_counter() - start) * ONE_SECOND_IN_MILLISECONDS)
        return res

    return wrapper