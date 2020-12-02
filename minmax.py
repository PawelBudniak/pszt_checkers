import checkers
import copy
import math
import player
import json


class MinmaxAI(player.Player):

    CACHE_FILE = 'board_scores.json'
    WIN_SCORE = 1000

    def __init__(self,is_white, opponent=None, depth=5):
        super().__init__(is_white)
        self.opponent = opponent
        self.depth = depth
        self.cache = self.load_cache()

    def load_cache(self):
        with open(self.CACHE_FILE, 'r') as fp:
            try:
                return json.load(fp)
            # if file is empty cache is empty
            except json.decoder.JSONDecodeError:
                return {}


    def save_cache(self):
        with open(self.CACHE_FILE, 'w') as fp:
            json.dump(self.cache, fp)



    def get_move(self, board):
        best_score = None
        best_move = None
        moves = board.available_full_moves(self)
        print(moves)
        all_scores = []
        for move in moves:
            temp_board = copy.deepcopy(board)
            temp_board.full_move(self, move)
            new_score = self.minmax_score(temp_board, self.opponent, self, depth=self.depth, alpha=-math.inf, beta=math.inf)
            all_scores.append(new_score)
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

        print(best_score)
        for i in range(len(all_scores)):
            print(all_scores[i], moves[i])

        return best_move

    def cache_and_return(self, board, current_player, score):
        self.cache[board.key(current_player)] = score
        return score

    def minmax_score(self, board, current_player, opponent, depth, alpha, beta):
        # white is the maximizer
        board_key = board.key(current_player)

        if board_key not in self.cache:
            if board.white_won() is True:
                return self.cache_and_return(board, current_player, self.WIN_SCORE)
            elif board.white_won() is False:
                return self.cache_and_return(board, current_player, -self.WIN_SCORE)
            elif board.is_draw():
                return self.cache_and_return(board, current_player, 0)
            elif depth == 0:
                h_score = self.heuristic(board, current_player, opponent)
                return self.cache_and_return(board, current_player, h_score)

            if current_player.is_white:
                max_score = -math.inf
                for move in board.available_full_moves(current_player):
                    temp_board = copy.deepcopy(board)
                    temp_board.full_move(current_player, move)
                    score = self.minmax_score(temp_board, opponent, current_player, depth - 1, alpha, beta)
                    max_score = max(score, max_score)
                    alpha = max(alpha, max_score)
                    if beta <= alpha:
                        break
                return self.cache_and_return(board, current_player, max_score)

            else:
                min_score = math.inf
                for move in board.available_full_moves(current_player):
                    temp_board = copy.deepcopy(board)
                    temp_board.full_move(current_player, move)
                    score = self.minmax_score(temp_board, opponent, current_player, depth - 1, alpha, beta)
                    min_score = min(score, min_score)
                    beta = min(beta, min_score)
                    if beta <= alpha:
                        break
                return self.cache_and_return(board, current_player, min_score)
        else:
            return self.cache[board_key]



    def heuristic(self, board, current_player, opponent, man_val=1, king_val=5):

        # current_player_score = self.get_score(current_player, board, man_val, king_val)
        # opponent_score = self.get_score(opponent, board, man_val, king_val)
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
            if piece.is_king:
                score += king_val
            else:
                score += man_val
        return score

        # player_val = sum(values[piece] for piece in player.get_pieces())

class TestMinimaxAI(MinmaxAI):

    def __init__(self, is_white, opponent=None, depth=5, noab, no):


    def minmax_score(self, board, current_player, opponent, depth):
        # white is the maximizer
        board_key = board.key(current_player)

        if board_key not in self.cache:
            if board.white_won() is True:
                return self.cache_and_return(board, current_player, self.WIN_SCORE)
            elif board.white_won() is False:
                return self.cache_and_return(board, current_player, -self.WIN_SCORE)
            elif board.is_draw():
                return self.cache_and_return(board, current_player, 0)
            elif depth == 0:
                h_score = self.heuristic(board, current_player, opponent)
                return self.cache_and_return(board, current_player, h_score)

            if current_player.is_white:
                max_score = -math.inf
                for move in board.available_full_moves(current_player):
                    temp_board = copy.deepcopy(board)
                    temp_board.full_move(current_player, move)
                    score = self.minmax_score(temp_board, opponent, current_player, depth - 1)
                    max_score = max(score, max_score)
                return self.cache_and_return(board, current_player, max_score)

            else:
                min_score = math.inf
                for move in board.available_full_moves(current_player):
                    temp_board = copy.deepcopy(board)
                    temp_board.full_move(current_player, move)
                    score = self.minmax_score(temp_board, opponent, current_player, depth - 1)
                    min_score = min(score, min_score)
                return self.cache_and_return(board, current_player, min_score)
        else:
            return self.cache[board_key]
