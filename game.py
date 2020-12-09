
import checkers
import player
from time import perf_counter_ns

class Game:

    def __init__ (self, white_player, black_player):
        self.brd = checkers.Board()
        self.brd.init_board()
        self.brd.white_player = white_player
        self.brd.black_player = black_player
        self.turn_count = 0
        self.white_move_count = 0
        self.white_move_time = 0
        self.black_move_count = 0
        self.black_move_time = 0
        self.game_time = 0

    def play(self, show_display, cache_white_player, cache_black_player, testing=False):

        running = True

        game_start = perf_counter_ns()
        while running:
            if show_display:
                self.brd.display()
                print(f'scores = {self.brd.score}')

            t_start = perf_counter_ns()

            move = self.brd.white_player.get_move(self.brd)
            while not self.brd.full_move(self.brd.white_player, move)[0]:
                move = self.brd.white_player.get_move(self.brd)

            t_end = perf_counter_ns()

            self.white_move_count += 1
            self.white_move_time += t_end - t_start

            if self.brd.white_won() is not None or self.brd.is_draw() is True:
                break

            self.turn_count += 1

            if show_display:
                self.brd.display()
                print(f'scores = {self.brd.score}')

            t_start = perf_counter_ns()

            move = self.brd.black_player.get_move(self.brd)
            while not self.brd.full_move(self.brd.black_player, move)[0]:
                move = self.brd.black_player.get_move(self.brd)

            t_end = perf_counter_ns()

            self.black_move_count += 1
            self.black_move_time += t_end - t_start

            if self.brd.white_won() is not None or self.brd.is_draw() is True:
                break

            self.turn_count += 1

        game_end = perf_counter_ns()

        self.game_time = int((game_end - game_start)/1000000)

        if testing:
            self.print_stat()

        if cache_white_player:
            self.brd.white_player.save_cache()
        if cache_black_player:
            self.brd.black_player.save_cache()

    def print_stat(self):
        if self.brd.white_won() is True:
            print("White player won")
        elif self.brd.white_won() is False:
            print("Black player won")
        elif self.brd.is_draw():
            print("A draw")
        print("Game time: " + str(self.game_time) + "ms turn count: " + str(self.turn_count))
        print("White player average move time: "
              + str((self.white_move_time / (1000000 * self.white_move_count))) + "ms")
        print("Black player move count: average move time: "
              + str((self.black_move_time / (1000000 * self.black_move_count))) + "ms")
