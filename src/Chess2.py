from src.moving import get_squares_in_between, move_is_vertical, get_distance_between_rows, move_is_diagonal, \
    move_is_knightmove, move_is_rookmove, move_is_queenmove, move_is_kingmove, get_opposite_color, get_to_square, \
    knight_move_vectors, col_dict
from src.game_setup import square_names, square_names_for_display
import time


def timeit(func):
    def measure_time(*args, **kw):
        start_time = time.time()
        result = func(*args, **kw)
        print("Processing time of %s(): %.2f seconds."
              % (func.__qualname__, time.time() - start_time))
        return result
    return measure_time


def countit(func):
    def count_calls(*args, **kw):
        count_calls.calls += 1
        return func(*args, **kw)
    count_calls.calls = 0
    count_calls.name = func.__qualname__
    return count_calls


class Board:
    def __init__(self):
        self.result = None
        self.game_ended = False
        self.h8_rook_has_moved = False
        self.a8_rook_has_moved = False
        self.h1_rook_has_moved = False
        self.a1_rook_has_moved = False
        self.black_king_has_moved = False
        self.white_king_has_moved = False
        self.a1 = "white rook"
        self.a2 = "white pawn"
        self.a3 = "empty"
        self.a4 = "empty"
        self.a5 = "empty"
        self.a6 = "empty"
        self.a7 = "black pawn"
        self.a8 = "black rook"
        self.b1 = "white knight"
        self.b2 = "white pawn"
        self.b3 = "empty"
        self.b4 = "empty"
        self.b5 = "empty"
        self.b6 = "empty"
        self.b7 = "black pawn"
        self.b8 = "black knight"
        self.c1 = "white bishop"
        self.c2 = "white pawn"
        self.c3 = "empty"
        self.c4 = "empty"
        self.c5 = "empty"
        self.c6 = "empty"
        self.c7 = "black pawn"
        self.c8 = "black bishop"
        self.d1 = "white queen"
        self.d2 = "white pawn"
        self.d3 = "empty"
        self.d4 = "empty"
        self.d5 = "empty"
        self.d6 = "empty"
        self.d7 = "black pawn"
        self.d8 = "black queen"
        self.e1 = "white king"
        self.e2 = "white pawn"
        self.e3 = "empty"
        self.e4 = "empty"
        self.e5 = "empty"
        self.e6 = "empty"
        self.e7 = "black pawn"
        self.e8 = "black king"
        self.f1 = "white bishop"
        self.f2 = "white pawn"
        self.f3 = "empty"
        self.f4 = "empty"
        self.f5 = "empty"
        self.f6 = "empty"
        self.f7 = "black pawn"
        self.f8 = "black bishop"
        self.g1 = "white knight"
        self.g2 = "white pawn"
        self.g3 = "empty"
        self.g4 = "empty"
        self.g5 = "empty"
        self.g6 = "empty"
        self.g7 = "black pawn"
        self.g8 = "black knight"
        self.h1 = "white rook"
        self.h2 = "white pawn"
        self.h3 = "empty"
        self.h4 = "empty"
        self.h5 = "empty"
        self.h6 = "empty"
        self.h7 = "black pawn"
        self.h8 = "black rook"
        self.last_move = tuple()
        self.last_piece_captured = "empty"

    @countit
    def put(self, piece, square):
        setattr(self, square, piece)

    @countit
    def free_square(self, square):
        setattr(self, square, "empty")

    @countit
    def is_occupied(self, square):
        return getattr(self, square) != "empty"

    @countit
    def move(self, from_square, to_square, undo=False):
        if not undo:
            self.last_move = (from_square, to_square)
            self.last_piece_captured = getattr(self, to_square)
        piece = getattr(self, from_square)
        self.put(piece, to_square)
        self.free_square(from_square)

    @countit
    def color_that_occupies(self, square):
        color = getattr(self, square).split(" ")[0]
        return color

    @countit
    def is_on_board(self, square):
        if getattr(self, square, "False") == "False":
            return False
        else:
            return True

    @countit
    def path_is_clear(self, from_square, to_square):
        for square in get_squares_in_between(from_square, to_square):
            if self.is_occupied(square):
                return False
        else:
            return True

    @countit
    def get_kind_of_piece_on(self, square):
        piece = getattr(self, square)
        if " " in piece:
            return piece.split(" ")[1]
        else:
            return piece

    @countit
    def is_reachable(self, from_square, to_square, color_to_move):
        if not self.correct_color_is_moved(from_square, color_to_move):
            return False
        if not self.path_is_clear(from_square, to_square):
            if self.get_kind_of_piece_on(from_square) != "knight":
                return False
        if self.square_is_occupied_by_own_color(color_to_move, to_square):
            return False
        if self.get_kind_of_piece_on(from_square) == "pawn":
            return self.pawn_move_is_legal(from_square, to_square)
        if self.get_kind_of_piece_on(from_square) == "rook":
            return move_is_rookmove(from_square, to_square)
        if self.get_kind_of_piece_on(from_square) == "bishop":
            return move_is_diagonal(from_square, to_square)
        if self.get_kind_of_piece_on(from_square) == "knight":
            return move_is_knightmove(from_square, to_square)
        if self.get_kind_of_piece_on(from_square) == "queen":
            return move_is_queenmove(from_square, to_square)
        if self.get_kind_of_piece_on(from_square) == "king":
            return (move_is_kingmove(from_square, to_square) or
                    self.move_is_castling(from_square, to_square, color_to_move))
        return False

    @countit
    def pawn_move_is_legal(self, from_square, to_square):
        if self.pawn_moves_forward(from_square, to_square):
            if move_is_vertical(from_square, to_square) and getattr(self, to_square) == "empty":
                if get_distance_between_rows(from_square, to_square) == 1:
                    return True
                if (self.pawn_is_on_initial_square(from_square)
                        and get_distance_between_rows(from_square, to_square) == 2):
                    return True
            if (move_is_diagonal(from_square, to_square)
                    and get_distance_between_rows(from_square, to_square) == 1
                    and self.move_is_capture_move(from_square, to_square)):
                return True
        return False

    @countit
    def pawn_moves_forward(self, from_square, to_square):
        if self.color_that_occupies(from_square) == "white":
            return int(to_square[1]) > int(from_square[1])
        if self.color_that_occupies(from_square) == "black":
            return int(to_square[1]) < int(from_square[1])

    @countit
    def square_is_occupied_by_own_color(self, color, square):
        return self.color_that_occupies(square) == color

    @countit
    def pawn_is_on_initial_square(self, square):
        color = self.color_that_occupies(square)
        if color == "white" and square[1] == "2":
            return True
        if color == "black" and square[1] == "7":
            return True
        return False

    @countit
    def move_is_capture_move(self, from_square, to_square):
        return (self.color_that_occupies(to_square) != "empty"
                and self.color_that_occupies(to_square) != self.color_that_occupies(from_square))

    @countit
    def correct_color_is_moved(self, from_square, color_to_move):
        return self.color_that_occupies(from_square) == color_to_move

    @countit
    def king_in_check_after_move(self, from_square, to_square, color_to_move):
        self.move(from_square, to_square)
        king_in_check = self.king_in_check(color_to_move)
        self.undo_last_move()
        return king_in_check

    @countit
    def get_legal_to_squares(self, from_square):
        legal_moves = set()
        for to_square in square_names:
            if self.is_reachable(from_square, to_square,
                                 self.color_that_occupies(from_square)):
                legal_moves.add(to_square)
        return legal_moves

    @countit
    def undo_last_move(self):
        self.move(self.last_move[1], self.last_move[0], undo=True)
        self.put(self.last_piece_captured, self.last_move[1])

    def white_king_in_check(self):
        return self.king_in_check("white")

    def black_king_in_check(self):
        return self.king_in_check("black")

    @countit
    def king_in_check(self, color):
        king_square = self.get_king_square(color)
        # is king checked by knight?
        for knight_move_vector in knight_move_vectors:
            to_square = get_to_square(king_square, knight_move_vector)
            if self.is_on_board(to_square):
                if getattr(self, to_square) == get_opposite_color(color) + " knight":
                    return True
        # is an opposite rook/queen closer than a friendly piece on a vertical?
        for move_vector in range(1, 9):
            to_square = get_to_square(king_square, (move_vector, 0))
            if self.is_on_board(to_square):
                if self.king_in_check_straight(color, to_square):
                    return True
                if getattr(self, to_square) != "empty":
                    break
        for move_vector in range(-1, -9, -1):
            to_square = get_to_square(king_square, (move_vector, 0))
            if self.is_on_board(to_square):
                if self.king_in_check_straight(color, to_square):
                    return True
                if getattr(self, to_square) != "empty":
                    break
        #  is an opposite rook/queen closer than a friendly piece on a horizontal?
        for move_vector in range(1, 9):
            to_square = get_to_square(king_square, (0, move_vector))
            if self.is_on_board(to_square):
                if self.king_in_check_straight(color, to_square):
                    return True
                if getattr(self, to_square) != "empty":
                    break
        for move_vector in range(-1, -9, -1):
            to_square = get_to_square(king_square, (0, move_vector))
            if self.is_on_board(to_square):
                if self.king_in_check_straight(color, to_square):
                    return True
                if getattr(self, to_square) != "empty" or not self.is_on_board(to_square):
                    break
        # is an opposite bishop/queen closer than a friendly piece on a diagonal?
        for move_vector in range(1, 9):
            to_square = get_to_square(king_square, (move_vector, move_vector))
            if self.is_on_board(to_square):
                if self.king_in_check_diagonal(color, to_square):
                    return True
                if getattr(self, to_square) != "empty":
                    break
        for move_vector in range(1, 9):
            to_square = get_to_square(king_square, (-move_vector, -move_vector))
            if self.is_on_board(to_square):
                if self.king_in_check_diagonal(color, to_square):
                    return True
                if getattr(self, to_square) != "empty":
                    break
        for move_vector in range(1, 9):
            to_square = get_to_square(king_square, (-move_vector, move_vector))
            if self.is_on_board(to_square):
                if self.king_in_check_diagonal(color, to_square):
                    return True
                if getattr(self, to_square) != "empty":
                    break
        for move_vector in range(1, 9):
            to_square = get_to_square(king_square, (move_vector, -move_vector))
            if self.is_on_board(to_square):
                if self.king_in_check_diagonal(color, to_square):
                    return True
                if getattr(self, to_square) != "empty":
                    break
        # is an opposite pawn one diagonal in front of the king?
        for move_vector in [(1, 1), (1, -1)]:
            to_square = get_to_square(king_square, move_vector)
            if self.is_on_board(to_square):
                if color == "white" and getattr(self, to_square) == "black pawn":
                    return True
        for move_vector in [(-1, 1), (-1, -1)]:
            to_square = get_to_square(king_square, move_vector)
            if self.is_on_board(to_square):
                if color == "black" and getattr(self, to_square) == "white pawn":
                    return True
        return False

    def get_king_square(self, color):
        king_square = "e1"
        for square in square_names:
            if getattr(self, square) == color + ' king':
                king_square = square
                break
        return king_square

    def get_white_king_square(self):
        return self.get_king_square("white")

    def get_black_king_square(self):
        return self.get_king_square("black")

    def king_in_check_straight(self, color, to_square):
        if (getattr(self, to_square) == get_opposite_color(color) + " queen"
                or getattr(self, to_square) == get_opposite_color(color) + " rook"):
            return True

    def king_in_check_diagonal(self, color, to_square):
        if (getattr(self, to_square) == get_opposite_color(color) + " queen"
                or getattr(self, to_square) == get_opposite_color(color) + " bishop"):
            return True

    @countit
    def move_is_legal(self, from_square, to_square, color_to_move):
        return (self.is_on_board(from_square) and self.is_on_board(to_square)
                and self.is_reachable(from_square, to_square, color_to_move)
                and not self.king_in_check_after_move(from_square, to_square, color_to_move))

    @countit
    def count_legal_moves(self, color):
        number_of_legal_moves = 0
        for from_square in square_names:
            if self.color_that_occupies(from_square) == color:
                for to_square in square_names:
                    if self.move_is_legal(from_square, to_square, color):
                        number_of_legal_moves += 1
        return number_of_legal_moves

    @countit
    def is_checkmated(self, color):
        return self.count_legal_moves(color) == 0 and self.king_in_check(color)

    @countit
    def is_stalemate(self, color):
        return self.count_legal_moves(color) == 0 and not self.king_in_check(color)

    #@timeit
    def move_if_legal(self, from_square, to_square, color_to_move):
        if self.move_is_legal(from_square, to_square, color_to_move):
            self.move(from_square, to_square)
            if self.move_is_white_castling_kingside(from_square, to_square):
                self.move("h1", "f1")
            if self.move_is_black_castling_kingside(from_square, to_square):
                self.move("h8", "f8")
            if self.move_is_white_castling_queenside(from_square, to_square):
                self.move("a1", "d1")
            if self.move_is_black_castling_queenside(from_square, to_square):
                self.move("a8", "d8")
            if from_square == "e1":
                self.white_king_has_moved = True
            if from_square == "e8":
                self.black_king_has_moved = True
            if from_square == "a1":
                self.a1_rook_has_moved = True
            if from_square == "h1":
                self.h1_rook_has_moved = True
            if from_square == "a8":
                self.a8_rook_has_moved = True
            if from_square == "h8":
                self.h8_rook_has_moved = True
            self.game_ends(get_opposite_color(color_to_move))

    @countit
    def move_is_white_castling_kingside(self, from_square, to_square):
        return (from_square, to_square) == ("e1", "g1") and not self.white_king_has_moved and not self.h1_rook_has_moved

    @countit
    def move_is_black_castling_kingside(self, from_square, to_square):
        return (from_square, to_square) == ("e8", "g8") and not self.black_king_has_moved and not self.h8_rook_has_moved

    @countit
    def move_is_white_castling_queenside(self, from_square, to_square):
        return (from_square, to_square) == ("e1", "c1") and not self.white_king_has_moved and not self.a1_rook_has_moved

    @countit
    def move_is_black_castling_queenside(self, from_square, to_square):
        return (from_square, to_square) == ("e8", "c8") and not self.black_king_has_moved and not self.a8_rook_has_moved

    @countit
    def move_is_castling(self, from_square, to_square, color):
        return (color == "white" and
                    (self.move_is_white_castling_kingside(from_square, to_square) or
                     self.move_is_white_castling_queenside(from_square, to_square))
                or
                color == "black" and
                    (self.move_is_black_castling_kingside(from_square, to_square) or
                     self.move_is_black_castling_queenside(from_square, to_square)))

    @countit
    def display(self):
        display_string = ""
        white_color = "\033[96m"
        black_color = "\033[94m"
        neutral_color = "\033[0m"
        for square in square_names_for_display:
            color = self.color_that_occupies(square)
            piece = self.get_kind_of_piece_on(square)
            filling = " " * (7-len(piece))
            if piece == "empty":
                display_string += "        " + neutral_color + "|"
            elif color == "white":
                display_string += white_color + " " + piece + filling + neutral_color + "|"
            elif color == "black":
                display_string += black_color + " " + piece + filling + neutral_color + "|"
            if square.startswith("h") and not square.endswith("1"):
                display_string += "\n"
        return display_string

    @countit
    def game_ends(self, color):
        if self.is_checkmated(color):
            self.game_ended = True
            self.result = get_opposite_color(color) + " wins"
        if self.is_stalemate(color):
            self.game_ended = True
            self.result = "draw (stalemate)"
