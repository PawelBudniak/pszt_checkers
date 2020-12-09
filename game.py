
import checkers
import player
from minmax import *
from time import perf_counter_ns

class Game:

    def __init__ (self, white_player, black_player):
        self.brd = checkers.Board()
        self.brd.init_board()
        self.brd.white_player = white_player
        self.brd.black_player = black_player
        self.turn_count = 0
        self.max_white_move_time = 0
        self.average_white_move_time = 0
        self.max_black_move_time = 0
        self.average_black_move_time = 0
        self.game_time = 0
        self.game_winner = None
        self.draw = False

    def get_stats(self):
        return()

    def play(self, show_display, cache_white_player, cache_black_player, testing=False):

        running = True
        white_move_count = 0
        white_move_time = 0
        black_move_count = 0
        black_move_time = 0

        game_start = perf_counter_ns()
        while running:
            if show_display:
                self.brd.display()
                print(f'scores = {self.brd.score}')

            t_start = perf_counter_ns()

            move = self.brd.white_player.get_move(self.brd)
            while not self.brd.full_move(self.brd.white_player, move)[0]:
                if show_display and not isinstance(self.brd.black_player, MinmaxAI):
                    print("Not a viable option!\n")
                    self.brd.display()
                    print(f'scores = {self.brd.score}')
                move = self.brd.white_player.get_move(self.brd)

            t_end = perf_counter_ns()

            white_move_count += 1
            duration = t_end - t_start
            white_move_time += duration
            duration /= 1000000
            if duration > self.max_white_move_time:
                print(duration, self.max_white_move_time)
                self.max_white_move_time = int(duration)

            if self.brd.white_won() is not None or self.brd.is_draw() is True:
                break

            self.turn_count += 1

            if show_display:
                self.brd.display()
                print(f'scores = {self.brd.score}')

            t_start = perf_counter_ns()

            move = self.brd.black_player.get_move(self.brd)
            while not self.brd.full_move(self.brd.black_player, move)[0]:
                if show_display and not isinstance(self.brd.black_player, MinmaxAI):
                    self.brd.display()
                    print("Not a viable option!\n")
                    print(f'scores = {self.brd.score}')
                move = self.brd.black_player.get_move(self.brd)

            t_end = perf_counter_ns()

            black_move_count += 1
            duration = t_end - t_start
            black_move_time += duration
            duration /= 1000000
            if duration > self.max_black_move_time:
                self.max_black_move_time = int(duration)

            self.game_winner = self.brd.white_won()
            self.draw = self.brd.is_draw()

            if self.game_winner is not None or self.draw is True:
                break

            self.turn_count += 1

        game_end = perf_counter_ns()

        self.game_time = int((game_end - game_start)/1000000)
        self.average_white_move_time = int(white_move_time / (1000000 * white_move_count))
        self.average_black_move_time = int(black_move_time / (1000000 * black_move_count))

        if testing:
            self.print_stat()
        if cache_white_player:
            self.brd.white_player.save_cache()
        if cache_black_player:
            self.brd.black_player.save_cache()

    def print_stat(self):
        if self.game_winner is True:
            print("White player won")
        elif self.game_winner is False:
            print("Black player won")
        elif self.draw:
            print("A draw")
        print("Game time: " + str(self.game_time) + "ms turn count: " + str(self.turn_count))
        print("White player average move time: "
              + str(self.average_white_move_time) + "ms")
        print("Longest white player move time: " + str(self.max_white_move_time) + "ms")
        print("Black player average move time: "
              + str(self.average_black_move_time) + "ms")
        print("Longest black player move time: " + str(self.max_black_move_time) + "ms")

