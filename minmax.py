import checkers
import copy


class MinmaxAI(checkers.Player):

    def get_move(self, board):
        best_score = None
        best_move = None
        for move in board.available_moves():
            temp_board = copy.deepcopy(board)
            temp_board.move(self, move[0], move[1])
            new_score = self.minimax_score(temp_board, self.opponent_symbol, depth=10)
            if best_score is None or new_score > best_score:
                best_score = new_score
                best_move = move
        return best_move

    def minmax_score(self, board, current_player, opponent, depth, alfa, beta):
        # white is the maximizer

        # przekazywanie wszedzie player i opponent dosc brzydkie wiec jesli board trzyma czyja tura to bym tego uzywal pozniej

        if board.winner() == current_player:
            return 1
        elif board.winner() == self.opponent_symbol:
            return -1
        elif board.is_draw():
            return 0
        elif depth == 0:
            return self.heuristic(board, current_player, opponent)

        # to musze dostosowac z kolka i krzyzyk na alfe bete ale to zajmie 10 sekund chyba

        scores = []
        for move in board.available_moves():
            temp_board = copy.deepcopy(board)
            temp_board.place_symbol(current_player, *move)
            if current_player.is_white():
                scores.append(self.minimax_score(temp_board, opponent, current_player, depth - 1))
            else:
                scores.append(self.minimax_score(temp_board, current_player, opponent, depth - 1))

        if current_player.is_white():


        if current_player.is_white():
            return max(scores)
        else:
            return min(scores)

    def heuristic(self, board, current_player, opponent, man_val=1, king_val=3):
        # player_score, opponent_score = 0

        current_player_score = self.get_score(current_player, board,  man_val, king_val)
        opponent_score = self.get_score(opponent, board,  man_val, king_val)

        score = abs(current_player_score - opponent_score)
        # return negative value if the current player is black (the minimizer)
        return score if self.is_white() == current_player.is_white() else -score

    def get_score(self, current_player, board, man_val, king_val):
        score = 0
        for piece in current_player.get_pieces(board):
            if piece.is_king:
                score += king_val
            else:
                score += man_val
        return score

        # player_val = sum(values[piece] for piece in player.get_pieces())
