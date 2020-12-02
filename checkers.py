from enum import Enum
import copy
from player import *


from helper import *


class Board:
    BOARD_SIZE = 8
    PIECES_COUNT = 12

    def __init__(self):
        self.board = [[None for i in range(self.BOARD_SIZE)]
                      for j in range(self.BOARD_SIZE)]
        #self.init_board()
        self.debug = False
        self.score = [self.PIECES_COUNT, self.PIECES_COUNT]
        self.white_queen_moves = 0
        self.black_queen_moves = 0
        self.white_player = None
        self.black_player = None

    def is_draw(self):
        return self.white_queen_moves >= 15 and self.black_queen_moves >= 15


    def white_won(self):
        self.count_pieces()
        if self.score[1] == 0 or not self._can_move(self.black_player):
            return True
        elif self.score[0] == 0 or not self._can_move(self.white_player):
            return False
        else:
            return None

    def count_pieces(self):
        self.score = [0,0]
        for y in range(self.BOARD_SIZE):
            for x in range(self.BOARD_SIZE):
                piece = self.board[y][x]
                if piece is not None and piece.is_white:
                    self.score[0] += 1
                elif piece is not None and not piece.is_white:
                    self.score[1] += 1

    def full_move(self, player, chosen_path):

        board = copy.deepcopy(self.board)
        begin_score = self.score
        if chosen_path is None:
            print(f'white won: {self.white_won()}')
            return False
        # print("Procesowana sciezka: " + str(chosen_path))
        processing = True
        chosen_path = copy.deepcopy(chosen_path)
        move_from = chosen_path.pop(0)
        move_to = chosen_path.pop(0)

        should_capture = self._should_capture(player)

        while processing:
            prev_score = self.score.copy()
            if not self.move(player, move_from, move_to):
                self.board = board
                return False
            if prev_score == self.score and should_capture:
                self.board = board
                print("Player required to capture, wrong move")
                return False
            # player can move multiple times only when capturing
            if prev_score == self.score and chosen_path:
                print("Too many move choices, wrong move")
                self.board = board
                return False
            should_capture = False

            if not chosen_path:
                break
            move_from = move_to
            move_to = chosen_path.pop(0)

        if self.score == begin_score and self.board[move_to.y][move_to.x].is_king:
            if self.board[move_to.y][move_to.x].is_white:
                self.white_queen_moves += 1
            else:
                self.black_queen_moves += 1
        return True

    def _should_capture(self, player):
        for piece in self.get_pieces(player):
            if self.available_captures(player, Point(piece.y, piece.x)):
                return True
        return False

    def _can_move(self, player):
        for piece in self.get_pieces(player):
            if self.available_actions(player, Point(piece.y, piece.x)):
                return True
        return False

    def move(self, player, start, to):
        # miki
        if not self._is_within_constraints(player, start, to):
            print("Error, wrong move")
            return
        from_piece = self.board[start.y][start.x]
        if from_piece.is_king:
            move_analysis = self._king_possible_capture(start, to)
            if not move_analysis[0]:
                return False
            else:
                # if a single piece was captured
                if move_analysis[1] is not None and move_analysis[2] == 1:
                    self.board[move_analysis[1][0]][move_analysis[1][1]] = None
                    if player.is_white:
                        self.count_pieces()
                        #self.score[0] -= 1
                        self.white_queen_moves = 0
                    else:
                        self.count_pieces()
                       # self.score[1] -= 1
                        self.black_queen_moves = 0
        elif not from_piece.is_king:
            if abs(to.y - start.y) == 2:
                self.board[average(to.y, start.y)][average(to.x, start.x)] = None
                if player.is_white:
                    self.count_pieces()
                    self.white_queen_moves = 0
                    pass
                   # self.score[0] -= 1
                else:
                    self.count_pieces()
                    self.black_queen_moves = 0
                    pass
                   #self.score[1] -= 1

        # if from_piece.is_white and to.y == 0 or (not from_piece.is_white) and to.y == self.BOARD_SIZE - 1:
        #     from_piece.is_king = True
        self._execute_move(start,to)
        self._try_king(player, to)
        return True  # successful action

    def _execute_move(self, start, to):
        self.board[to.y][to.x] = self.board[start.y][start.x]
        self.board[start.y][start.x] = None
        piece = self.board[to.y][to.x]
        piece.y = to.y
        piece.x = to.x

    # check if this move is a capture
    def is_legal_capture(self, player, start, to):
        # miki
        captured_piece = None

        if self._is_within_constraints(player, start, to):
            from_piece = self.board[start.y][start.x]
            if from_piece.is_king:
                # handle king behavior
                return self._is_king_legal_capture(start, to)
            else:
                return self._is_man_legal_capture(start, to)
        return False, None

    # check if the move is legal when regarding game's rules
    def is_legal_move(self, player, start, to):
        # miki
        if self._is_within_constraints(player, start, to):
            from_piece = self.board[start.y][start.x]
            if from_piece.is_king:
                # handle king behavior
                return self._is_king_legal_move(start, to), None
            else:
                return self._is_man_legal_move(start, to), None
        return False, None

    def is_legal_action(self, player, start, to):
        # miki

        if self._is_within_constraints(player, start, to):
            from_piece = self.board[start.y][start.x]
            if from_piece.is_king:
                # handle king behavior
                return self._is_king_legal_action(start, to)
            else:
                return self._is_man_legal_action(start, to)
        return False

    # check basic game constraints
    def _is_within_constraints(self, player, start, to):

        if to.y not in range(self.BOARD_SIZE) or to.x not in range(self.BOARD_SIZE) or \
                start.y not in range(self.BOARD_SIZE) or start.x not in range(self.BOARD_SIZE):
            return False
        from_piece = self.board[start.y][start.x]
        # case: out of board bounds
        if from_piece is None:
            return False
        # case: piece not destined for given player
        if not from_piece.is_white == player.is_white:
            return False

        # case: piece cannot move like that because the x-travel distance must be equal to the y-travel distance
        if abs(to.y - start.y) != abs(to.x - start.x):
            return False
        # case: destination taken by another piece
        if self.board[to.y][to.x] is not None:
            return False
        return True

    # underscore na początku metody dajesz to taka kownencja zeby pokazac ze metoda ma byc private (bardziej
    # protected chyba w sumie)
    def _is_king_legal_action(self, start, to):
        result = self._king_possible_capture(start, to)
        if self._king_possible_capture(start, to)[0]:
            return True,
        return False

    def _is_king_legal_capture(self, start, to):
        result = self._king_possible_capture(start, to)
        if result[0] is True and result[1] is not None and result[2] == 1:
            return True, result[1]
        return False, None

    def _is_king_legal_move(self, start, to):
        result = self._king_possible_capture(start, to)
        if result[0] is True and result[1] is None and result[2] == 0:
            return True,
        return False

    # arg 0 tells the user, if the action is at all possible
    # arg 1 holds the captured piece - only, if it was captured
    # arg 2 hold the count of encountered pieces
    def _king_possible_capture(self, start, to):
        from_piece = self.board[start.y][start.x]

        dy = sgn(to.y - start.y)
        dx = sgn(to.x - start.x)

        is_action_possible = True
        captured_pieces = 0
        captured_piece = None  # only useful, if succesful capture

        # look for any pieces on the kings path
        # shift ranges by dx and dy so it goes from [start, stop) to (start, stop] (excludes start, includes stop)
        y_path = range(start.y + dy, to.y + dy, dy)
        x_path = range(start.x + dx, to.x + dx, dx)
        path = zip(y_path, x_path)
        for y, x in path:
            piece = self.board[y][x]
            if piece is not None:
                if piece.is_white == from_piece.is_white:
                    # collision with allied piece
                    is_action_possible = False
                    break
                else:
                    captured_pieces += 1
                    captured_piece = (y, x)
        if captured_pieces not in (0, 1):
            is_action_possible = False
        return is_action_possible, captured_piece, captured_pieces

    def _is_man_legal_action(self, start, to):

        if self._is_man_legal_capture(start, to)[0] or self._is_man_legal_move(start, to):
            return True
        else:
            return False

    def _is_man_legal_capture(self, start, to):

        from_piece = self.board[start.y][start.x]
        delta_y = to.y - start.y

        if abs(delta_y) == 2:
            if self.board[average(to.y, start.y)][average(to.x, start.x)] is None:
                return False, None
            if self.board[average(to.y, start.y)][average(to.x, start.x)].is_white == \
                    from_piece.is_white:
                return False, None
            # if the move is too long in range ( not moving by one step and not capturing )
            else:
                return True, (average(to.y, start.y), average(to.x, start.x))
        return False, None

    # trying to move a piece without capturing
    def _is_man_legal_move(self, start, to):

        from_piece = self.board[start.y][start.x]
        delta_y = to.y - start.y

        if abs(delta_y) == 1:
            if from_piece.is_white and delta_y != -1 or not from_piece.is_white and delta_y != 1:
                return False
            else:
                return True
        return False

    # list all available moves
    # TODO: 2 sprawdzenia
    def available_moves(self, player, start):
        move_list = []
        for row in range(self.BOARD_SIZE):
            for el in range(self.BOARD_SIZE):
                if self.is_legal_move(player, start, Point(row, el))[0]:
                    move_list.append(Point(row, el))
        #print(move_list)
        return move_list

    def available_actions(self, player, start):
        action_list = []
        for row in range(self.BOARD_SIZE):
            for el in range(self.BOARD_SIZE):
                if self.is_legal_action(player, start, Point(row, el)):
                    action_list.append(start)
                    action_list.append(Point(row, el))
        # print(move_list)
        return action_list

    # TODO: pilnowac piece.y i piece.x i chyba score przy tyych wszystkich biciach
    def available_full_moves(self, player):
        all_captures = []
        all_normal_moves = []
        for piece in player.get_pieces(self):
            start = Point(piece.y, piece.x)
            capture_tree = self.capture_trees(player, start)
            capture_tree.pop()  # usuwa taka liste co ma sam pionek startowy, jakos to trzeba zmienic bo jest brzydko
            # since we build the tree starting from the latest moves, we need to reverse it
            capture_tree = [list(reversed(alist)) for alist in capture_tree]
            all_captures.extend(capture_tree)

            normal_moves = self.available_moves(player, Point(piece.y, piece.x))
            normal_tree = [[start, move] for move in normal_moves]
            all_normal_moves.extend(normal_tree)

        #  if available captures, one of them needs to be executed
        if all_captures:
            return all_captures
        else:
            return all_normal_moves

    # def _capture_possibilities(self, player, start, all_moves, move_chain):
    #     captures = self.available_captures(player, start)
    #     move_chain.append(start)
    #     all_moves.append(copy.deepcopy(move_chain))
    #     if captures is None:
    #         return None
    #
    #     board_copy = copy.deepcopy(self.board)
    #
    #     for capture in captures:
    #         self.board = copy.deepcopy(self.board)
    #         self.move(player, start, capture)
    #         self._capture_possibilities(player, capture, all_moves, move_chain)
    #         #if new_chain is not None:
    #             #all_moves.append(new_chain)
    #
    #     self.board = board_copy
    #
    #     return all_moves

    def capture_trees(self, player, start):
        captures = self.available_captures(player, start)
        #if start.y == 6 and start.x == 5:
            #print('d00psko')
        if not captures:
            #print(f'siema: {start}')
            return [[start]]
        board_copy = copy.deepcopy(self.board)
        score_copy = copy.deepcopy(self.score)
        tree = []
        for capture in captures:
            self.board = copy.deepcopy(board_copy)
            if not self.move(player, start, capture):
                print('nie move')
            child_tree = self.capture_trees(player, capture)
            for alist in child_tree:
                alist.append(start)
            tree.extend((child_tree))
        self.board = board_copy
        tree.append([start])
        self.score = score_copy
        return tree




    # list all available captures
    def available_captures(self, player, start):
        move_list = []
        for row in range(self.BOARD_SIZE):
            for el in range(self.BOARD_SIZE):
                if self.is_legal_capture(player, start, Point(row, el))[0]:
                    move_list.append(Point(row, el))
        #print(move_list)
        return move_list

    def init_board(self):
        def fill_row(row, start, is_white):
            for column in range(start, self.BOARD_SIZE, 2):
                self.board[row][column] = Piece(row, column, is_white, False)

        # fill black
        fill_row(0, 1, is_white=False)
        fill_row(1, 0, is_white=False)
        fill_row(2, 1, is_white=False)

        # fill white
        fill_row(self.BOARD_SIZE - 1, 0, is_white=True)
        fill_row(self.BOARD_SIZE - 2, 1, is_white=True)
        fill_row(self.BOARD_SIZE - 3, 0, is_white=True)

    def _get_king(self, player, point):
        self.board[point.y][point.x].is_king = True

    def _try_king(self, player, point):
        if (player.is_white and point.y == 0 or
                not player.is_white and point.y == self.BOARD_SIZE - 1):
            self._get_king(player, point)

    def get_pieces(self, player):
        pieces = []
        for row in self.board:
            for cell in row:
                tmp_piece = cell
                if tmp_piece is not None and tmp_piece.is_white == player.is_white:
                    pieces.append(tmp_piece)
        return pieces

    def display(self):

        def print_horizontal_lines():
            print("   ", end='')
            for _ in range(self.BOARD_SIZE):
                print("--- ", end='')

        # print column ids (letters)
        print("    ", end='')
        for i in range(self.BOARD_SIZE):
            col_id = chr(ord('A') + i) if self.debug is False else str(i)
            print(col_id + "   ", end='')
        print('')

        print_horizontal_lines()

        for y in range(self.BOARD_SIZE):
            print('')  # newline
            row_id = y + 1 if self.debug is False else y
            print(str(row_id) + ' ', end='')  # print row ids (numbers)
            for x in range(self.BOARD_SIZE):
                if self.board[y][x] is None:
                    print("|   ", end='')
                else:
                    print("|{:^3}".format(str(self.board[y][x])), end='')
            print("|")
            print_horizontal_lines()
        print('')  # newline

    def key(self, player):
        whites_turn = player.is_white
        key = str(whites_turn) + '\n'
        for col in self.board:
            for cell in col:
                if cell is not None:
                    key += (str(cell))
                else:
                    key += '-'
            key += '\n'
        return key



class Piece:

    def __init__(self, y, x, is_white, is_king=False):
        self.is_white = is_white
        self.is_king = is_king
        self.y = y
        self.x = x

    def __str__(self):
        if self.is_white:
            char = 'w'
        else:
            char = 'b'
        if self.is_king:
            char = char.upper()
        return char

    def __repr__(self):
        return self.__str__()

if __name__ == '__main__':
    brd = Board()
    brd.display()
