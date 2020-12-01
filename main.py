# This is a sample Python script.
import checkers
from helper import Point
import minmax


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    brd = checkers.Board()
    brd.debug = True
    brd.board[3][2] = checkers.Piece(3, 2, True, is_king=False)
    brd.board[2][1] = checkers.Piece(2, 1, False, is_king=False)
    brd.board[3][2] = checkers.Piece(3, 2, True, is_king=False)
    brd.board[5][4] = checkers.Piece(5, 4, True, is_king=False)
    brd.board[5][6] = checkers.Piece(5, 6, True, is_king=False)
    brd.board[5][2] = checkers.Piece(5, 2, True, is_king=False)
    brd.board[3][4] = checkers.Piece(3, 4, True, is_king=False)
    brd.board[1][4] = checkers.Piece(1, 4, True, is_king=False)










    player1 = checkers.Player(is_white=True)
    player2 = checkers.Player(is_white=False)

# print(Point(3,2))

    brd.display()

    print(brd.capture_trees(player2, Point(2,1)))
    print(brd.available_full_moves(player2))
    #print(brd._capture_possibilities(player2, Point(6, 5), list(), [Point(4, 3)]))

    # #brd.board[6][5] = None
# player1 = checkers.Player(is_white=True)
# player2 = checkers.Player(is_white=False)
# running = True
# temp = False
# while brd.score[0] > 0 and brd.score[1] > 0:
#     brd.display()
#     move = player1.get_move(brd)
#     while not brd.full_move(player1, move):
#         move = player1.get_move(brd)
#         brd.display()
#     brd.display()
#     move = player2.get_move(brd)
#     while not brd.full_move(player2, move):
#         move = player2.get_move(brd)
#         brd.display()
#
# print("woohoo someone won")
#     # player 2
# brd.board[2][1] = checkers.Piece(2, 1, False, is_king=True)
# brd.board[3][2] = checkers.Piece(3, 2, True, is_king=False)
# brd.board[4][3] = checkers.Piece(True, False, 4, 3)
# brd.board[5][4] = None


# print("Available moves:")
# brd.available_moves(player1, (2, 3), False)
# print("Available captures:")
# brd.available_captures(player1, (2, 3), False)
# brd.move(player1, (2, 1), (5, 4))
# brd.display()


# brd.move(player, (2, 1), (4, 3), False)
# brd.display()
# print(brd.is_legal_move((2, 1), (5, 4), False))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
