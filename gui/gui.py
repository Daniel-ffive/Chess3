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
        if row_local % 2 == 0 and col_local % 2 == 0 or row_local % 2 == 1 and col_local % 2 == 1:
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


if __name__ == '__main__':
    img_folder = os.path.join("..", "pieces_img")
    light_color = "#FFF3D6"
    dark_color = "#C9BA95"
    accent_color = "#95A5C9"
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

    main_window.mainloop()
