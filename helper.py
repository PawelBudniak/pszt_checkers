

def average(x, y):
    return int((x + y) / 2)


def sgn(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


class Point:

    def __init__(self, y, x):
        self.x = x
        self.y = y

    def __str__(self):
        return f'Point({self.y},{self.x})'

    def __repr__(self):
        return self.__str__()
