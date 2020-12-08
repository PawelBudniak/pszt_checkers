import unittest

from checkers import Board
from minmax import MinmaxAI
from piece import Piece
from player import Player
import copy



class MyTestCase(unittest.TestCase):

        # def setUp(self):
        #     self.white_player = Player(is_white=False)
        #     self.minmax = MinmaxAI(is_white=False, depth = 5,)
        #     self.brd = Board(self.white_player, self.minmax)

        def test_minmax_board_state(self):
            self.white_player = Player(is_white=True)
            self.minmax = MinmaxAI(is_white=False, depth=5, opponent=self.white_player)
            self.brd = Board(self.white_player, self.minmax)

            self.brd.board[5][0] = Piece(5, 0, is_white=False, is_queen=False)
            self.brd.board[6][1] = Piece(6, 1, is_white=True, is_queen=False)
            self.brd.board[4][5] = Piece(4, 5, is_white=True, is_queen=True)
            self.brd.board[2][0] = Piece(2, 0, is_white=True, is_queen=False)

            board_key = self.brd.key(self.minmax)
            score_copy = list(self.brd.score)
            white_pieces_copy = copy.deepcopy(self.white_player.get_pieces(self.brd))
            black_pieces_copy = copy.deepcopy(self.minmax.get_pieces(self.brd))

            move = self.minmax.get_move(self.brd)

            self.assertEqual(board_key, self.brd.key(self.minmax),
                             msg='Minmax changes board state')
            self.assertCountEqual(score_copy, self.brd.score,
                                  msg='Minmax changes score state')
            white_pieces_after = self.white_player.get_pieces(self.brd)
            black_pieces_after = self.minmax.get_pieces(self.brd)
            self.assertListEqual(white_pieces_copy, white_pieces_after)
            self.assertListEqual(black_pieces_copy, black_pieces_after)


        def test_minmax_board_state2(self):
            self.white_player = Player(is_white=True)
            self.minmax = MinmaxAI(is_white=False, depth=3, opponent=self.white_player)
            self.brd = Board(self.white_player, self.minmax)

            self.brd.init_board()

            board_key = self.brd.key(self.minmax)
            score_copy = list(self.brd.score)
            white_pieces_copy = copy.deepcopy(self.white_player.get_pieces(self.brd))
            black_pieces_copy = copy.deepcopy(self.minmax.get_pieces(self.brd))

            move = self.minmax.get_move(self.brd)

            self.assertEqual(board_key, self.brd.key(self.minmax),
                             msg='Minmax changes board state')
            self.assertCountEqual(score_copy, self.brd.score,
                                  msg='Minmax changes score state')
            self.assertCountEqual(white_pieces_copy, self.white_player.get_pieces(self.brd))
            self.assertCountEqual(black_pieces_copy, self.minmax.get_pieces(self.brd))



if __name__ == '__main__':
    unittest.main()
