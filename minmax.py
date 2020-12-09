import checkers
import copy
import math
import player
import json
from helper import *
import pickle
from piece import Piece


def clear_cache():
    with open(MinmaxAI.CACHE_FILE, 'wb') as fp:
        pickle.dump({}, fp)


class MinmaxAI(player.Player):
    CACHE_FILE = 'board_scores.pickle'
    WIN_SCORE = math.inf

    def __init__(self, is_white, opponent=None, depth=5, noab=False, nocache=False, nosort=False):
        super().__init__(is_white)
        self.opponent = opponent
        self.depth = depth
        self.noab = noab
        self.nocache = nocache
        self.nosort = nosort
        if not nocache:
            self.cache = self.load_cache()
        else:
            self.cache = {}

    def load_cache(self):
        try:
            with open(self.CACHE_FILE, 'rb') as fp:
                return pickle.load(fp)
        except FileNotFoundError:
            return {}

    def save_cache(self):
        with open(self.CACHE_FILE, 'wb') as fp:
            pickle.dump(self.cache, fp)

    def keeps_cache(self):
        return not self.nocache

    def get_move(self, board):
        best_score = None
        best_move = None
        moves = board.available_full_moves(self)

        if not self.nosort:
            moves.sort(key=len, reverse=True)

        for move in moves:

            # save board state before move
            move_info = MoveInfo(board, move)
            result, captured_pieces = board.full_move(self, move)
            move_info.captured_pieces = captured_pieces

            new_score = self.minmax_score(board, self.opponent, self, depth=self.depth, alpha=-math.inf,
                                          beta=math.inf)

            move_info.undo_full_move()

            # white maximizes
            if self.is_white:
                if best_score is None or new_score > best_score:
                    best_score = new_score
                    best_move = move
            # black minimizes
            else:
                if best_score is None or new_score < best_score:
                    best_score = new_score
                    best_move = move

        return best_move

    def cache_and_return(self, board_key, score, depth, type):
        if self.nocache:
            return score
        self.cache[board_key] = CacheEntry(score, depth, type)
        return score

    def minmax_score(self, board, current_player, opponent, depth, alpha, beta):

        board_key = None
        # white is the maximizer
        if not self.nocache:
            board_key = board.key(current_player)
            cache_entry = self.cache.get(board_key, None)

        # If entry was found for the current board state:
        # Check if it was found at a depth bigger or equal to current
        # If it wasn't, then it possibly contains less information than this function could find - so we ignore it
        # This fact is irrelevant for terminal board states (with abs(cache_entry.value) == math.inf),
        # since if we can guarantee a win in 3 moves, analyzing next moves won't provide any new information

        if (not self.nocache
                and cache_entry is not None
                and (cache_entry.depth >= depth or abs(cache_entry.value) == math.inf)):

            # if the value wasn't estimated by alpha beta just return it
            if cache_entry.type == EntryType.EXACT:
                return cache_entry.value

            # if it was estimated, use the estimation to possibly adjust alpha or beta
            elif cache_entry.type == EntryType.UPPERBOUND:
                beta = min(beta, cache_entry.value)
            elif cache_entry.type == EntryType.LOWERBOUND:
                alpha = max(alpha, cache_entry.value)

                if beta <= alpha:
                    return cache_entry.value

        if board.white_won() is True:
            return self.cache_and_return(board_key, self.WIN_SCORE, depth, EntryType.EXACT)
        elif board.white_won() is False:
            return self.cache_and_return(board_key, -self.WIN_SCORE, depth, EntryType.EXACT)
        elif board.is_draw():
            return self.cache_and_return(board_key, 0, depth, EntryType.EXACT)
        elif depth == 0:
            h_score = self.heuristic(board, current_player, opponent)
            return self.cache_and_return(board_key, h_score, depth, EntryType.EXACT)

        if current_player.is_white:
            max_score = -math.inf

            moves = board.available_full_moves(current_player)
            if not self.nosort:
                moves.sort(key=len, reverse=True)
            for move in moves:

                # save board state before move
                move_info = MoveInfo(board, move)
                result, captured_pieces = board.full_move(current_player, move)
                move_info.captured_pieces = captured_pieces

                score = self.minmax_score(board, opponent, current_player, depth - 1, alpha, beta)
                max_score = max(score, max_score)

                move_info.undo_full_move()

                if not self.noab:
                    alpha = max(alpha, max_score)
                    if beta <= alpha:
                        return self.cache_and_return(board_key, max_score, depth, EntryType.LOWERBOUND)

            return self.cache_and_return(board_key, max_score, depth, EntryType.EXACT)

        else:
            min_score = math.inf
            moves = board.available_full_moves(current_player)
            if not self.nosort:
                moves.sort(key=len, reverse=True)
            for move in moves:

                # save board state before move
                move_info = MoveInfo(board, move)
                result, captured_pieces = board.full_move(current_player, move)
                move_info.captured_pieces = captured_pieces

                score = self.minmax_score(board, opponent, current_player, depth - 1, alpha, beta)
                min_score = min(score, min_score)

                move_info.undo_full_move()

                if not self.noab:
                    beta = min(beta, min_score)
                    if beta <= alpha:
                        return self.cache_and_return(board_key, alpha, depth, EntryType.UPPERBOUND)

            return self.cache_and_return(board_key, min_score, depth, EntryType.EXACT)

    def heuristic(self, board, current_player, opponent, man_val=1, king_val=5):
        white_score = self.get_score(True, board, man_val, king_val)
        black_score = self.get_score(False, board, man_val, king_val)

        score = white_score - black_score
        return score

    def get_score(self, is_white, board, man_val, king_val):
        score = 0
        if is_white:
            current_player = board.white_player
        else:
            current_player = board.black_player
        for piece in current_player.get_pieces(board):
            if piece.is_queen:
                score += king_val
            else:
                score += man_val
        return score


class MoveInfo:
    """
    Holds information necessary to revert a full move
    """

    def __init__(self, board, move):
        self.board = board
        self.starting_piece = copy.copy(board.board[move[0].y][move[0].x])
        self.score = copy.copy(board.score)
        self.w_queen_moves = board.white_queen_moves
        self.b_queen_moves = board.black_queen_moves
        self.final_point = move[-1]
        self.captured_pieces = None

    def undo_full_move(self):
        self.board.board[self.starting_piece.y][self.starting_piece.x] = self.starting_piece

        # remove the piece from the point it jumped to, except when it made a circular combo capture and came back
        # to its starting point
        if self.starting_piece.to_point() != self.final_point:
            self.board.board[self.final_point.y][self.final_point.x] = None
        if self.captured_pieces:
            for piece in self.captured_pieces:
                self.board.board[piece.y][piece.x] = piece
        self.board.score = self.score
        self.board.white_queen_moves = self.w_queen_moves
        self.board.black_queen_moves = self.b_queen_moves


class CacheEntry:

    def __init__(self, value, depth, type):
        self.value = value
        self.depth = depth
        self.type = type


class EntryType:
    EXACT = 0
    LOWERBOUND = -1
    UPPERBOUND = 1
