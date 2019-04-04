from orders_generator.decorator.singleton import singleton

@singleton
class Metric_storage:

    def __init__(self):
        self.storage = dict()

    def add_to_storage(self, key, value):
        if key not in self.storage:
            self.storage[key] = []
        self.storage[key].append(value)
