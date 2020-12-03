from checkers import *
from helper import *


class Piece:

    BOARD_SIZE = 8

    def __init__(self, y, x, is_white, is_queen=False):
        self.is_white = is_white
        self.is_queen = is_queen
        self.y = y
        self.x = x

    def __str__(self):
        if self.is_white:
            char = 'w'
        else:
            char = 'b'
        if self.is_queen:
            char = char.upper()
        return char

    def try_move(self, to, current_player, board):
        """
        :param
        board: board on which the piece is positioned
        to: coordinates of destined move
        :return
        possible_action:
            True - possible capture
            False - possible move
            None - unavailable action
        captured_piece: coordinates of a captured piece
        """

        possible_action = None
        captured_piece = None

        if not self.check_constraints(to, current_player, board):
            return possible_action, captured_piece

        if self.is_queen:

            # look for any pieces on the kings path
            # shift ranges by dx and dy so it goes from [start, stop) to (start, stop] (excludes start, includes stop)
            path = get_linear_path(Point(self.y, self.x), Point(to.y, to.x))

            captured_pieces = 0

            for y, x in path:

                piece = board[y][x]

                if piece is not None:

                    if piece.is_white == self.is_white:
                        # collision with allied piece
                        possible_action = False
                        break

                    else:
                        # came over opponents piece
                        captured_pieces += 1
                        captured_piece = (y, x)
                        possible_action = True

            # if came over more than 1 opponent, then the move is not a viable option
            if captured_pieces not in (0, 1):
                possible_action = None

        elif not self.is_queen:

            if abs(to.y - self.y) == 1:

                # if piece is moving in the right direction
                if current_player.is_white and to.y > self.y or (not current_player.is_white) and to.y < self.y:
                    possible_action = False

            elif abs(to.y - self.y) == 2:
                # if piece in between starting and ending point is of opposite color
                if board[average(to.y, self.y)][average(to.x, self.x)].is_white is not self.is_white:
                    possible_action = True
                    captured_piece = board[average(to.y, self.y)][average(to.x, self.x)]

        return possible_action, captured_piece

    def check_constraints(self,  to, current_player, board):

        # case: destined coordinates out of board bounds
        if to.y not in range(self.BOARD_SIZE) or to.x not in range(self.BOARD_SIZE) or \
                self.y not in range(self.BOARD_SIZE) or self.x not in range(self.BOARD_SIZE):
            return False

        # case: piece not destined for given player
        if not self.is_white == current_player.is_white:
            return False

        # case: piece cannot move like that because the x-travel distance must be equal to the y-travel distance
        if abs(to.y - self.y) != abs(to.x - self.x):
            return False

        # case: destination taken by another piece
        if board[to.y][to.x] is not None:
            return False
        return True

    def available_moves(self, current_player, board, must_capture=False):

        if self.is_queen:
            path = self.get_queen_path()
        else:
            path = self.get_man_path()

        for el in path:
            possible_capture, captured_piece = self.try_move(el, current_player, board)
            if possible_capture is None or must_capture is True and possible_capture is not True:
                path.remove(el)

        return path

    def get_queen_path(self):

        path = []

        import itertools
        directions = itertools.product((-1, 1), repeat=2)

        for dy, dx in directions:
            y, x = self.y, self.x

            while 0 <= y < self.BOARD_SIZE and 0 <= x < self.BOARD_SIZE:
                if not (y, x) == (self.y, self.x):
                    path.append(Point(y, x))
                y += dy
                x += dx

        return path

    def get_man_path(self):

        path = []

        import itertools
        directions = itertools.product((-1, 1), repeat=2)

        for dy, dx in directions:
            for i in (1, 2):
                y, x = self.y + i*dy, self.x + i*dx
                if 0 <= y and 0 <= x < self.BOARD_SIZE:
                    path.append(Point(y, x))

        return path

    def __repr__(self):
        return self.__str__()
