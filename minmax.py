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

        self.turn = 0

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
        # print(str(moves))
        # print(moves)
        # all_scores = []
        if not self.nosort:
            moves.sort(key=len, reverse=True)
            # print(str(moves))
        if self.turn == 0 and self.is_white:
            self.turn += 1
            return [Point(5, 0), Point(4, 1)]
        for move in moves:
            # temp_board = copy.deepcopy(board)
            # temp_board.full_move(self, move)
            # if move == [Point(4,1), Point(3,2)]:
            #     print('suicide')
            # if move == [Point(6,1), Point(5,0)]:
            #     print('wybierz to')

            score_copy = copy.copy(board.score)
            w_queen_moves, b_queen_moves = board.white_queen_moves, board.black_queen_moves
            start = board.board[move[0].y][move[0].x]
            starting_piece = Piece(start.y, start.x, start.is_white, start.is_queen)
            result, captured_pieces = board.full_move(self, move)

            new_score = self.minmax_score(board, self.opponent, self, depth=self.depth, alpha=-math.inf,
                                          beta=math.inf)

            board.board[starting_piece.y][starting_piece.x] = starting_piece
            board.board[move[-1].y][move[-1].x] = None
            if captured_pieces:
                for piece in captured_pieces:
                    board.board[piece.y][piece.x] = piece
            board.score = score_copy
            board.white_queen_moves = w_queen_moves
            board.black_queen_moves = b_queen_moves

            # all_scores.append(new_score)
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

        # print(f'Best score: {best_score}')
        # for i in range(len(all_scores)):
        #     print(f' Scores: {all_scores[i]}, Moves:  {moves[i]}')

        self.turn += 1
        if not best_move:
            print('brak ruchow')

        return best_move

    def cache_and_return(self, board, current_player, score, depth, type):
        if self.nocache:
            return score
        self.cache[board.key(current_player)] = CacheEntry(score, depth, type)
        return score

    def minmax_score(self, board, current_player, opponent, depth, alpha, beta):

        # white is the maximizer
        if not self.nocache:
            board_key = board.key(current_player)
            cache_entry = self.cache.get(board_key, None)

        if (not self.nocache
                and cache_entry is not None
                and cache_entry.depth >= depth):

            # if the value wasn't estimated by alpha beta just return it
            if cache_entry.type == EntryType.EXACT:
                return cache_entry.value

            # if it was estimated, use the estimation to possibly adjust alpha or beta
            elif cache_entry.type == EntryType.UPPERBOUND:
                beta = min(beta, cache_entry.value)
            elif cache_entry.type == EntryType.LOWERBOUND:
                alpha = max(alpha, cache_entry.value)

                if beta <= alpha:
                    # bez cache na wiki?
                    return cache_entry.value

        if board.white_won() is True:
            return self.cache_and_return(board, current_player, self.WIN_SCORE, depth, EntryType.EXACT)
        elif board.white_won() is False:
            return self.cache_and_return(board, current_player, -self.WIN_SCORE, depth, EntryType.EXACT)
        elif board.is_draw():
            return self.cache_and_return(board, current_player, 0, depth, EntryType.EXACT)
        elif depth == 0:
            h_score = self.heuristic(board, current_player, opponent)
            return self.cache_and_return(board, current_player, h_score, depth, EntryType.EXACT)

        if current_player.is_white:
            max_score = -math.inf
            for move in board.available_full_moves(current_player):
                # temp_board = copy.deepcopy(board)
                # temp_board.full_move(current_player, move)
                if len(move) > 2:
                    print(move[0].y, move[0].x)
                    print(move[-1].y, move[-1].x)

                score_copy = copy.copy(board.score)
                w_queen_moves, b_queen_moves = board.white_queen_moves, board.black_queen_moves
                start = board.board[move[0].y][move[0].x]
                starting_piece = Piece(start.y, start.x, start.is_white, start.is_queen)
                result, captured_pieces = board.full_move(current_player, move)

                if result == False:
                    print('ciekawe')

                score = self.minmax_score(board, opponent, current_player, depth - 1, alpha, beta)
                max_score = max(score, max_score)

                board.board[starting_piece.y][starting_piece.x] = starting_piece
                board.board[move[-1].y][move[-1].x] = None
                if captured_pieces:
                    for piece in captured_pieces:
                        board.board[piece.y][piece.x] = piece
                board.score = score_copy
                board.white_queen_moves = w_queen_moves
                board.black_queen_moves = b_queen_moves


                if not self.noab:
                    alpha = max(alpha, max_score)
                    if beta <= alpha:
                        return self.cache_and_return(board, current_player, max_score, depth, EntryType.LOWERBOUND)

            return self.cache_and_return(board, current_player, max_score, depth, EntryType.EXACT)

        else:
            # best_board = board
            min_score = math.inf
            for move in board.available_full_moves(current_player):
                # temp_board = copy.deepcopy(board)
                # temp_board.full_move(current_player, move)

                score_copy = copy.copy(board.score)
                w_queen_moves, b_queen_moves = board.white_queen_moves, board.black_queen_moves
                start = board.board[move[0].y][move[0].x]
                starting_piece = Piece(start.y, start.x, start.is_white, start.is_queen)
                result, captured_pieces = board.full_move(current_player, move)

                if result == False:
                    print('ciekawe')

                score = self.minmax_score(board, opponent, current_player, depth - 1, alpha, beta)
                min_score = min(score, min_score)

                board.board[starting_piece.y][starting_piece.x] = starting_piece
                board.board[move[-1].y][move[-1].x] = None
                if captured_pieces:
                    for piece in captured_pieces:
                        board.board[piece.y][piece.x] = piece
                board.score = score_copy
                board.white_queen_moves = w_queen_moves
                board.black_queen_moves = b_queen_moves


                if not self.noab:
                    beta = min(beta, min_score)
                    if beta <= alpha:
                        return self.cache_and_return(board, current_player, alpha, depth, EntryType.UPPERBOUND)

            return self.cache_and_return(board, current_player, min_score, depth, EntryType.EXACT)

    # def minmax_score(self, board, current_player, opponent, depth, alpha, beta):
    #
    #     # white is the maximizer
    #     if not self.nocache:
    #         board_key = board.key(current_player)
    #
    #     if self.nocache or board_key not in self.cache:
    #         if board.white_won() is True:
    #             return self.cache_and_return(board, current_player, self.WIN_SCORE)
    #         elif board.white_won() is False:
    #             return self.cache_and_return(board, current_player, -self.WIN_SCORE)
    #         elif board.is_draw():
    #             return self.cache_and_return(board, current_player, 0)
    #         elif depth == 0:
    #             h_score = self.heuristic(board, current_player, opponent)
    #             return self.cache_and_return(board, current_player, h_score)
    #
    #         if current_player.is_white:
    #             for move in board.available_full_moves(current_player):
    #                 temp_board = copy.deepcopy(board)
    #                 temp_board.full_move(current_player, move)
    #                 alpha = max(alpha, self.minmax_score(temp_board, opponent, current_player, depth - 1, alpha, beta))
    #                 if alpha >= beta:
    #                     break
    #             return self.cache_and_return(board, current_player, beta)
    #
    #         else:
    #             for move in board.available_full_moves(current_player):
    #                 temp_board = copy.deepcopy(board)
    #                 temp_board.full_move(current_player, move)
    #                 beta = min(beta, self.minmax_score(temp_board, opponent, current_player, depth - 1, alpha, beta))
    #                 if alpha >= beta:
    #                     break
    #             return self.cache_and_return(board, current_player, alpha)
    #     else:
    #         return self.cache[board_key]

    def heuristic(self, board, current_player, opponent, man_val=1, king_val=5):
        white_score = self.get_score(True, board, man_val, king_val)
        black_score = self.get_score(False, board, man_val, king_val)

        score = white_score - black_score
        # return negative value if the current player is black (the minimizer)
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


class CacheEntry:

    def __init__(self, value, depth, type):
        self.value = value
        self.depth = depth
        self.type = type


class EntryType:
    EXACT = 0
    LOWERBOUND = -1
    UPPERBOUND = 1
    TERMINAL = 2
    HEURISTIC = 3

    # player_val = sum(values[piece] for piece in player.get_pieces())

# class TestMinimaxAI(MinmaxAI):
#
#     def __init__(self, is_white, opponent, depth, noab=False, nocache=False, nosort=False):
#         super().__init__(is_white, opponent, depth)
#         self.noab = noab
#         self.nocache = nocache
#         self.nosort = nosort
#
#
#     def get_move(self, board):
#
#         moves = board.available_full_moves(self)
#         if not self.nosort:
#             moves.sort(key=len)
#         for move in moves:
#             temp_board = copy.deepcopy(board)
#             temp_board.full_move(self, move)
#             # if self.noab:
#             #     new_score = self.minmax_score_noab(temp_board, self.opponent, self, depth=self.depth)
#             # else:
#             new_score = self.minmax_score(temp_board, self.opponent, self, depth=self.depth, alpha=-math.inf,
#                                               beta=math.inf)
#             # white maximizes
#             if self.is_white:
#                 if best_score is None or new_score > best_score:
#                     best_score = new_score
#                     best_move = move
#             # black minimizes
#             else:
#                 if best_score is None or new_score < best_score:
#                     best_score = new_score
#                     best_move = move
#
#         return best_move
#
#     def minmax_score(self, board, current_player, opponent, depth, alpha, beta):
#
#         # white is the maximizer
#         if not self.nocache:
#             board_key = board.key(current_player)
#
#         if self.nocache or board_key not in self.cache:
#             if board.white_won() is True:
#                 return self.cache_and_return(board, current_player, self.WIN_SCORE)
#             elif board.white_won() is False:
#                 return self.cache_and_return(board, current_player, -self.WIN_SCORE)
#             elif board.is_draw():
#                 return self.cache_and_return(board, current_player, 0)
#             elif depth == 0:
#                 h_score = self.heuristic(board, current_player, opponent)
#                 return self.cache_and_return(board, current_player, h_score)
#
#             if current_player.is_white:
#                 max_score = -math.inf
#                 for move in board.available_full_moves(current_player):
#                     temp_board = copy.deepcopy(board)
#                     temp_board.full_move(current_player, move)
#                     score = self.minmax_score(temp_board, opponent, current_player, depth - 1, alpha, beta)
#                     max_score = max(score, max_score)
#                     if not self.noab:
#                         alpha = max(alpha, max_score)
#                         if beta <= alpha:
#                             break
#                 return self.cache_and_return(board, current_player, max_score)
#
#             else:
#                 min_score = math.inf
#                 for move in board.available_full_moves(current_player):
#                     temp_board = copy.deepcopy(board)
#                     temp_board.full_move(current_player, move)
#                     score = self.minmax_score(temp_board, opponent, current_player, depth - 1, alpha, beta)
#                     min_score = min(score, min_score)
#                     if not self.noab:
#                         beta = min(beta, min_score)
#                         if beta <= alpha:
#                             break
#                 return self.cache_and_return(board, current_player, min_score)
#         else:
#             return self.cache[board_key]
#
#
#     def cache_and_return(self, board, current_player, score):
#         if self.nocache:
#             return score
#         else:
#             super().cache_and_return(board, current_player, score)
#
#
#
#     # na wszelki, ale sie nie przyda raczej
#     def minmax_score_noab(self, board, current_player, opponent, depth):
#         # white is the maximizer
#
#         if self.nocache:
#             board_key = board.key(current_player)
#         if self.nocache or board_key not in self.cache:
#             if board.white_won() is True:
#                 return self.cache_and_return(board, current_player, self.WIN_SCORE)
#             elif board.white_won() is False:
#                 return self.cache_and_return(board, current_player, -self.WIN_SCORE)
#             elif board.is_draw():
#                 return self.cache_and_return(board, current_player, 0)
#             elif depth == 0:
#                 h_score = self.heuristic(board, current_player, opponent)
#                 return self.cache_and_return(board, current_player, h_score)
#
#             if current_player.is_white:
#                 max_score = -math.inf
#                 for move in board.available_full_moves(current_player):
#                     temp_board = copy.deepcopy(board)
#                     temp_board.full_move(current_player, move)
#                     score = self.minmax_score(temp_board, opponent, current_player, depth - 1)
#                     max_score = max(score, max_score)
#                 return self.cache_and_return(board, current_player, max_score)
#
#             else:
#                 min_score = math.inf
#                 for move in board.available_full_moves(current_player):
#                     temp_board = copy.deepcopy(board)
#                     temp_board.full_move(current_player, move)
#                     score = self.minmax_score(temp_board, opponent, current_player, depth - 1)
#                     min_score = min(score, min_score)
#                 return self.cache_and_return(board, current_player, min_score)
#         else:
#             return self.cache[board_key]
