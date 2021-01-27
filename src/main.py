from src.Chess2 import Board

board = Board()
color_to_move = "white"


def switch_turn(color):
    if color == "white":
        return "black"
    else:
        return "white"


print(board.display())
while not board.game_ended:

    move = input("Enter move in the form <from_square>,<to_square>:")
    from_square = move.split(",")[0]
    to_square = move.split(",")[1]
    if board.move_is_legal(from_square, to_square, color_to_move):
        board.move_if_legal(from_square, to_square, color_to_move)
        color_to_move = switch_turn(color_to_move)
        print("")
        print(board.display())
    else:
        print("illegal move!")
else:
    print(board.result)
