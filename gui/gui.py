from tkinter import Tk, Label, Entry, Button, PhotoImage, Canvas
from src.Chess2 import Board
from src.game_setup import square_names
import os


def render_on_start():
    col_dict = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
    for i in range(8):
        board_canvas.create_text(space_for_enumeration // 2, square_size // 2 + i * square_size,
                                 text=str(8 - i))
        board_canvas.create_text(space_for_enumeration + square_size // 2 + i * square_size,
                                 space_for_enumeration // 2 + square_size * 8,
                                 text=col_dict[i + 1])
    render_board()


def render_board():
    for i, sq_name in enumerate(square_names):
        row_local = i % 8
        col_local = i // 8
        if (sq_name == board.get_white_king_square() and board.white_king_in_check()
                or sq_name == board.get_black_king_square() and board.black_king_in_check()):
            bg_color = check_color
        elif row_local % 2 == 0 and col_local % 2 == 0 or row_local % 2 == 1 and col_local % 2 == 1:
            bg_color = dark_color
        else:
            bg_color = light_color
        x_pos = (i//8)*square_size+space_for_enumeration
        y_pos = ((7-i) % 8)*square_size
        board_canvas.create_rectangle((i//8)*square_size+space_for_enumeration,
                                      ((7-i) % 8)*square_size,
                                      ((i//8)+1)*square_size+space_for_enumeration,
                                      (((7-i) % 8)+1)*square_size,
                                      fill=bg_color, width=0)
        render_piece(sq_name, x_pos, y_pos)
    if board.game_ended:
        board_canvas.create_rectangle(2.5*square_size+space_for_enumeration,
                                      3.5*square_size,
                                      5.5*square_size+space_for_enumeration,
                                      4.5*square_size, fill=accent_color, width=0)
        board_canvas.create_text(4*square_size+space_for_enumeration,
                                 4*square_size, text=board.result)


def render_piece(sq_name, x_pos, y_pos):
    piece_on_square = getattr(board, sq_name)
    piece_img = PhotoImage(file=os.path.join(img_folder, piece_on_square + '.png'))
    setattr(main_window, sq_name, piece_img)
    board_canvas.create_image(x_pos, y_pos, anchor="nw", image=piece_img)


def get_square_from_coord(x, y):
    for i, sq_name in enumerate(square_names):
        if ((i//8)*square_size+space_for_enumeration < x < ((i//8)+1)*square_size+space_for_enumeration
                and ((7-i) % 8)*square_size < y < (((7-i) % 8)+1)*square_size):
            return sq_name
    return None


def switch_turn(color):
    if color == "white":
        return "black"
    else:
        return "white"


def make_move():
    global color_to_move
    from_square = clicker.move_from
    to_square = clicker.move_to
    if board.move_is_legal(from_square, to_square, color_to_move):
        board.move_if_legal(from_square, to_square, color_to_move)
        color_to_move = switch_turn(color_to_move)
    render_board()


class Clicker:

    def __init__(self):
        self.move_from = None
        self.move_to = None
        self.prev_square = None
        self.square = None

    def on_grab(self, event):
        self.move_from = get_square_from_coord(event.x, event.y)

    def on_drag(self, event):
        if self.move_from:
            setattr(main_window, self.move_from, empty_img)
            piece_on_square = getattr(board, self.move_from)
            piece_img = PhotoImage(file=os.path.join(img_folder, piece_on_square + '.png'))
            board_canvas.create_image(event.x, event.y, image=piece_img)
            setattr(main_window, "floating", piece_img)

    def on_drop(self, event):
        self.move_to = get_square_from_coord(event.x, event.y)
        if self.move_from and self.move_to:
            make_move()
        else:
            render_board()
            delattr(main_window, "floating")

    def coloring(self, event):
        if not board.game_ended:
            self.prev_square = self.square
            self.square = get_square_from_coord(event.x, event.y)
            self.on_enter()
            self.on_leave()

    def on_enter(self):
        if self.square in square_names:
            i = square_names.index(self.square)
            board_canvas.create_rectangle((i // 8) * square_size + space_for_enumeration,
                                          ((7 - i) % 8) * square_size,
                                          ((i // 8) + 1) * square_size + space_for_enumeration,
                                          (((7 - i) % 8) + 1) * square_size,
                                          fill=accent_color, width=0)
            x_pos = (i // 8) * square_size + space_for_enumeration
            y_pos = ((7 - i) % 8) * square_size
            render_piece(self.square, x_pos, y_pos)

    def on_leave(self):
        if self.prev_square in square_names and self.square != self.prev_square:
            i = square_names.index(self.prev_square)
            row_local = i % 8
            col_local = i // 8
            if row_local % 2 == 0 and col_local % 2 == 0 or row_local % 2 == 1 and col_local % 2 == 1:
                bg_color = dark_color
            else:
                bg_color = light_color
            board_canvas.create_rectangle((i // 8) * square_size + space_for_enumeration,
                                          ((7 - i) % 8) * square_size,
                                          ((i // 8) + 1) * square_size + space_for_enumeration,
                                          (((7 - i) % 8) + 1) * square_size,
                                          fill=bg_color, width=0)
            x_pos = (i // 8) * square_size + space_for_enumeration
            y_pos = ((7 - i) % 8) * square_size
            render_piece(self.prev_square, x_pos, y_pos)


if __name__ == '__main__':
    img_folder = os.path.join("..", "pieces_img")
    light_color = "#DDDDDD"
    dark_color = "#BBBBBB"
    accent_color = "#95A5C9"
    check_color = "#DF7F78"
    dark_squares = []
    light_squares = []
    space_for_enumeration = 30
    square_size = 45

    for idx, square_name in enumerate(square_names):
        row = idx % 8
        col = idx // 8
        if row % 2 == 0 and col % 2 == 0 or row % 2 == 1 and col % 2 == 1:
            dark_squares.append(square_name)
        else:
            light_squares.append(square_name)

    main_window = Tk()

    empty_img = PhotoImage(file=os.path.join(img_folder, 'empty.png'))

    board = Board()
    color_to_move = "white"

    board_canvas = Canvas(main_window, width=8*square_size+space_for_enumeration,
                          height=8*square_size+space_for_enumeration, name="chess_board")
    board_canvas.pack()
    render_on_start()

    clicker = Clicker()

    board_canvas.bind('<Button-1>', clicker.on_grab)
    board_canvas.bind('<B1-Motion>', clicker.on_drag)
    board_canvas.bind('<ButtonRelease-1>', clicker.on_drop)
    board_canvas.bind('<Motion>', clicker.coloring)

    main_window.mainloop()
