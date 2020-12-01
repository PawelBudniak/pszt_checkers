from enum import Enum


def average(x, y):
    return int((x + y) / 2)


def sgn(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


class Board:
    BOARD_SIZE = 8

    def __init__(self):
        self.board = [[None for i in range(self.BOARD_SIZE)]
                      for j in range(self.BOARD_SIZE)]
        self.init_board()
        self.debug = False

    def move(self, player, from_yx, to_yx, move_in_progress):
        # miki
        if not self.is_legal_move(player, from_yx, to_yx, move_in_progress):
            print("Error, wrong move")
            return
        from_piece = self.board[from_yx[0]][from_yx[1]]
        if from_piece.is_king:
            # captured piece coordinates
            x = -1
            y = -1
            # calculating the horizontal direction from->end to check for capturing/movement
            if from_yx[0] > to_yx[0] < 0:
                dy = -1
            else:
                dy = 1
            # calculating the vertical direction from->end to check for capturing/movement
            if from_yx[1] - to_yx[1] > 0:
                dx = -1
            else:
                dx = 1
            # count of seen objects with the opposite color
            # offset from the beginning coordinates
            t = dy
            c = dx
            # while we've not met the ending point:
            while from_yx[0] + t != to_yx[0] and from_yx[1] + c != to_yx[1]:
                # if we came across a piece:
                if self.board[from_yx[0] + t][from_yx[1] + c] is not None:
                    x = from_yx[1] + c
                    y = from_yx[0] + t
                    break
                t += dy
                c += dx
            if x != -1:
                self.board[y][x] = None
        elif not from_piece.is_king:
            if abs(to_yx[0] - from_yx[0]) == 2:
                self.board[average(to_yx[0], from_yx[0])][average(to_yx[1], from_yx[1])] = None
        self.board[to_yx[0]][to_yx[1]], self.board[from_yx[0]][from_yx[1]] = self.board[from_yx[0]][from_yx[1]], \
                                                                             self.board[to_yx[0]][to_yx[1]]
        if from_piece.is_white and to_yx[0] == 0 or (not from_piece.is_white) and to_yx[0] == self.BOARD_SIZE - 1:
            from_piece.is_king = True

    # check if the move is legal when regarding game's rules
    def is_legal_move(self, player, from_yx, to_yx, move_in_progress):
        # miki
        from_piece = self.board[from_yx[0]][from_yx[1]]
        # case: piece not destined for given player
        if not from_piece.is_white == player.is_white:
            return False
        # case: out of board bounds
        if from_piece is None:
            return False
        if to_yx[0] not in range(self.BOARD_SIZE) or to_yx[1] not in range(self.BOARD_SIZE):
            return False
        # case: piece cannot move like that because the x-travel distance must be equal to the y-travel distance
        if abs(to_yx[0] - from_yx[0]) != abs(to_yx[1] - from_yx[1]):
            return False
        # case: destination taken by another piece
        if self.board[to_yx[0]][to_yx[1]] is not None:
            return False
        if from_piece.is_king:
            # handle king behavior
            return self._is_legal_king_move(from_yx, to_yx, move_in_progress)
        else:
            return self._is_man_legal_move(from_yx, to_yx, move_in_progress)

    # underscore na początku metody dajesz to taka kownencja zeby pokazac ze metoda ma byc private (bardziej
    # protected chyba w sumie)
    def _is_legal_king_move(self, from_yx, to_yx, move_in_progress):
        from_piece = self.board[from_yx[0]][from_yx[1]]

        dy = sgn(to_yx[0] - from_yx[0])
        dx = sgn(to_yx[1] - from_yx[1])

        captured_pieces = 0
        # look for any pieces on the kings path
        # shift ranges by dx and dy so it goes from [start, stop) to (start, stop] (excludes start, includes stop)
        x_iter = iter(range(from_yx[1] + dx, to_yx[1] + dx, dx))
        for y in range(from_yx[0] + dy, to_yx[0] + dy, dy):
            x = next(x_iter)
            piece = self.board[y][x]
            if piece is not None:
                if piece.is_white == from_piece.is_white:
                    # collision with allied piece
                    return False
                else:
                    captured_pieces += 1
        if captured_pieces > 1:
            # only one capture allowed in yyyyyy small_move?
            return False

        return True

    def _is_man_legal_move(self, from_yx, to_yx, move_in_progress):
        from_piece = self.board[from_yx[0]][from_yx[1]]

        delta_y = to_yx[0] - from_yx[0]

        # if piece is white and not moving up the board or
        # it is black and not moving down the board, return false
        if abs(delta_y) == 1:
            if (from_piece.is_white and delta_y != -1 or
                    not from_piece.is_white and delta_y != 1):
                return False
        # handle if attempted capture which means absolute delta of y is 2
        elif abs(delta_y) == 2:
            if self.board[average(to_yx[0], from_yx[0])][average(to_yx[1], from_yx[1])] is None:
                return False
            if self.board[average(to_yx[0], from_yx[0])][average(to_yx[1], from_yx[1])].is_white == \
                    from_piece.is_white:
                return False
        # if the move is too long in range ( not moving by one step and not capturing )
        else:
            return False

        return True

    # no clue
    def available_moves(self, player, from_yx, move_in_progress):
        move_list = []
        for row in range(self.BOARD_SIZE):
            for el in range(self.BOARD_SIZE):
                if self.is_legal_move(player, from_yx, (row, el), move_in_progress):
                    move_list.append((row, el))
        print(move_list)
        return move_list

    def init_board(self):
        def fill_row(row, start, is_white):
            for column in range(start, self.BOARD_SIZE, 2):
                self.board[row][column] = Piece(row, column, is_white, False)

        # fill black
        fill_row(0, 1, is_white=False)
        fill_row(1, 0, is_white=False)
        fill_row(2, 1, is_white=False)

        # fill white
        fill_row(self.BOARD_SIZE - 1, 0, is_white=True)
        fill_row(self.BOARD_SIZE - 2, 1, is_white=True)
        fill_row(self.BOARD_SIZE - 3, 0, is_white=True)

    def get_king(self, player, yx):
        pass

    def display(self):

        def print_horizontal_lines():
            print("   ", end='')
            for _ in range(self.BOARD_SIZE):
                print("--- ", end='')

        # print column ids (letters)
        print("    ", end='')
        for i in range(self.BOARD_SIZE):
            col_id = chr(ord('A') + i) if self.debug is False else str(i)
            print(col_id + "   ", end='')
        print('')

        print_horizontal_lines()

        for y in range(self.BOARD_SIZE):
            print('')  # newline
            row_id = y + 1 if self.debug is False else y
            print(str(row_id) + ' ', end='')  # print row ids (numbers)
            for x in range(self.BOARD_SIZE):
                if self.board[y][x] is None:
                    print("|   ", end='')
                else:
                    print("|{:^3}".format(str(self.board[y][x])), end='')
            print("|")
            print_horizontal_lines()
        print('')  # newline


class Piece:

    def __init__(self, y, x, is_white, is_king=False):
        self.is_white = is_white
        self.is_king = is_king
        self.y = y
        self.x = x

    def __str__(self):
        if self.is_white:
            char = 'w'
        else:
            char = 'b'
        if self.is_king:
            char = char.upper()
        return char


class Player:

    def __init__(self, is_white):
        self.is_white = is_white

    def get_move(self):
        pass


class MinmaxAI(Player):

    def get_move(self):
        pass

    def minmax_score(self):
        pass


if __name__ == '__main__':
    brd = Board()
    brd.display()
