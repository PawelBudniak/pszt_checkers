import unittest
from checkers import Board
from piece import *
from player import Player
from helper import *
import copy

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.white_player = Player(is_white=True)
        self.black_player = Player(is_white=False)
        self.brd = Board(self.white_player, self.black_player)

    def test_try_move_man(self):
        self.brd.board[5][2] = Piece(5, 2, is_white=True, is_queen=False)
        piece = self.brd.board[5][2]
        av_moves = piece.available_moves(self.white_player, self.brd.board)
        av_captures = piece.available_moves(self.white_player, self.brd.board, must_capture=True)
        self.brd.board[4][1] = Piece(4, 1, is_white=False, is_queen=False)
        self.assertEqual([Point(4,1), Point(4,3)], av_moves)
        self.assertEqual([], av_captures)
        self.assertTrue(piece.try_move(Point(3,0), self.white_player, self.brd.board)[0] == Move.Capture)
        self.assertFalse(piece.try_move(Point(6,3), self.white_player, self.brd.board)[0] == Move.Traverse)
        self.assertFalse(piece.try_move(Point(3,4), self.white_player, self.brd.board)[0] != Move.Unavailable)

    def test_try_move_queen(self):
        self.brd.board[5][4] = Piece(5, 4, is_white=True, is_queen=True)
        piece = self.brd.board[5][4]
        self.brd.board[3][2] = Piece(3, 2, is_white=False, is_queen=True)
        self.brd.board[3][6] = Piece(3, 6, is_white=False, is_queen=False)
        av_captures = piece.available_moves(self.white_player, self.brd.board, must_capture=True)
        av_moves = piece.available_moves(self.white_player, self.brd.board)
        print(str(av_captures) + "\n" + str(av_moves))
        self.assertEqual([Point(4,3), Point(2,1), Point(1,0), Point(4,5), Point(2,7), Point(6,3), Point(7,2), Point(6,5), Point(7,6)], av_moves)
        self.assertEqual([Point(2,1), Point(1,0), Point(2,7)], av_captures)

    def test_man_available_moves(self):
        self.brd.board[3][2] = Piece(3, 2, is_white=True, is_queen=False)
        piece = self.brd.board[3][2]
        self.brd.board[2][1] = Piece(2, 1, is_white=False, is_queen=False)
        self.brd.board[1][0] = Piece(1, 0, is_white=False, is_queen=False)
        self.brd.board[4][3] = Piece(4, 3, is_white=False, is_queen=False)
        self.assertEqual([Point(5,4)], piece.available_moves(self.white_player, self.brd.board, must_capture=True))
        self.assertEqual([Point(2,3)], piece.available_moves(self.white_player, self.brd.board, must_capture=False))

    def test_queen_available_moves(self):
        self.brd.board[3][4] = Piece(3, 4, is_white=True, is_queen=True)
        piece = self.brd.board[3][4]
        self.brd.board[5][6] = Piece(5, 6, is_white=False)
        self.brd.board[2][3] = Piece(2, 3, is_white=True)
        self.brd.board[1][2] = Piece(1, 2, is_white=False)
        self.brd.board[1][6] = Piece(1, 6, is_white=False)
        self.brd.board[0][7] = Piece(0, 7, is_white=False)
        self.brd.display()
        self.assertEqual([Point(6,7)], piece.available_moves(self.white_player, self.brd.board, must_capture=True))
        self.assertEqual([Point(2,5), Point(4,3), Point(5,2), Point(6,1), Point(7,0), Point(4,5)], piece.available_moves(self.white_player, self.brd.board, must_capture=False))

    def test_get_man_path(self):
        self.brd.board[2][7] = Piece(2, 7, is_white=True)
        piece = self.brd.board[2][7]
        self.assertEqual([Point(1,6), Point(0,5), Point(3,6), Point(4,5)], piece.get_man_path())

    def test_get_queen_path(self):
        self.brd.board[4][5] = Piece(4, 5, is_white=True, is_queen=True)
        piece = self.brd.board[4][5]
        self.assertEqual(set([Point(5,6), Point(6,7), Point(5,4), Point(6,3), Point(7,2), Point(3,6), Point(2,7), Point(3,4), Point(2,3), Point(1,2), Point(0,1)]), set(piece.get_queen_path()))


if __name__ == '__main__':
    unittest.main()
