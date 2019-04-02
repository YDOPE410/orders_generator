from orders_generator.decorator.singleton import singleton


@singleton
class LCM:
    def __init__(self, X0, LCM_A, LCM_C, LCM_M):
        self.X0 = X0
        self.LCM_A = LCM_A
        self.LCM_C = LCM_C
        self.LCM_M = LCM_M

    def next(self):
        self.X0 = (self.X0 * self.LCM_A + self.LCM_C) % self.LCM_M
        return self.X0
