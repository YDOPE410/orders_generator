from decorator.singleton import singleton

class Storage:
    def __init__(self):
        self._storage = list()
        self._pushed = 0
        self._popped = 0

    def push(self, item):
        self._storage.append(item)
        self._pushed += 1

    def pop(self, amount):
        temp = self._storage[:amount]
        del self._storage[:amount]
        self._popped += amount
        return temp

    def count(self):
        return len(self._storage)