import unittest
from checkers import Board
from piece import Piece
from player import Player
from helper import *
import copy


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.white_player = Player(is_white=True)
        self.black_player = Player(is_white=False)
        self.brd = Board(self.white_player, self.black_player)

    def test_white_won(self):
        self.brd.board[4][1] = Piece(4, 1, is_white=True, is_queen=False)
        self.assertTrue(self.brd.white_won())

    def test_can_move(self):
        self.brd.board[5][0] = Piece(5, 0, is_white=True, is_queen=False)
        self.brd.board[4][1] = Piece(4, 1, is_white=False, is_queen=False)
        self.brd.board[3][2] = Piece(3, 2, is_white=False, is_queen=False)
        self.brd.white_player = Player(is_white=True)
        self.brd.black_player = Player(is_white=False)
        self.brd.display()
        self.brd.count_pieces()
        print(str(self.brd.available_moves(self.brd.white_player, capturing=None)))
        self.assertFalse(self.brd._can_move(self.brd.white_player))

    def test_should_catpture(self):
        self.brd.board[5][0] = Piece(5, 0, is_white=True, is_queen=False)
        self.brd.board[4][1] = Piece(4, 1, is_white=False, is_queen=False)
        self.brd.board[3][4] = Piece(5, 2, is_white=False, is_queen=False)
        self.brd.board[6][4] = Piece(5, 0, is_white=True, is_queen=False)
        self.assertTrue(self.brd._should_capture(self.brd.white_player))
        self.assertFalse(self.brd._should_capture(self.brd.black_player))

    def test_is_draw(self):
        self.brd.board[5][0] = Piece(5, 0, is_white=True, is_queen=True)
        self.brd.board[3][0] = Piece(3, 0, is_white=False, is_queen=True)
        for i in range(15):
            if i % 2 == 0:
                self.brd.full_move(self.brd.white_player, [Point(5, 0), Point(6, 1)])
                self.brd.full_move(self.brd.black_player, [Point(3, 0), Point(2, 1)])
            else:
                self.brd.full_move(self.brd.white_player, [Point(6, 1), Point(5, 0)])
                self.brd.full_move(self.brd.black_player, [Point(2, 1), Point(3, 0)])
        self.assertTrue(self.brd.is_draw())

    def lists_of_lists_equal(self, first, second):
        self.assertEqual(set(map(tuple, first)), set(map(tuple, second)))

    def test_available_full_moves_capture(self):
        self.brd.board[5][0] = Piece(5, 0, is_white=True, is_queen=False)
        self.brd.board[6][1] = Piece(6, 1, is_white=False, is_queen=False)
        correct_moves = [[Point(5, 0), Point(7, 2)]]
        self.assertCountEqual(correct_moves, self.brd.available_full_moves(self.white_player))

    def test_available_full_moves_state(self):
        self.brd.board[5][0] = Piece(5, 0, is_white=True, is_queen=False)
        self.brd.board[6][1] = Piece(6, 1, is_white=False, is_queen=False)
        board_key = self.brd.key(self.white_player)
        score_copy = copy.copy(self.brd.score)
        moves = self.brd.available_full_moves(self.white_player)

        self.assertEqual(board_key, self.brd.key(self.white_player),
                         msg='Board.full_available_moves() changes board state')
        self.assertCountEqual(score_copy, self.brd.score,
                         msg='Board.full_available_moves() changes score state')


    def test_avaiable_moves(self):
        self.brd.board[5][5] = Piece(5, 5, is_white=True, is_queen=False)
        correct_moves = [Point(4, 6), Point(4, 4)]
        self.assertEqual(set(correct_moves), set(self.brd.board[5][5].available_moves(self.white_player, self.brd.board)))

    def test_available_full_moves_no_capture(self):
        self.brd.board[6][1] = Piece(6, 1, is_white=True, is_queen=False)
        correct_moves = [[Point(6, 1), Point(5, 0)], [Point(6, 1), Point(5, 2)]]
        available_moves = self.brd.available_full_moves(self.white_player)
        print(str(available_moves))
        #self.lists_of_lists_equal(correct_moves, self.brd.available_full_moves(self.white_player))
        self.assertCountEqual(correct_moves, self.brd.available_full_moves(self.white_player))

    def test_available_full_moves_queen(self):
        self.brd.board[5][0] = Piece(5, 0, is_white=False, is_queen=False)
        self.brd.board[6][1] = Piece(6, 1, is_white=True, is_queen=False)
        self.brd.board[4][5] = Piece(4, 5, is_white=True, is_queen=True)
        moves = self.brd.available_full_moves(self.black_player)
        board_key = self.brd.key(self.black_player)
        score_copy = copy.copy(self.brd.score)



        self.assertIn([Point(5, 0), Point(7, 2)], moves)
        self.assertIn([Point(5, 0), Point(7, 2), Point(3, 6)], moves)
        self.assertIn([Point(5, 0), Point(7, 2), Point(2, 7)], moves)
        self.assertNotIn([Point(5, 0), Point(7, 2), Point(4, 5)], moves)
        self.assertEqual(board_key, self.brd.key(self.black_player),
                         msg='Board.full_available_moves() changes board state')
        self.assertCountEqual(score_copy, self.brd.score,
                              msg='Board.full_available_moves() changes score state')

    def test_count_pieces(self):
        self.brd.board[5][0] = Piece(5, 0, is_white=True, is_queen=False)
        self.brd.board[5][2] = Piece(5, 2, is_white=False, is_queen=False)
        self.brd.board[5][4] = Piece(5, 4, is_white=False, is_queen=False)
        self.brd.board[5][6] = Piece(5, 6, is_white=True, is_queen=False)
        self.brd.board[1][0] = Piece(1, 0, is_white=False, is_queen=False)
        self.brd.board[1][2] = Piece(1, 2, is_white=False, is_queen=False)
        self.brd.board[1][4] = Piece(1, 4, is_white=True, is_queen=False)
        self.brd.board[1][6] = Piece(1, 6, is_white=False, is_queen=False)
        self.brd.count_pieces()
        self.assertEqual([3, 5], self.brd.score)


    def test_full_move_man(self):
        self.brd.board[5][0] = Piece(5, 0, is_white=True, is_queen=False)
        self.brd.board[4][1] = Piece(5, 2, is_white=False, is_queen=False)
        self.brd.board[2][3] = Piece(5, 4, is_white=False, is_queen=False)
        self.brd.board[2][5] = Piece(5, 6, is_white=False, is_queen=False)
        self.assertTrue(self.brd.full_move(self.brd.white_player, [Point(5,0), Point(3, 2), Point(1,4), Point(3, 6)])[0])

    def test_full_move_queen(self):
        self.brd.board[7][0] = Piece(7, 0, is_white=True, is_queen=True)
        self.brd.board[5][2] = Piece(5, 2, is_white=False, is_queen=False) # to 4, 3
        self.brd.board[5][4] = Piece(5, 4, is_white=False, is_queen=False) # to 6, 5
        self.brd.board[3][2] = Piece(3, 2, is_white=False, is_queen=False) # to 2, 1
        self.brd.board[1][2] = Piece(1, 2, is_white=False, is_queen=False) # to 0, 3
        self.assertTrue(
            self.brd.full_move(self.white_player, [Point(7, 0), Point(4, 3), Point(6, 5), Point(2, 1), Point(0, 3)])[0])
        self.brd.board[1][0] = Piece(1, 0, is_white=True, is_queen=True)
        self.brd.board[5][4] = Piece(5, 2, is_white=False, is_queen=False)  # to 4, 3
        self.brd.board[3][2] = Piece(3, 2, is_white=False, is_queen=False)  # to 2, 1
        self.assertFalse(self.brd.full_move(self.white_player, [Point(1,0), Point(6,5)])[0])

    # TODO:
    def test_undo_capture(self):
        self.brd.board[7][0] = Piece(7, 0, is_white=True, is_queen=True)
        self.brd.board[5][2] = Piece(5, 2, is_white=False, is_queen=False)  # to 4, 3
        self.brd.board[5][4] = Piece(5, 4, is_white=False, is_queen=False)  # to 6, 5
        self.brd.board[3][2] = Piece(3, 2, is_white=False, is_queen=False)  # to 2, 1
        self.brd.board[1][2] = Piece(1, 2, is_white=False, is_queen=False)  # to 0, 3
        path = [Point(7, 0), Point(4, 3), Point(6, 5), Point(2, 1), Point(0, 3)]
        captured = self.brd.full_move(self.white_player, path)[1]


if __name__ == '__main__':
    unittest.main()
