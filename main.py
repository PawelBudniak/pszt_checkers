# This is a sample Python script.
import checkers
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    brd = checkers.Board()
    brd.debug = True

    brd.board[2][1] = checkers.Piece(2, 1, False, is_king=True)
    brd.board[3][2] = checkers.Piece(3, 2, True, is_king=False)
    # self.board[4][3] = Piece(True, False, 4, 3)
    brd.board[5][4] = None

    player = checkers.Player(False)
    brd.display()
    brd.available_moves(player, (0, 1), False)
    brd.available_captures(player, (0, 1), False)
    #brd.move(player, (2, 1), (4, 3), False)
    #brd.display()
    #print(brd.is_legal_move((2, 1), (5, 4), False))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
