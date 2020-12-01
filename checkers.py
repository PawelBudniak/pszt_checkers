from enum import Enum
import copy

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
    PIECES_COUNT = 12

    def __init__(self):
        self.board = [[None for i in range(self.BOARD_SIZE)]
                      for j in range(self.BOARD_SIZE)]
        self.init_board()
        self.debug = False
        self.score = [self.PIECES_COUNT, self.PIECES_COUNT]

    def full_move(self, player, chosen_path):
        board = copy.deepcopy(self.board)
        print("Procesowana sciezka: " + str(chosen_path))
        processing = True
        move_from = (chosen_path.pop(0), chosen_path.pop(0))
        move_to = (chosen_path.pop(0), chosen_path.pop(0))

        should_capture = len(self.available_captures(player, move_from)) > 0

        while processing:
            x = self.score.copy()
            if not self.move(player, move_from, move_to):
                self.board = board
                return False
            if x == self.score and should_capture:
                self.board = board
                print("Player required to capture, wrong move")
                return False
            if x == self.score and chosen_path:
                print("Too many move choices, wrong move")
                self.board = board
                return False
            should_capture = False
            if not chosen_path:
                break
            move_from = move_to
            move_to = (chosen_path.pop(0), chosen_path.pop(0))

        return True

    def move(self, player, from_yx, to_yx):
        # miki
        if not self._is_within_constraints(player, from_yx, to_yx):
            print("Error, wrong move")
            return
        from_piece = self.board[from_yx[0]][from_yx[1]]
        if from_piece.is_king:
            move_analysis = self._king_possible_capture(from_yx, to_yx)
            if not move_analysis[0]:
                return False
            else:
                if move_analysis[1] is not None and move_analysis[2] == 1:
                    self.board[move_analysis[1][0]][move_analysis[1][1]] = None
                    if player.is_white:
                        self.score[0] -= 1
                    else:
                        self.score[1] -= 1
        elif not from_piece.is_king:
            if abs(to_yx[0] - from_yx[0]) == 2:
                self.board[average(to_yx[0], from_yx[0])][average(to_yx[1], from_yx[1])] = None
                if player.is_white:
                    self.score[0] -= 1
                else:
                    self.score[1] -= 1
        self.board[to_yx[0]][to_yx[1]], self.board[from_yx[0]][from_yx[1]] = self.board[from_yx[0]][from_yx[1]], \
                                                                             self.board[to_yx[0]][to_yx[1]]
        if from_piece.is_white and to_yx[0] == 0 or (not from_piece.is_white) and to_yx[0] == self.BOARD_SIZE - 1:
            from_piece.is_king = True
        return True  # successful action

    # check if this move is a capture
    def is_legal_capture(self, player, from_yx, to_yx):
        # miki
        captured_piece = None

        if self._is_within_constraints(player, from_yx, to_yx):
            from_piece = self.board[from_yx[0]][from_yx[1]]
            if from_piece.is_king:
                # handle king behavior
                return self._is_king_legal_capture(from_yx, to_yx)
            else:
                return self._is_man_legal_capture(from_yx, to_yx)
        return False, None

    # check if the move is legal when regarding game's rules
    def is_legal_move(self, player, from_yx, to_yx):
        # miki
        if self._is_within_constraints(player, from_yx, to_yx):
            from_piece = self.board[from_yx[0]][from_yx[1]]
            if from_piece.is_king:
                # handle king behavior
                return self._is_king_legal_move(from_yx, to_yx), None
            else:
                return self._is_man_legal_move(from_yx, to_yx), None
        return False, None

    def is_legal_action(self, player, from_yx, to_yx):
        # miki

        if self._is_within_constraints(player, from_yx, to_yx):
            from_piece = self.board[from_yx[0]][from_yx[1]]
            if from_piece.is_king:
                # handle king behavior
                return self._is_king_legal_action(from_yx, to_yx)
            else:
                return self._is_man_legal_action(from_yx, to_yx)
        return False

    # check basic game constraints
    def _is_within_constraints(self, player, from_yx, to_yx):

        if to_yx[0] not in range(self.BOARD_SIZE) or to_yx[1] not in range(self.BOARD_SIZE) or\
                from_yx[0] not in range(self.BOARD_SIZE) or from_yx[1] not in range(self.BOARD_SIZE):
            return False
        from_piece = self.board[from_yx[0]][from_yx[1]]
        # case: out of board bounds
        if from_piece is None:
            return False
        # case: piece not destined for given player
        if not from_piece.is_white == player.is_white:
            return False

        # case: piece cannot move like that because the x-travel distance must be equal to the y-travel distance
        if abs(to_yx[0] - from_yx[0]) != abs(to_yx[1] - from_yx[1]):
            return False
        # case: destination taken by another piece
        if self.board[to_yx[0]][to_yx[1]] is not None:
            return False
        return True

    # underscore na początku metody dajesz to taka kownencja zeby pokazac ze metoda ma byc private (bardziej
    # protected chyba w sumie)
    def _is_king_legal_action(self, from_yx, to_yx):
        result = self._king_possible_capture(from_yx, to_yx)
        if self._king_possible_capture(from_yx, to_yx)[0]:
            return True,
        return False

    def _is_king_legal_capture(self, from_yx, to_yx):
        result = self._king_possible_capture(from_yx, to_yx)
        if result[0] is True and result[1] is not None and result[2] == 1:
            return True, result[1]
        return False, None

    def _is_king_legal_move(self, from_yx, to_yx):
        result = self._king_possible_capture(from_yx, to_yx)
        if result[0] is True and result[1] is None and result[2] == 0:
            return True,
        return False

    # arg 0 tells the user, if the action is at all possible
    # arg 1 holds the captured piece - only, if it was captured
    # arg 2 hold the count of encountered pieces
    def _king_possible_capture(self, from_yx, to_yx):
        from_piece = self.board[from_yx[0]][from_yx[1]]

        dy = sgn(to_yx[0] - from_yx[0])
        dx = sgn(to_yx[1] - from_yx[1])

        is_action_possible = True
        captured_pieces = 0
        captured_piece = None  # only useful, if succesful capture

        # look for any pieces on the kings path
        # shift ranges by dx and dy so it goes from [start, stop) to (start, stop] (excludes start, includes stop)
        y_path = range(from_yx[0] + dy, to_yx[0] + dy, dy)
        x_path = range(from_yx[1] + dx, to_yx[1] + dx, dx)
        path = zip(y_path, x_path)
        for y, x in path:
            piece = self.board[y][x]
            if piece is not None:
                if piece.is_white == from_piece.is_white:
                    # collision with allied piece
                    is_action_possible = False
                    break
                else:
                    captured_pieces += 1
                    captured_piece = (y, x)
        if captured_pieces not in (0, 1):
            is_action_possible = False
        return is_action_possible, captured_piece, captured_pieces

    def _is_man_legal_action(self, from_yx, to_yx):

        if self._is_man_legal_capture(from_yx, to_yx) or self._is_man_legal_move(from_yx, to_yx):
            return True
        else:
            return False

    def _is_man_legal_capture(self, from_yx, to_yx):

        from_piece = self.board[from_yx[0]][from_yx[1]]
        delta_y = to_yx[0] - from_yx[0]

        if abs(delta_y) == 2:
            if self.board[average(to_yx[0], from_yx[0])][average(to_yx[1], from_yx[1])] is None:
                return False, None
            if self.board[average(to_yx[0], from_yx[0])][average(to_yx[1], from_yx[1])].is_white == \
                    from_piece.is_white:
                return False, None
            # if the move is too long in range ( not moving by one step and not capturing )
            else:
                return True, (average(to_yx[0], from_yx[0]), average(to_yx[1], from_yx[1]))
        return False, None

    # trying to move a piece without capturing
    def _is_man_legal_move(self, from_yx, to_yx):

        from_piece = self.board[from_yx[0]][from_yx[1]]
        delta_y = to_yx[0] - from_yx[0]

        if abs(delta_y) == 1:
            if from_piece.is_white and delta_y != -1 or not from_piece.is_white and delta_y != 1:
                return False
            else:
                return True
        return False

    # list all available moves
    def available_moves(self, player, from_yx):
        move_list = []
        for row in range(self.BOARD_SIZE):
            for el in range(self.BOARD_SIZE):
                if self.is_legal_move(player, from_yx, (row, el))[0]:
                    move_list.append((row, el))
        print(move_list)
        return move_list

    # list all available captures
    def available_captures(self, player, from_yx):
        move_list = []
        for row in range(self.BOARD_SIZE):
            for el in range(self.BOARD_SIZE):
                if self.is_legal_capture(player, from_yx, (row, el))[0]:
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

    def get_move(self, board):
        x = input("Is white = " + str(self.is_white) + "\nEnter coordinates: <from_y> <from_x> <to_y> <to_x>").split()
        result = []
        for i in range(len(x)):
            result.append(int(x[i]))
        return result

class MinmaxAI(Player):

    def get_move(self):
        pass

    def minmax_score(self):
        pass


if __name__ == '__main__':
    brd = Board()
    brd.display()
