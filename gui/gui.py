from tkinter import Tk, Label, Entry, Button, PhotoImage
from src.Chess2 import Board
from src.game_setup import square_names
import os

img_folder = os.path.join("..", "pieces_img")

light_color = "#FFF3D6"
dark_color = "#C9BA95"
accent_color = "#95A5C9"
dark_squares = []
light_squares = []
for idx, square_name in enumerate(square_names):
    row = idx % 8
    col = idx // 8
    if row % 2 == 0 and col % 2 == 0 or row % 2 == 1 and col % 2 == 1:
        dark_squares.append(square_name)
    else:
        light_squares.append(square_name)


def switch_turn(color):
    if color == "white":
        return "black"
    else:
        return "white"


def render_piece(tk_square, sq_name):
    piece_on_square = getattr(board, sq_name)
    piece_img = PhotoImage(file=os.path.join(img_folder, piece_on_square + '.png'))
    tk_square.config(image=piece_img, cursor="hand2")
    tk_square.image = piece_img


def render_board():
    for i, sq_name in enumerate(square_names):
        row_local = i % 8
        col_local = i // 8
        if row_local % 2 == 0 and col_local % 2 == 0 or row_local % 2 == 1 and col_local % 2 == 1:
            bg_color = dark_color
        else:
            bg_color = light_color
        tk_squares_dict[sq_name] = Label(main_window, bg=bg_color, name=sq_name)
        tk_squares_dict[sq_name].grid(column=col_local+1, row=7 - row_local)
        tk_squares_dict[sq_name].bind('<Button-1>', enter_square_by_clicking)
        render_piece(tk_squares_dict[sq_name], sq_name)


def make_move():
    global color_to_move
    from_square = move_from_entry.get()
    move_from_entry.delete(0, len(from_square))
    to_square = move_to_entry.get()
    move_to_entry.delete(0, len(to_square))
    if board.move_is_legal(from_square, to_square, color_to_move):
        board.move_if_legal(from_square, to_square, color_to_move)
        render_board()
        color_to_move = switch_turn(color_to_move)
        message.config(text="")
        move_label.config(text=f"{color_to_move}, please enter your move:")
    else:
        message.config(text="illegal move, try again!")
        render_board()
    if board.game_ended:
        message.config(text=board.result)
        render_board()


def enter_square_by_clicking(event):
    widget_name = str(event.widget)[1:]
    move_from = move_from_entry.get()
    if len(move_from) == 0:
        move_from_entry.insert(0, widget_name)
        event.widget.config(bg=accent_color)
    elif len(move_from) == 2:
        if move_from == widget_name:
            move_from_entry.delete(0, 2)
            if widget_name in dark_squares:
                event.widget.config(bg=dark_color)
            if widget_name in light_squares:
                event.widget.config(bg=light_color)
        else:
            move_to_entry.insert(0, widget_name)
            make_move()


def reset_game():
    global board
    board = Board()
    global color_to_move
    color_to_move = "white"
    render_board()
    message.config(text="")
    global move_label
    move_label.config(text="white, please enter your move:")


if __name__ == '__main__':
    board = Board()
    color_to_move = "white"
    main_window = Tk()
    tk_squares_dict = dict()
    tk_buttons_dict = dict()
    render_board()
    col_dict = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
    for idx in range(8):
        Label(main_window, text=str(idx+1)).grid(column=0, row=7-idx)
        Label(main_window, text=col_dict[idx+1]).grid(column=idx+1, row=8)

    move_label = Label(main_window, text=f"{color_to_move}, please enter your move:")
    move_label.grid(column=9, row=3, columnspan=2)
    move_from_label = Label(main_window, text="from square:")
    move_from_label.grid(column=9, row=4)
    move_to_label = Label(main_window, text="to square:")
    move_to_label.grid(column=10, row=4)
    move_from_entry = Entry(main_window, width=3)
    move_from_entry.grid(column=9, row=5)
    move_to_entry = Entry(main_window, width=3)
    move_to_entry.grid(column=10, row=5)
    Button(main_window, text='confirm move', command=make_move).grid(column=9, row=6, columnspan=2)
    message = Label(main_window)
    message.grid(column=9, row=7, columnspan=2)
    Button(main_window, text='reset game', command=reset_game).grid(column=9, row=8, columnspan=2)

    main_window.mainloop()
