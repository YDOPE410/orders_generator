class Storage:
    def __init__(self):
        self._storage = list()
        self._pushed = 0
        self._popped = 0
        self.generated = 0
        self.published = 0

    def push(self, item):
        self._storage.append(item)
        self._pushed += 1

    def get(self, amount):
        temp = self._storage[:amount]
        return temp

    def delete(self, amount):
        del self._storage[:amount]
        self._popped += amount


    def count(self):
        return len(self._storage)