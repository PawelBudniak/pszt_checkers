import unittest
from checkers import *

class MyTestCase(unittest.TestCase):
    def test_white_won(self):
        brd = Board()
        brd.board[4][1] = Piece(4, 1, is_white=True, is_king=False)
        self.assertTrue(brd.white_won())

    def test_can_move(self):
        brd = Board()
        brd.board[5][0] = Piece(5, 0, is_white=True, is_king=False)
        brd.board[4][1] = Piece(4, 1, is_white=False, is_king=False)
        brd.board[3][2] = Piece(3, 2, is_white=False, is_king=False)
        brd.white_player = Player(is_white=True)
        brd.black_player = Player(is_white=False)
        brd.count_pieces()
        self.assertFalse(brd._can_move(brd.white_player))

    def test_should_catpture(self):
        brd = Board()
        brd.white_player = Player(is_white=True)
        brd.black_player = Player(is_white=False)
        brd.board[5][0] = Piece(5, 0, is_white=True, is_king=False)
        brd.board[4][1] = Piece(4, 1, is_white=False, is_king=False)
        brd.board[3][4] = Piece(5, 2, is_white=False, is_king=False)
        brd.board[6][4] = Piece(5, 0, is_white=True, is_king=False)
        self.assertTrue(brd._should_capture(brd.white_player))
        self.assertFalse(brd._should_capture(brd.black_player))

    def test_is_draw(self):
        brd = Board()
        brd.white_player = Player(is_white=True)
        brd.black_player = Player(is_white=False)
        brd.board[5][0] = Piece(5, 0, is_white=True, is_king=True)
        brd.board[3][0] = Piece(3, 0, is_white=False, is_king=True)
        for i in range(15):
            if i % 2 == 0:
                brd.full_move(brd.white_player, [Point(5, 0), Point(6, 1)])
                brd.full_move(brd.black_player, [Point(3,0), Point(2, 1)])
            else:
                brd.full_move(brd.white_player, [Point(6, 1), Point(5, 0)])
                brd.full_move(brd.black_player, [Point(2, 1), Point(3, 0)])
        self.assertTrue(brd.is_draw())
    def test_available_full_moves(self):
        brd = Board()
        white = Player(is_white=True)
        brd.white_player = white
        brd.black_player = Player(is_white=False)
        brd.board[5][0] = Piece(5, 0, is_white=True, is_king=False)
        brd.board[6][1] = Piece(4, 1, is_white=False, is_king=False)
        correct_moves = [[Point(5,0), Point(7,2)]]
        #self.assertEqual(correct_moves, brd.available_full_moves(white))
        self.assertEqual(set(map(tuple,correct_moves)), set(map(tuple,brd.available_full_moves(white))))

    def test_avaialble_moves(self):
        brd = Board()
        white = Player(is_white=True)
        brd.white_player = white
        brd.board[5][5] = Piece(5, 5, is_white=True, is_king=False)
        correct_moves = [Point(4, 6), Point(4, 4)]
        self.assertEqual(set(correct_moves), set(brd.available_moves(white, Point(5,5))))

    def test_available_full_moves_no_capture(self):
        brd = Board()
        white = Player(is_white=True)
        brd.white_player = white
        brd.board[5][5] = Piece(5, 5, is_white=True, is_king=False)
        correct_moves = [[Point(5,5), Point(4,6)], [Point(5,5), Point(4,4)]]
        self.assertEqual(set(map(tuple,correct_moves)), set(map(tuple,brd.available_full_moves(white))))



if __name__ == '__main__':
    unittest.main()
