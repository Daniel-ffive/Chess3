col_dict = {"a": 1, "b": 2, "c": 3, "d": 4,
            "e": 5, "f": 6, "g": 7, "h": 8}
rev_col_dict = {1: "a", 2: "b", 3: "c", 4: "d",
                5: "e", 6: "f", 7: "g", 8: "h"}
knight_move_vectors = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]


def reverse_dict(dictionary):
    return {dictionary[key]: key for key in dictionary.keys()}


def move_is_vertical(from_square, to_square):
    return from_square[0] == to_square[0]


def move_is_horizontal(from_square, to_square):
    return from_square[1] == to_square[1]


def move_is_diagonal(from_square, to_square):
    return get_distance_between_rows(from_square, to_square) == get_distance_between_columns(from_square, to_square)


def get_distance_between_columns(from_square, to_square):
    return abs(col_dict[to_square[0]] - col_dict[from_square[0]])


def get_move_length(from_square, to_square):
    if move_is_horizontal(from_square, to_square):
        return get_distance_between_columns(from_square, to_square)
    else:
        return get_distance_between_rows(from_square, to_square)


def get_distance_between_rows(from_square, to_square):
    return abs(int(to_square[1]) - int(from_square[1]))


def move_is_knightmove(from_square, to_square):
    return (get_move_vector(from_square, to_square) == (2, 1)
            or get_move_vector(from_square, to_square) == (1, 2))


def get_move_vector(from_square, to_square):
    return (get_distance_between_rows(from_square, to_square),
            get_distance_between_columns(from_square, to_square))


def get_to_square(from_square, move_vector):
    try:
        to_square = (rev_col_dict[col_dict[from_square[0]] + move_vector[1]] +
                     str(int(from_square[1]) + move_vector[0]))
    except KeyError:
        to_square = "x0"
    return to_square


def get_squares_in_between(from_square, to_square):
    if move_is_vertical(from_square, to_square):
        return get_squares_in_between_vertical(from_square, to_square)
    if move_is_horizontal(from_square, to_square):
        return get_squares_in_between_horizontal(from_square, to_square)
    if move_is_diagonal(from_square, to_square):
        return get_squares_in_between_diagonal(from_square, to_square)
    else:
        return set()


def get_squares_in_between_vertical(from_square, to_square):
    counter = min(int(from_square[1]), int(to_square[1])) + 1
    squares_in_between = set()
    while counter < max(int(from_square[1]), int(to_square[1])):
        squares_in_between.add(from_square[0] + str(counter))
        counter += 1
    return squares_in_between


def get_squares_in_between_horizontal(from_square, to_square):
    counter = min(col_dict[from_square[0]], col_dict[to_square[0]]) + 1
    squares_in_between = set()
    while counter < max(col_dict[from_square[0]], col_dict[to_square[0]]):
        squares_in_between.add(reverse_dict(col_dict)[counter] + from_square[1])
        counter += 1
    return squares_in_between


def get_squares_in_between_diagonal(from_square, to_square):
    if col_dict[from_square[0]] < col_dict[to_square[0]] and int(from_square[1]) < int(to_square[1]):
        col_operator = '+'
        row_operator = '+'
    if col_dict[from_square[0]] > col_dict[to_square[0]] and int(from_square[1]) < int(to_square[1]):
        col_operator = '-'
        row_operator = '+'
    if col_dict[from_square[0]] > col_dict[to_square[0]] and int(from_square[1]) > int(to_square[1]):
        col_operator = '-'
        row_operator = '-'
    if col_dict[from_square[0]] < col_dict[to_square[0]] and int(from_square[1]) > int(to_square[1]):
        col_operator = '+'
        row_operator = '-'
    squares_in_between = set()
    counter_col = add_or_subtract_one(col_dict[from_square[0]], col_operator)
    counter_row = add_or_subtract_one(int(from_square[1]), row_operator)
    while counter_col != col_dict[to_square[0]]:
        squares_in_between.add(reverse_dict(col_dict)[counter_col] + str(counter_row))
        counter_col = add_or_subtract_one(counter_col, col_operator)
        counter_row = add_or_subtract_one(counter_row, row_operator)
    return squares_in_between


def sign(number):
    if number < 0:
        return -1
    if number >= 0:
        return 1


def move_is_rookmove(from_square, to_square):
    if move_is_vertical(from_square, to_square):
        return True
    if move_is_horizontal(from_square, to_square):
        return True
    return False


def move_is_queenmove(from_square, to_square):
    if move_is_vertical(from_square, to_square):
        return True
    if move_is_horizontal(from_square, to_square):
        return True
    if move_is_diagonal(from_square, to_square):
        return True
    return False


def move_is_kingmove(from_square, to_square):
    if move_is_vertical(from_square, to_square):
        if get_distance_between_rows(from_square, to_square) == 1:
            return True
    if move_is_horizontal(from_square, to_square):
        if get_distance_between_columns(from_square, to_square) == 1:
            return True
    if move_is_diagonal(from_square, to_square):
        if get_distance_between_rows(from_square, to_square) == 1:
            return True
    return False


def get_opposite_color(color):
    if color == "white":
        return "black"
    if color == "black":
        return "white"


def add_or_subtract_one(a, operator):
    if operator == "+":
        return a + 1
    if operator == "-":
        return a - 1
