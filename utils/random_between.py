import math


def random_between(min, max, seed):
    return int(abs(math.sin(seed))*(max-min+1)+min)

