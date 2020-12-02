import checkers
import copy
import math


class MinmaxAI(checkers.Player):

    def __init__(self,is_white, opponent=None, depth=5):
        super().__init__(is_white)
        self.opponent = opponent
        self.depth = depth


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
            if self.is_white:
                if best_score is None or new_score > best_score:
                    best_score = new_score
                    best_move = move
            else:
                if best_score is None or new_score < best_score:
                    best_score = new_score
                    best_move = move
        print(best_score)
        for i in range(len(all_scores)):
            print(all_scores[i], moves[i])

        return best_move

    def minmax_score(self, board, current_player, opponent, depth, alpha, beta):
        # white is the maximizer

        # przekazywanie wszedzie player i opponent dosc brzydkie wiec jesli board trzyma czyja tura to bym tego uzywal pozniej

        if board.white_won() is True:
            return 1000
        elif board.white_won() is False:
            return -1000
        elif board.is_draw():
            return 0
        elif depth == 0:
            return self.heuristic(board, current_player, opponent)

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
            return max_score
        else:
            min_score = math.inf
            for move in board.available_full_moves(current_player):
                temp_board = copy.deepcopy(board)
                temp_board.full_move(current_player, move)
                score = self.minmax_score(temp_board, opponent, current_player, depth - 1, alpha, beta)
                min_score = min(score, min_score)
                beta = min(alpha, min_score)
                if beta <= alpha:
                    break
            return min_score

    def heuristic(self, board, current_player, opponent, man_val=1, king_val=5):
        # player_score, opponent_score = 0

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
