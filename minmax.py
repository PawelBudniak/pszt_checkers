import checkers
import copy
import math


class MinmaxAI(checkers.Player):

    def __init__(self, opponent=None, depth=5):
        self.opponent = opponent
        self.depth = depth


    def get_move(self, board):
        best_score = None
        best_move = None
        for move in board.available_full_moves(self):
            temp_board = copy.deepcopy(board)
            temp_board.full_move(self, move)
            new_score = self.minimax_score(temp_board, self.opponent, self, depth=10, alpha=-math.inf, beta=math.inf)
            if self.is_white:
                if best_score is None or new_score > best_score:
                    best_score = new_score
                    best_move = move
            else:
                if best_score is None or new_score < best_score:
                    best_score = new_score
                    best_move = move
        return best_move

    def minmax_score(self, board, current_player, opponent, depth, alpha, beta):
        # white is the maximizer

        # przekazywanie wszedzie player i opponent dosc brzydkie wiec jesli board trzyma czyja tura to bym tego uzywal pozniej

        if board.winner().is_white:
            return 1
        elif not board.winner().is_white:
            return -1
        elif board.is_draw():
            return 0
        elif depth == 0:
            return self.heuristic(board, current_player, opponent)

        if current_player.is_white:
            max_score = -math.inf
            for move in board.available_full_moves(current_player):
                temp_board = copy.deepcopy(board)
                temp_board.full_move(current_player, move)
                score = self.minmax_score(self, temp_board, opponent, current_player, depth - 1, alpha, beta)
                max_score = max(score, max_score)
                alpha = max(alpha, max_score)
                if beta <= alpha:
                    break
            return max_score
        else:
            min_score = math.inf
            for move in board.available_full_moves():
                temp_board = copy.deepcopy(board)
                temp_board.full_move(current_player, move)
                score = self.minmax_score(self, temp_board, opponent, current_player, depth - 1, alpha, beta)
                min_score = min(score, min_score)
                beta = min(alpha, min_score)
                if beta <= alpha:
                    break
            return min_score

    def heuristic(self, board, current_player, opponent, man_val=1, king_val=3):
        # player_score, opponent_score = 0

        current_player_score = self.get_score(current_player, board, man_val, king_val)
        opponent_score = self.get_score(opponent, board, man_val, king_val)

        score = abs(current_player_score - opponent_score)
        # return negative value if the current player is black (the minimizer)
        return score if current_player.is_white else -score

    def get_score(self, current_player, board, man_val, king_val):
        score = 0
        for piece in current_player.get_pieces(board):
            if piece.is_king:
                score += king_val
            else:
                score += man_val
        return score

        # player_val = sum(values[piece] for piece in player.get_pieces())
