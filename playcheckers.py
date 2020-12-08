import minmax
from player import *
import game
import sys
import json


DEFAULT_DEPTH = 5


def my_find(list, el, default=None):
    try:
        return list.index(el)
    except ValueError:
        return default


def get_player_from_args(is_white, opponent, args, start, stop):
    noab = nocache = nosort = False
    depth = DEFAULT_DEPTH

    i = start
    while i != stop and i != len(args):
        if args[i] == '-noab':
            noab = True
        if args[i] == '-nocache':
            nocache = True
        if args[i] == '-nosort':
            nosort = True
        if args[i] == '-depth':
            depth = int(args[i + 1])
            i += 1
        i += 1
    print(noab, nocache, nosort, depth)
    return minmax.MinmaxAI(True, opponent, depth, noab, nocache, nosort)



if __name__ == '__main__':
    args = sys.argv
    p1_start = my_find(args, '-p1')
    p2_start = my_find(args, '-p2')
    testing = False


    if p1_start is not None:
        player1 = get_player_from_args(True, None, args, p1_start, p2_start)
    else:
        player1 = Player(is_white=True)
    if p2_start is not None:
        player2 = get_player_from_args(False, player1, args, p2_start, p1_start)
    else:
        player2 = Player(is_white=False)

    if '-clearcache' in sys.argv:
        minmax.clear_cache()


    if '-test' in sys.argv:
        testing = True

    #  if p1 is AI we need to set his opponent
    if p1_start is not None:
        player1.opponent = player2

    print(player1)
    print(player2)

    game = game.Game(player1, player2)
    game.play(show_display=True, cache_white_player=player1.keeps_cache(), cache_black_player=player2.keeps_cache(), testing=testing)














