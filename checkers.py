from enum import Enum


class Board:
    BOARD_SIZE = 8

    # 1 - kazdy z graczy ma  liste pionkow (typ, (koordy))
    # 2 - na boardzie stawiam se obiekty Piece w danym miejscu i essa

    def __init__(self):
        self.board = [[None for i in range(self.BOARD_SIZE)]
                      for j in range(self.BOARD_SIZE)]
        self.init_board()

    def move(self, player, from_yx, to_yx):
        # miki

        pass

    def is_legal_move(self, player, from_yx, to_yx):
        # miki

        # case: out of board bounds

        # case: piece cannot move like that

        # case: spot taken
        pass

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

    def __init__(self, board):
        self.board = board

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
