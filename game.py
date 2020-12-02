
import checkers
import player


class Game:

    def __init__ (self, white_player, black_player):
        self.brd = checkers.Board()
        self.brd.init_board()
        self.brd.white_player = white_player
        self.brd.black_player = black_player
        self.turn_count = 0

    def play(self, show_display, cache_white_player, cache_black_player):

        while self.brd.white_won() is None and self.brd.is_draw() is False:

            if show_display:
                self.brd.display()

            move = self.brd.white_player.get_move(self.brd)

            while not self.brd.full_move(self.brd.white_player, move):
                move = self.brd.white_player.get_move(self.brd)
                if show_display:
                    self.brd.display()

            if show_display:
                self.brd.display()
                print(f'scores = {self.brd.score}')

            move = self.brd.black_player.get_move(self.brd)

            while not self.brd.full_move(self.brd.black_player, move):
                move = self.brd.black_player.get_move(self.brd)
                if show_display:
                    self.brd.display()

            if show_display:
                self.brd.display()
                print(f'scores = {self.brd.score}')

            self.turn_count += 1

        if cache_white_player:
            self.brd.white_player.save_cache()
        if cache_black_player:
            self.brd.black_player.save_cache()

