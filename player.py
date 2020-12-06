from helper import Point

class Player:

    def __init__(self, is_white):
        self.is_white = is_white

    def get_move(self, board):
        moves = input(
            "Is white = " + str(self.is_white) + "\nEnter coordinates: <from_y> <from_x> <to_y> <to_x>").split()
        moves = [int(x) for x in moves]  # albo result = list(map(int, moves))
        result = []
        for i in range(0, len(moves), 2):
            result.append(Point(moves[i], moves[i+1]))
        if result[0] is None:
            exit(1)
        print(result)
        return result

    def keeps_cache(self):
        return False

    def get_pieces(self, board):
        return board.get_pieces(self)