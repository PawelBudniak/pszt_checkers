

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

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        return (self.x < other.x and self.y < other.y or
                self.x == other.x and self.y < other.x)

