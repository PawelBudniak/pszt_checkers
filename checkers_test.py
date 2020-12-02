import unittest
from checkers import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)
    def test_white_won(self):
        brd = Board()
        brd.board[4][1] = Piece(4,1, is_white=True, is_king=False)
        self.assertTrue(brd.white_won())

    def test_can_move(self):
        brd = Board()
        brd.board[5][0] = Piece(5, 0, is_white=True, is_king=False)
        brd.board[4][1] = Piece(4, 1, is_white=False, is_king=False)
        brd.white_player = Player(is_white=True)
        brd.black_player = Player(is_white=False)
        self.assertFalse(brd._can_move(brd.white_player))


if __name__ == '__main__':
    unittest.main()
