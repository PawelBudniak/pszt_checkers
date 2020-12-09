from helper import Point


class Player:

    def __init__(self, is_white):
        self.is_white = is_white

    def get_move(self, board):
        if self.is_white:
            print("\n* * * White player's turn * * *")
        else:
            print("\n* * * Black player's turn * * *")
        moves = input("Choose destined piece path in the desired order.\n"
                      "Input format: <from_y> <from_x> <to_y1> <to_x1>...<to_xn> <to_yn>"
                      "\nEnter <quit> to end the game.\n" "Enter coordinates: ").split()
        if len(moves) == 1 and moves[0] == "quit":
            return moves
        if len(moves) < 2:
            print("\nERROR: Wrong path choice")
            return
        for move in moves:
            if not move.isdecimal():
                print("\nERROR: Wrong format! Input gathers digits only!")
                return
            elif int(move) not in range(0, board.BOARD_SIZE):
                print("\nERROR: Choice out of bounds!")
                return
        moves = [int(x) for x in moves]  # albo result = list(map(int, moves))
        result = []
        for i in range(0, len(moves), 2):
            result.append(Point(moves[i], moves[i + 1]))
        if result[0] is None:
            exit(1)
        print("Chosen path: " + str(result))
        return result

    def keeps_cache(self):
        return False

    def get_pieces(self, board):
        return board.get_pieces(self)
