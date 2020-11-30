from enum import Enum


def average(x, y):
    return int((x + y) / 2)


class Board:
    BOARD_SIZE = 8

    # 1 - kazdy z graczy ma  liste pionkow (typ, (koordy))
    # 2 - na boardzie stawiam se obiekty Piece w danym miejscu i essa

    def __init__(self):
        self.board = [[None for i in range(self.BOARD_SIZE)]
                      for j in range(self.BOARD_SIZE)]
        self.init_board()

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
        if from_piece.is_white and to_yx[0] == 0 or (not from_piece.is_white) and to_yx[0] == self.BOARD_SIZE-1:
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
            count = 0
            # offset from the beginning coordinates
            t = dy
            c = dx
            # while we've not met the ending point:
            while from_yx[0] + t != to_yx[0] and from_yx[1] + c != to_yx[1]:
                # if we came across a piece:
                if self.board[from_yx[0] + t][from_yx[1] + c] is not None:
                    # if it is the same color as the piece we are moving with:
                    if self.board[from_yx[0] + t][from_yx[1] + c].is_white == from_piece.is_white and t != 0:
                        return False
                    # else, it must be the enemies piece
                    else:
                        count += 1
                if count > 1:
                    return False
                t += dy
                c += dx
        else:
            # handle standard move: if diff = 1 and white, move only up else if black, only down
            if abs(to_yx[0] - from_yx[0]) == 1:
                # if piece is white and not moving up the board or
                # it is black and not moving down the board, return false
                if (from_piece.is_white and to_yx[0] - from_yx[0] != -1) or \
                        ((not from_piece.is_white) and to_yx[0] - from_yx[0] != 1):
                    return False
            # handle if attempted capture which means absolute delta of y is 2
            elif abs(to_yx[0] - from_yx[0]) == 2:
                if not move_in_progress:
                    # if black tries to go up or white tries to go down
                    # but now, the absolute delta of y is ought to be 2
                    if (from_piece.is_white and to_yx[0] - from_yx[0] != -2) or \
                            ((not from_piece.is_white) and to_yx[0] - from_yx[0] != 2):
                        return False
                if self.board[average(to_yx[0], from_yx[0])][average(to_yx[1], from_yx[1])] is None:
                    return False
                if self.board[average(to_yx[0], from_yx[0])][average(to_yx[1], from_yx[1])].is_white == \
                        from_piece.is_white:
                    return False
            # if the move is too long in range ( not moving by one step and not capturing )
            else:
                return False
        return True

    def available_moves(self, piece):
        # miki
        pass

    def init_board(self):
        def fill_row(row, start, is_white):
            for column in range(start, self.BOARD_SIZE, 2):
                self.board[row][column] = Piece(is_white, False, row, column)

        # fill black
        fill_row(0, 1, is_white=False)
        fill_row(1, 0, is_white=False)
        fill_row(2, 1, is_white=False)

        # fill white
        fill_row(self.BOARD_SIZE - 1, 0, is_white=True)
        fill_row(self.BOARD_SIZE - 2, 1, is_white=True)
        fill_row(self.BOARD_SIZE - 3, 0, is_white=True)
        self.board[2][1] = Piece(False, False, 2, 1)
        self.board[3][2] = Piece(True, False, 3, 2)
        #self.board[4][3] = Piece(True, False, 4, 3)
        self.board[5][4] = None

    def get_king(self, player, yx):
        pass

    # def display(self):
    #     for row in self.board:
    #         for cell in row:
    #             if cell is None:
    #                 print('x', end = '')
    #             else:
    #                 print(cell)
    #         print('')

    def display(self):

        def print_horizontal_lines():
            print("   ", end='')
            for _ in range(self.BOARD_SIZE):
                print("--- ", end='')

        # print column ids (letters)
        print("    ", end='')
        for i in range(self.BOARD_SIZE):
            print(chr(ord('A') + i) + "   ", end='')
        print('')

        print_horizontal_lines()

        for y in range(self.BOARD_SIZE):
            print('')  # newline
            print(str(y + 1) + ' ', end='')  # print row ids (numbers)
            for x in range(self.BOARD_SIZE):
                if self.board[y][x] is None:
                    print("|   ", end='')
                else:
                    print("|{:^3}".format(str(self.board[y][x])), end='')
            print("|")
            print_horizontal_lines()
        print('')  # newline


class Piece:

    def __init__(self, is_white, is_king, y, x):
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
