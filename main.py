# This is a sample Python script.
import checkers
from helper import Point
import minmax
from player import *
import game
from piece import *


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    minmax.clear_cache()
    # player2 = checkers.Player(is_white=True)
    # player1 =checkers.Player(is_white=False)
    player2 = minmax.MinmaxAI(is_white=True, nocache=True)
    player1 = minmax.MinmaxAI(is_white=False, opponent=player2, depth=7, nocache=True)
    player2.opponent = player1
    player2.depth = 1
    game = game.Game(player2, player1)
    game.play(show_display=True, cache_black_player=False, cache_white_player=False, testing=True)

    # board = checkers.Board()
    #
    # player2 = checkers.Player(is_white=True)
    # board.white_player = player2
    # board.board[1][0] = None
    # # board.board[2][1] = checkers.Piece(2, 1, False, is_queen=False)
    # board.board[2][1] = None
    # #board.board[3][2] = checkers.Piece(3, 2, False, is_queen=False)
    # board.board[5][4] = checkers.Piece(5, 4, True, is_queen=True)
    # #board.board[3][4] = checkers.Piece(3, 4, True, is_queen=False)
    # board.display()
    # print(str(board.move(board.white_player, Point(5, 4), Point(2, 1))))
    # board.display()
    # print(str(board.move(board.white_player, Point(4, 1), Point(3, 2) )))
    # board.display()
    # print(str(board.move(board.white_player, Point(3, 2), Point(4, 3) )))
    # board.display()


#  brd = checkers.Board()
#  brd.debug = True
#  brd.init_board()
# #  brd.board[2][1] = checkers.Piece(2, 1, False, is_king=False)
# #  brd.board[3][2] = checkers.Piece(3, 2, True, is_king=False)
# #  brd.board[5][4] = checkers.Piece(5, 4, True, is_king=False)
# #  brd.board[5][6] = checkers.Piece(5, 6, True, is_king=False)
# #  brd.board[5][2] = checkers.Piece(5, 2, True, is_king=False)
# #  brd.board[3][4] = checkers.Piece(3, 4, True, is_king=False)
# # brd.board[1][4] = checkers.Piece(1, 4, True, is_king=False)
# #  brd.board[3][6] = checkers.Piece(3, 6, True, is_king=False)


# print(Point(3,2))

# brd.display()

#     player2 = checkers.Player(is_white=True)
#     player1 = minmax.MinmaxAI(is_white=False, opponent=player2, depth=5)
#     brd.black_player = player1
#     brd.white_player = player2
#     print(brd.available_full_moves(player2))
#
#     # #brd.board[6][5] = None
# #     brd.count_pieces()
# #     print(f'scores = {brd.score}')
# #     #player2 = checkers.Player(is_white=True)
# #     player2 = minmax.MinmaxAI(is_white=True)
# #     player1 = minmax.MinmaxAI(is_white=False, opponent=player2, depth=8)
# #     player2.opponent = player1
# #     player2.depth = 5
# #
#     # brd.black_player = player1
#     # brd.white_player = player2
# #     #player2 = checkers.Player(is_white=False)
# #     running = True
# #     temp = False
#     while brd.white_won() is None and brd.is_draw() is False:
#         brd.display()
#         move = player1.get_move(brd)
#         while not brd.full_move(player1, move):
#             move = player1.get_move(brd)
#             brd.display()
#         # print ("------------------------")
#         # print(f'typ: {type(player1.cache)}')
#         # print(player1.cache)
#         player1.save_cache()
#         brd.display()
#         print(f'scores = {brd.score}')
#         move = player2.get_move(brd)
#         while not brd.full_move(player2, move):
#             move = player2.get_move(brd)
#             brd.display()
#
#     player1.save_cache()
# #
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
