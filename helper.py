
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

    def __init__(self, x, y):
        self.x = x
        self.y = y
