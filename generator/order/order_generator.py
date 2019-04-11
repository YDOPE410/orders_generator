from generator.generator import Generator


class Order_generator(Generator):

    def __init__(self, zone_generator):
        self._zone_generator = zone_generator

    def change_zone(self, zone_generator):
        self._zone_generator = zone_generator

    def generate_batch(self, amount):
        result = list()
        for i in range(amount):
            result += self.generate()
        return result

    def generate(self):
        return self._zone_generator.generate()