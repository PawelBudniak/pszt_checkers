from enum import Enum
import copy

import minmax
from player import *
from piece import Piece, Move
from helper import *


class Board:
    BOARD_SIZE = 8
    PIECES_COUNT = 12

    def __init__(self, white_player=None, black_player=None):
        self.board = [[None for i in range(self.BOARD_SIZE)]
                      for j in range(self.BOARD_SIZE)]
        # self.init_board()
        self.debug = True
        self.score = [self.PIECES_COUNT, self.PIECES_COUNT]
        self.white_queen_moves = 0
        self.black_queen_moves = 0
        self.white_player = white_player
        self.black_player = black_player

    def set(self, other):
        self.board = other.board
        self.white_queen_moves = other.white_queen_moves
        self.black_queen_moves = other.white_queen_moves
        self.score = other.score

    def is_draw(self):
        return self.white_queen_moves >= 15 and self.black_queen_moves >= 15

    def white_won(self):
        # self.count_pieces()
        if self.score[1] == 0 or not self._can_move(self.black_player):
            return True
        elif self.score[0] == 0 or not self._can_move(self.white_player):
            return False
        else:
            return None

    def count_pieces(self):
        self.score = [0, 0]
        for y, x in BoardHelper.possible_tiles:
            piece = self.board[y][x]
            if piece is not None and piece.is_white:
                self.score[0] += 1
            elif piece is not None and not piece.is_white:
                self.score[1] += 1

    def full_move(self, player, chosen_path):
        if not chosen_path:
            return False, None

        if chosen_path[0] == "quit":
            print("Quiting...")
            exit(0)

        if not isinstance(player, minmax.MinmaxAI):
            if self.try_full_move(player, chosen_path) is False:
                return False, None

        begin_score = copy.deepcopy(self.score)
        move_from = chosen_path[0]
        captured_pieces = []

        for move_to in chosen_path[1:]:

            result, captured_piece = self.move(player, move_from, move_to)
            if not result:
                return False, captured_pieces
            move_from = move_to
            if captured_piece is not None:
                captured_pieces.append(captured_piece)

        if self.score == begin_score and self.board[move_to.y][move_to.x].is_queen:
            if self.board[move_to.y][move_to.x].is_white:
                self.white_queen_moves += 1
            else:
                self.black_queen_moves += 1
        return True, captured_pieces

    def try_full_move(self, player, chosen_path):
        if not chosen_path:
            return False

        should_capture = self._should_capture(player)
        # print(str(should_capture))
        start_point = chosen_path[0]

        begin_state = copy.deepcopy(self)

        for point in chosen_path[1:]:
            result = self.try_move(player, start_point, point)
            # print(str(result))

            # if the piece should capture but it doesnt
            if len(chosen_path) == 2 and should_capture and result is False:
                # print("1. " + str(start_point) + "2. " + str(point))
                self.set(begin_state)
                return False

            # if the piece is trying to traverse when moving more than one time
            if len(chosen_path) != 2 and result is False:
                self.set(begin_state)
                return False

            # if the piece is not capturing when path is longer than 2
            if result is None:
                self.set(begin_state)
                return False
            self.move(player, start_point, point)
            start_point = point
        self.set(begin_state)
        return True

    def _should_capture(self, player):
        for piece in self.get_pieces(player):
            if piece.available_moves(player, self.board, must_capture=True):
                return True
        return False

    def _can_move(self, player):
        for piece in self.get_pieces(player):
            if piece.available_moves(player, self.board):
                return True
        return False

    # TODO test
    def move(self, player, start, to):

        from_piece = self.board[start.y][start.x]
        available_move, captured_piece = from_piece.try_move(to, player, self.board)

        if available_move != Move.Unavailable:
            self._execute_move(available_move, player, start, to, captured_piece)
            return True, captured_piece  # successful action

    def try_move(self, player, start, to):
        from_piece = self.board[start.y][start.x]
        if not from_piece:
            return None
        available_move, captured_piece = from_piece.try_move(to, player, self.board)
        if available_move == Move.Unavailable:
            return None
        if available_move == Move.Traverse:
            return False
        return True

    def _execute_move(self, available_move, player, start, to, captured_piece):
        self.board[to.y][to.x] = self.board[start.y][start.x]
        self.board[start.y][start.x] = None
        piece = self.board[to.y][to.x]
        piece.y = to.y
        piece.x = to.x
        if captured_piece:
            self.board[captured_piece.y][captured_piece.x] = None
        self._update_data(available_move, player)
        self._try_king(player, to)
        if available_move == Move.Capture:
            if player.is_white:
                self.score[1] -= 1
            else:
                self.score[0] -= 1

    def _update_data(self, available_move, player):

        if available_move == Move.Capture:
            if player.is_white:
                self.white_queen_moves = 0
            else:
                self.black_queen_moves = 0
            # self.count_pieces()

    def available_moves(self, player, capturing):
        moves = []
        for piece in self.get_pieces(player):
            piece_moves = piece.available_moves(player, self.board, capturing)
            moves.append(piece_moves)
        moves.sort(key=len, reverse=True)
        return moves

    # TODO redo this shit
    def available_full_moves(self, player):
        all_captures = []

        pieces = player.get_pieces(self)

        for piece in pieces:
            start = Point(piece.y, piece.x)
            capture_tree = self.capture_trees(player, Point(piece.y, piece.x))
            # remove the last element - it contains only the starting point
            capture_tree.pop()
            # since we build the tree starting from the latest moves, we need to reverse it
            capture_tree = [list(reversed(alist)) for alist in capture_tree]
            all_captures.extend(capture_tree)

        # if captures available, one of them needs to be executed
        if all_captures:
            return all_captures

        all_normal_moves = []

        # otherwise only non-capture moves are available
        for piece in pieces:
            start = Point(piece.y, piece.x)
            normal_moves = piece.available_moves(player, self.board)
            normal_tree = [[start, move] for move in normal_moves]
            all_normal_moves.extend(normal_tree)
        return all_normal_moves

    def capture_trees(self, player, start):

        captures = self.board[start.y][start.x].available_moves(player, self.board, must_capture=True)
        # if there are no more captures left to combo, end recursion and return the last visited point
        if not captures:
            return [[start]]

        score_copy = copy.copy(self.score)
        tree = []

        for capture in captures:
            # save board state before move
            original = self.board[start.y][start.x]
            capturing_piece = Piece(original.y, original.x, original.is_white, original.is_queen)
            result, captured_piece = self.move(player, start, capture)

            child_tree = self.capture_trees(player, capture)
            for alist in child_tree:
                alist.append(start)
            tree.extend(child_tree)

            # restore board state after move
            self.undo_capture(capturing_piece, captured_piece, capture)

        tree.append([start])
        self.score = score_copy
        return tree


    def undo_capture(self, capturing, captured, destination):

        self.board[capturing.y][capturing.x] = capturing
        self.board[captured.y][captured.x] = captured

        # remove the piece from the point it jumped to, except when it made a circular combo capture and came back
        # to its starting point
        if destination != capturing.to_point():
            self.board[destination.y][destination.x] = None

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

    def _get_king(self, player, point):
        self.board[point.y][point.x].is_queen = True

    def _try_king(self, player, point):
        if (player.is_white and point.y == 0 or
                not player.is_white and point.y == self.BOARD_SIZE - 1):
            self._get_king(player, point)

    def get_pieces(self, player):
        pieces = []
        for y, x in BoardHelper.possible_tiles:
            piece = self.board[y][x]
            if piece is not None and piece.is_white == player.is_white:
                pieces.append(piece)
        return pieces

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

    def key(self, player):
        whites_turn = player.is_white
        key = str(whites_turn)
        for col in self.board:
            for cell in col:
                if cell is not None:
                    key += (str(cell))
                else:
                    key += '-'
        return key


class BoardHelper:
    possible_tiles = [(y, x) for y in range(Board.BOARD_SIZE)
                      for x in range((y + 1) % 2, Board.BOARD_SIZE, 2)]


if __name__ == '__main__':
    brd = Board()
    brd.display()
