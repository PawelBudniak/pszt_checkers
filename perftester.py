from minmax import *
from player import *
import game


def test_checkers(title, white_player, black_player, depth_range, iterations_count):
    f = open("results.txt", "a")
    f.write(title)
    for i in range(1, depth_range + 1):
        f.write("\nTested depth = " + str(i) + "\n")
        white_player.depth = i
        for j in range(iterations_count):
            f.write("\nIteration number: " + str(j + 1) + "\n")
            test_game = game.Game(white_player, black_player)
            test_game.play(False, False, False, testing=False)
            f.write(test_game.get_stat())
    f.close()


if __name__ == '__main__':
    result_file = open("results.txt", "w").close()
    white_player = MinmaxAI(is_white=True, nocache=True, noab=True, nosort=True)
    black_player = MinmaxAI(is_white=False, opponent=white_player, depth=1, nocache=True, noab=False, nosort=False)
    white_player.opponent = black_player
    test_checkers("\n***\nBare-bones minimax\n***\n", white_player, black_player, 6, 1)
    white_player = MinmaxAI(is_white=True, opponent=black_player, nocache=True, noab=False, nosort=True)
    test_checkers("\n***\nMinmax with ab and no sorting\n***\n", white_player, black_player, 6, 1)
    white_player = MinmaxAI(is_white=True, opponent=black_player, nocache=True, noab=False, nosort=False )
    test_checkers("\n***\nMinmax with ab and sorting\n***\n", white_player, black_player, 6, 5)
    white_player = MinmaxAI(is_white=True, opponent=black_player, nocache=False, noab=False, nosort=False )
    test_checkers("\n***\nMinmax with ab, sorting and caching\n***\n", white_player, black_player, 6, 5)




