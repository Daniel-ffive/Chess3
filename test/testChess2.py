import unittest

from src.Chess2 import Board
from src.moving import move_is_vertical, move_is_horizontal, move_is_diagonal, get_distance_between_columns, \
    get_move_length, move_is_knightmove, get_move_vector, get_squares_in_between_vertical, get_squares_in_between, \
    get_squares_in_between_horizontal, reverse_dict, get_squares_in_between_diagonal, sign, get_opposite_color, \
    add_or_subtract_one
from src.game_setup import square_names


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_boardCorrectlySetUp_AfterInit(self):
        self.assertEqual("white rook", self.board.a1)
        self.assertEqual("white rook", self.board.h1)
        self.assertEqual("white knight", self.board.b1)
        self.assertEqual("white knight", self.board.g1)
        self.assertEqual("white bishop", self.board.c1)
        self.assertEqual("white bishop", self.board.f1)
        self.assertEqual("white queen", self.board.d1)
        self.assertEqual("white king", self.board.e1)
        self.assertEqual("white pawn", self.board.a2)
        self.assertEqual("white pawn", self.board.b2)
        self.assertEqual("white pawn", self.board.c2)
        self.assertEqual("white pawn", self.board.d2)
        self.assertEqual("white pawn", self.board.e2)
        self.assertEqual("white pawn", self.board.f2)
        self.assertEqual("white pawn", self.board.g2)
        self.assertEqual("white pawn", self.board.h2)
        self.assertEqual("black rook", self.board.a8)
        self.assertEqual("black rook", self.board.h8)
        self.assertEqual("black knight", self.board.b8)
        self.assertEqual("black knight", self.board.g8)
        self.assertEqual("black bishop", self.board.c8)
        self.assertEqual("black bishop", self.board.f8)
        self.assertEqual("black queen", self.board.d8)
        self.assertEqual("black king", self.board.e8)
        self.assertEqual("black pawn", self.board.a7)
        self.assertEqual("black pawn", self.board.b7)
        self.assertEqual("black pawn", self.board.c7)
        self.assertEqual("black pawn", self.board.d7)
        self.assertEqual("black pawn", self.board.e7)
        self.assertEqual("black pawn", self.board.f7)
        self.assertEqual("black pawn", self.board.g7)
        self.assertEqual("black pawn", self.board.h7)

    def test_pieceXonSquareY_AfterPut(self):
        self.board.put("whitePawn", "e4")
        self.assertEqual("whitePawn", self.board.e4)
        self.board.put("blackPawn", "e5")
        self.assertEqual("blackPawn", self.board.e5)

    def test_squareEmpty_AfterFreeSquare(self):
        self.board.free_square("e2")
        self.assertEqual("empty", self.board.e2)

    def test_isSquareOccupied(self):
        self.board.is_occupied("e2")
        self.assertTrue(self.board.is_occupied("e2"))

    def test_squareOccupiedByColor(self):
        self.assertEqual("white", self.board.color_that_occupies("e2"))
        self.assertEqual("black", self.board.color_that_occupies("e7"))
        self.assertEqual("empty", self.board.color_that_occupies("e3"))

    def test_isMoveFromXtoYVertical(self):
        self.assertTrue(move_is_vertical("e2", "e4"))
        self.assertFalse(move_is_vertical("e2", "h2"))
        self.assertFalse(move_is_vertical("e2", "f4"))

    def test_isMoveFromXtoYHorizontal(self):
        self.assertFalse(move_is_horizontal("e2", "e4"))
        self.assertTrue(move_is_horizontal("e2", "h2"))
        self.assertFalse(move_is_horizontal("e2", "f4"))

    def test_isMoveFromXtoYDiagonal(self):
        self.assertFalse(move_is_diagonal("e2", "e4"))
        self.assertFalse(move_is_diagonal("e2", "h2"))
        self.assertFalse(move_is_diagonal("e2", "f4"))
        self.assertTrue(move_is_diagonal("e2", "g4"))

    def test_getDistanceBetweenColumns(self):
        self.assertEqual(5, get_distance_between_columns("a2", "f4"))
        self.assertEqual(1, get_distance_between_columns("b2", "a4"))

    def test_moveFromXtoY(self):
        self.board.move("e2", "e4")
        self.assertEqual("empty", self.board.e2)
        self.assertEqual("white pawn", self.board.e4)

    def test_getMoveLength(self):
        self.assertEqual(4, get_move_length("a2", "a6"))
        self.assertEqual(6, get_move_length("b2", "h8"))
        self.assertEqual(2, get_move_length("f6", "h6"))

    def test_isMoveFromXtoYaKnightMove(self):
        self.assertTrue(move_is_knightmove("e2", "f4"))
        self.assertTrue(move_is_knightmove("e2", "g3"))
        self.assertFalse(move_is_knightmove("e2", "g4"))

    def test_getMoveVector(self):
        self.assertEqual((2, 1), get_move_vector("e2", "f4"))

    def test_squareOnBoard(self):
        self.assertTrue(self.board.is_on_board("e2"))
        self.assertFalse(self.board.is_on_board("t7"))

    def test_pathClear(self):
        self.assertTrue(self.board.path_is_clear("a2", "a7"))
        self.assertFalse(self.board.path_is_clear("a2", "a8"))
        self.assertTrue(self.board.path_is_clear("a3", "h3"))
        self.assertFalse(self.board.path_is_clear("a1", "e1"))
        self.assertTrue(self.board.path_is_clear("a2", "f7"))
        self.assertFalse(self.board.path_is_clear("a2", "g8"))

    def test_getSquaresBetween(self):
        self.assertSetEqual({"a3", "a4", "a5", "a6"},
                            get_squares_in_between("a2", "a7"))
        self.assertSetEqual({"b3", "c3", "d3"},
                            get_squares_in_between("a3", "e3"))
        self.assertSetEqual({"b3", "c4"},
                            get_squares_in_between("a2", "d5"))

    def test_getSquaresBetweenVertical(self):
        self.assertSetEqual({"a3", "a4", "a5", "a6"},
                            get_squares_in_between_vertical("a2", "a7"))
        self.assertSetEqual({"a3", "a4", "a5", "a6"},
                            get_squares_in_between_vertical("a7", "a2"))

    def test_getSquaresBetweenHorizontal(self):
        self.assertSetEqual({"b3", "c3", "d3"},
                            get_squares_in_between_horizontal("a3", "e3"))
        self.assertSetEqual({"b3", "c3", "d3"},
                            get_squares_in_between_horizontal("e3", "a3"))

    def test_reverseDict(self):
        self.assertDictEqual({1: "a", 2: "b"}, reverse_dict({"a": 1, "b": 2}))

    def test_getSquaresBetweenDiagonal(self):
        self.assertSetEqual({"b3", "c4"},
                            get_squares_in_between_diagonal("a2", "d5"))
        self.assertSetEqual({"c4", "b3"},
                            get_squares_in_between_diagonal("d5", "a2"))
        self.assertSetEqual({"e2", "d3"},
                            get_squares_in_between_diagonal("f1", "c4"))
        self.assertSetEqual({"d3", "e2"},
                            get_squares_in_between_diagonal("c4", "f1"))

    def test_whichKindOfPieceOnSquare(self):
        self.assertEqual("bishop", self.board.get_kind_of_piece_on("c1"))
        self.assertEqual("queen", self.board.get_kind_of_piece_on("d1"))

    def test_pieceCannotMoveFromEmptySquare(self):
        self.assertFalse(self.board.is_reachable("d4", "d5", "white"))

    def test_pieceCannotJumpOverOtherPiece_ExceptKnight(self):
        self.board.put("white pawn", "e3")
        self.board.put("black pawn", "d3")
        self.assertFalse(self.board.is_reachable("e2", "e4", "white"))
        self.assertFalse(self.board.is_reachable("d2", "d4", "white"))
        self.assertFalse(self.board.is_reachable("a1", "a4", "white"))

    def test_squareOccupiedByOppColor(self):
        self.assertTrue(self.board.square_is_occupied_by_own_color("white", "e2"))

    def testSign(self):
        self.assertEqual(-1, sign(-4))
        self.assertEqual(1, sign(4))

    def test_PawnOnInitialSquare(self):
        self.assertTrue(self.board.pawn_is_on_initial_square("e2"))
        self.assertTrue(self.board.pawn_is_on_initial_square("e7"))
        self.assertFalse(self.board.pawn_is_on_initial_square("g3"))
        self.assertFalse(self.board.pawn_is_on_initial_square("a5"))

    def test_isCorrectColorMoved(self):
        self.assertTrue(self.board.correct_color_is_moved("e2", "white"))
        self.assertFalse(self.board.correct_color_is_moved("e2", "black"))

    def test_pieceCannotMoveOnSquareOccupiedByPieceOfSameColor(self):
        self.assertFalse(self.board.is_reachable("e1", "e2", "white"))
        self.assertFalse(self.board.is_reachable("c1", "b2", "white"))

    def test_undoLastMove(self):
        self.board.move("e2", "e4")
        self.board.undo_last_move()
        self.assertTrue(self.board.is_occupied("e2"))
        self.assertFalse(self.board.is_occupied("e4"))

    def test_undoLastMoveWithCapture(self):
        self.board.move("e2", "e4")
        self.board.move("d7", "d5")
        self.board.move("e4", "d5")
        self.board.undo_last_move()
        self.assertEqual("black pawn", self.board.d5)
        self.assertEqual("white pawn", self.board.e4)

    def test_getOppColor(self):
        self.assertEqual("white", get_opposite_color("black"))
        self.assertEqual("black", get_opposite_color("white"))

    def test_addOrSubtractOne(self):
        self.assertEqual(2, add_or_subtract_one(1, '+'))
        self.assertEqual(4, add_or_subtract_one(5, '-'))

    @unittest.skip
    def test_displayBoard(self):
        output = self.board.display()
        white_color = "\033[96m"
        black_color = "\033[94m"
        neutral_color = "\033[0m"
        expected_output = ("-" * 9 * 8 + "\n" + (" " * 8 + "|") * 8 + "\n" +
                           black_color + " rook   " + neutral_color + "|" + black_color + " knight " + neutral_color + "|" +
                           black_color + " bishop " + neutral_color + "|" + black_color + " queen  " + neutral_color + "|" +
                           black_color + " king   " + neutral_color + "|" + black_color + " bishop " + neutral_color + "|" +
                           black_color + " knight " + neutral_color + "|" + black_color + " rook   " + neutral_color + "|" +
                           "\n" + (" " * 8 + "|") * 8 + "\n" + "-" * 9 * 8 + "\n" + (" " * 8 + "|") * 8 + "\n" +
                           black_color + " pawn   " + neutral_color + "|" + black_color + " pawn   " + neutral_color + "|" +
                           black_color + " pawn   " + neutral_color + "|" + black_color + " pawn   " + neutral_color + "|" +
                           black_color + " pawn   " + neutral_color + "|" + black_color + " pawn   " + neutral_color + "|" +
                           black_color + " pawn   " + neutral_color + "|" + black_color + " pawn   " + neutral_color + "|" +
                           "\n" + (" " * 8 + "|") * 8 + "\n" + "-" * 9 * 8 + "\n" + (" " * 8 + "|") * 8 + "\n" +
                           "        " + neutral_color + "|" + "        " + neutral_color + "|" + "        " + neutral_color + "|" + "        " + neutral_color + "|" +
                           "        " + neutral_color + "|" + "        " + neutral_color + "|" + "        " + neutral_color + "|" + "        " + neutral_color + "|" +
                           "\n" + (" " * 8 + "|") * 8 + "\n" + "-" * 9 * 8 + "\n" + (" " * 8 + "|") * 8 + "\n" +
                           "        " + neutral_color + "|" + "        " + neutral_color + "|" + "        " + neutral_color + "|" + "        " + neutral_color + "|" +
                           "        " + neutral_color + "|" + "        " + neutral_color + "|" + "        " + neutral_color + "|" + "        " + neutral_color + "|" +
                           "\n" + (" " * 8 + "|") * 8 + "\n" + "-" * 9 * 8 + "\n" + (" " * 8 + "|") * 8 + "\n" +
                           "        " + neutral_color + "|" + "        " + neutral_color + "|" + "        " + neutral_color + "|" + "        " + neutral_color + "|" +
                           "        " + neutral_color + "|" + "        " + neutral_color + "|" + "        " + neutral_color + "|" + "        " + neutral_color + "|" +
                           "\n" + (" " * 8 + "|") * 8 + "\n" + "-" * 9 * 8 + "\n" + (" " * 8 + "|") * 8 + "\n" +
                           "        " + neutral_color + "|" + "        " + neutral_color + "|" + "        " + neutral_color + "|" + "        " + neutral_color + "|" +
                           "        " + neutral_color + "|" + "        " + neutral_color + "|" + "        " + neutral_color + "|" + "        " + neutral_color + "|" +
                           "\n" + (" " * 8 + "|") * 8 + "\n" + "-" * 9 * 8 + "\n" + (" " * 8 + "|") * 8 + "\n" +
                           white_color + " pawn   " + neutral_color + "|" + white_color + " pawn   " + neutral_color + "|" +
                           white_color + " pawn   " + neutral_color + "|" + white_color + " pawn   " + neutral_color + "|" +
                           white_color + " pawn   " + neutral_color + "|" + white_color + " pawn   " + neutral_color + "|" +
                           white_color + " pawn   " + neutral_color + "|" + white_color + " pawn   " + neutral_color + "|" +
                           "\n" + (" " * 8 + "|") * 8 + "\n" + "-" * 9 * 8 + "\n" + (" " * 8 + "|") * 8 + "\n" +
                           white_color + " rook   " + neutral_color + "|" + white_color + " knight " + neutral_color + "|" +
                           white_color + " bishop " + neutral_color + "|" + white_color + " queen  " + neutral_color + "|" +
                           white_color + " king   " + neutral_color + "|" + white_color + " bishop " + neutral_color + "|" +
                           white_color + " knight " + neutral_color + "|" + white_color + " rook   " + neutral_color + "|" +
                           "\n" + (" " * 8 + "|") * 8 + "\n" + "-" * 9 * 8 )
        print(expected_output)
        self.assertEqual(expected_output, output)


class TestPawnMovement(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_pawnCanMoveOneOrTwoSteps(self):
        self.assertTrue(self.board.is_reachable("e2", "e4", "white"))
        self.assertTrue(self.board.is_reachable("e2", "e3", "white"))
        self.assertTrue(self.board.is_reachable("e7", "e5", "black"))
        self.assertTrue(self.board.is_reachable("e7", "e6", "black"))

    def test_pawnCanCaptureOppPieceOneStepDiagonally(self):
        self.board.move("e2", "e4")
        self.board.move("d7", "d5")
        self.assertTrue(self.board.is_reachable("e4", "d5", "white"))
        self.assertTrue(self.board.is_reachable("d5", "e4", "black"))

    def test_pawnCannotCaptureEmptySquare(self):
        self.board.move("d2", "d3")
        self.assertFalse(self.board.is_reachable("d3", "c4", "white"))

    def test_pawnCannotCaptureOwnPiece(self):
        self.board.move("d2", "d3")
        self.assertFalse(self.board.is_reachable("d3", "e4", "white"))

    def test_pawnCannotCaptureMovingStraight(self):
        self.board.put("white pawn", "e4")
        self.board.put("black pawn", "e5")
        self.assertFalse(self.board.pawn_move_is_legal("e4", "e5"))


class TestRookMovement(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.put("white rook", "a3")
        self.board.put("black rook", "h6")

    def test_rookCanMoveVerticallyUnlimited(self):
        self.assertTrue(self.board.is_reachable("a3", "a6", "white"))
        self.assertTrue(self.board.is_reachable("h6", "h3", "black"))

    def test_rookCanMoveHorizontallyUnlimited(self):
        self.assertTrue(self.board.is_reachable("a3", "h3", "white"))
        self.assertTrue(self.board.is_reachable("h6", "a6", "black"))

    def test_rookCanCaptureOppPieces(self):
        self.assertTrue(self.board.is_reachable("a3", "a7", "white"))
        self.assertTrue(self.board.is_reachable("h6", "h2", "black"))

    def test_rookCannotJumpOverPieces(self):
        self.assertFalse(self.board.is_reachable("a3", "a8", "white"))
        self.assertFalse(self.board.is_reachable("h6", "h1", "black"))

    def test_rookCannotMoveDiagonally(self):
        self.assertFalse(self.board.is_reachable("a3", "d6", "white"))
        self.assertFalse(self.board.is_reachable("h6", "e3", "black"))


class TestBishopMovement(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.put("white bishop", "a3")
        self.board.put("black bishop", "a6")

    def test_bishopCanMoveDiagonallyUnlimited(self):
        self.assertTrue(self.board.is_reachable("a3", "d6", "white"))
        self.assertTrue(self.board.is_reachable("a6", "d3", "black"))

    def test_bishopCanCaptureOppPieces(self):
        self.assertTrue(self.board.is_reachable("a3", "e7", "white"))
        self.assertTrue(self.board.is_reachable("a6", "e2", "black"))

    def test_bishopCannotJumpOverPieces(self):
        self.assertFalse(self.board.is_reachable("a3", "f8", "white"))
        self.assertFalse(self.board.is_reachable("a6", "f1", "black"))

    def test_bishopCannotDoKnightMove(self):
        self.assertFalse(self.board.is_reachable("a3", "b5", "white"))

    def test_bishopCanMoveFromInitialPos(self):
        self.board = Board()
        self.board.move("e2", "e3")
        self.assertTrue(self.board.is_reachable("f1", "c4", "white"))


class TestKnightMovement(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.put("white knight", "e5")
        self.board.put("black knight", "d3")

    def test_knightCanMoveTwoVertOneHorizontal(self):
        self.assertTrue(self.board.is_reachable("e5", "f3", "white"))
        self.assertTrue(self.board.is_reachable("d3", "c5", "black"))

    def test_knightCanMoveOneVertTwoHorizontal(self):
        self.assertTrue(self.board.is_reachable("e5", "g4", "white"))
        self.assertTrue(self.board.is_reachable("d3", "b4", "black"))

    def test_knightCannotMoveDiagonally(self):
        self.assertFalse(self.board.is_reachable("e5", "g3", "white"))

    def test_knightCanJumpOverPieces(self):
        self.assertTrue(self.board.is_reachable("g1", "f3", "white"))
        self.assertTrue(self.board.is_reachable("g8", "f6", "black"))

    def test_knightCannotJumpOnSquareOccupiedByOwnColor(self):
        self.assertFalse(self.board.is_reachable("g1", "e2", "white"))
        self.assertFalse(self.board.is_reachable("g8", "e7", "black"))

    def test_knightCanCapture(self):
        self.assertTrue(self.board.is_reachable("e5", "d3", "white"))
        self.assertTrue(self.board.is_reachable("d3", "e5", "black"))


class TestQueenMovement(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.put("white queen", "a3")
        self.board.put("black queen", "h6")

    def test_queenCanMoveDiagonally(self):
        self.assertTrue(self.board.is_reachable("a3", "d6", "white"))
        self.assertTrue(self.board.is_reachable("h6", "e3", "black"))

    def test_queenCanMoveVertically(self):
        self.assertTrue(self.board.is_reachable("a3", "a6", "white"))
        self.assertTrue(self.board.is_reachable("h6", "h3", "black"))

    def test_queenCanMoveHorizontally(self):
        self.assertTrue(self.board.is_reachable("a3", "h3", "white"))
        self.assertTrue(self.board.is_reachable("h6", "a6", "black"))

    def test_queenCanCaptureOppPieces(self):
        self.assertTrue(self.board.is_reachable("a3", "e7", "white"))
        self.assertTrue(self.board.is_reachable("h6", "d2", "black"))

    def test_queenCannotJumpOverPieces(self):
        self.assertFalse(self.board.is_reachable("a3", "f8", "white"))
        self.assertFalse(self.board.is_reachable("h6", "c1", "black"))

    def test_queenCannotDoKnightmove(self):
        self.assertFalse(self.board.is_reachable("a3", "b5", "white"))


class TestKingMovement(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.put("white king", "a3")
        self.board.put("black king", "h6")

    def test_kingCanMoveOneVertically(self):
        self.assertTrue(self.board.is_reachable("a3", "a4", "white"))
        self.assertTrue(self.board.is_reachable("h6", "h5", "black"))

    def test_kingCanMoveOneHorizontally(self):
        self.assertTrue(self.board.is_reachable("a3", "b3", "white"))
        self.assertTrue(self.board.is_reachable("h6", "g6", "black"))

    def test_kingCanMoveOneDiagonally(self):
        self.assertTrue(self.board.is_reachable("a3", "b4", "white"))
        self.assertTrue(self.board.is_reachable("h6", "g5", "black"))

    def test_kingCannotMoveOffBoard(self):
        self.assertFalse(self.board.is_reachable("h6", "i6", "black"))


class TestKingInCheck(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.put("white king", "a3")
        self.board.put("black king", "h6")
        self.board.free_square("e1")
        self.board.free_square("e8")

    def test_kingInCheck_ifMovedIntoCheck(self):
        self.board.put("white rook", "a5")
        self.board.put("black rook", "h4")
        self.assertTrue(self.board.king_in_check_after_move("a3", "a4", "white"))
        self.assertTrue(self.board.king_in_check_after_move("h6", "h5", "black"))

    def test_moveIllegal_ifKingInCheck_afterMove(self):
        self.board.put("white rook", "a5")
        self.board.put("black rook", "h4")
        self.assertFalse(self.board.move_is_legal("a3", "a4", "white"))
        self.assertFalse(self.board.move_is_legal("h6", "h5", "black"))

    def test_getAllReachableToSquaresFromSquareX(self):
        self.assertSetEqual({"e3", "e4"},
                            self.board.get_legal_to_squares("e2"))
        self.assertSetEqual({"e5", "e6"},
                            self.board.get_legal_to_squares("e7"))
        self.assertSetEqual(set(),
                            self.board.get_legal_to_squares("c1"))

    def test_getAllReachableToSquaresForBlockedPawn(self):
        self.board.put("black pawn", "a4")
        self.assertSetEqual(set(), self.board.get_legal_to_squares("a4"))

    def test_kingInCheck_ifAttacked(self):
        self.board.put("black rook", "h3")
        self.assertTrue(self.board.king_in_check("white"))
        self.assertFalse(self.board.king_in_check("black"))

    def test_kingNotInCheck_ifInFrontOfPawn(self):
        self.board.put("black pawn", "a4")
        self.assertFalse(self.board.king_in_check("white"))

    def test_kingNotInCheck_ifTwoStepsFromPawnOnInitialSquare(self):
        self.board.move("a3", "e5")
        self.assertFalse(self.board.king_in_check("white"))


class TestFoolsMate(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.move_if_legal("f2", "f3", "white")
        self.board.move_if_legal("e7", "e5", "black")
        self.board.move_if_legal("g2", "g4", "white")
        self.board.move_if_legal("d8", "h4", "black")

    def test_countLegalMovesAfterFoolsMate(self):
        self.assertEqual(0, self.board.count_legal_moves("white"))

    def test_countLegalMoves_inInitialPosition(self):
        self.board = Board()
        self.assertEqual(20, self.board.count_legal_moves("white"))
        self.assertEqual(20, self.board.count_legal_moves("black"))

    def test_checkMate_afterFoolsMate(self):
        self.assertTrue(self.board.is_checkmated("white"))
        self.assertFalse(self.board.is_checkmated("black"))

    def test_gameEndedWithBlackWin_afterWhiteIsCheckmated(self):
        self.assertTrue(self.board.game_ended)
        self.assertEqual("black wins", self.board.result)


class TestStaleMate(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        for square in square_names:
            setattr(self.board, square, "empty")
        self.board.put("a1", "white king")
        self.board.put("b3", "black queen")

    def test_staleMate(self):
        self.assertTrue(self.board.is_stalemate("white"))

    def test_notMate_ifStaleMate(self):
        self.assertFalse(self.board.is_checkmated("white"))


class TestLegalMoves(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_rejectMoveIfIllegal(self):
        self.board.move_if_legal("e2", "d3", "white")
        self.assertEqual("white pawn", self.board.e2)
        self.assertEqual("empty", self.board.d3)

    def test_movePawnIfLegal(self):
        self.board.move_if_legal("e2", "e3", "white")
        self.assertEqual("empty", self.board.e2)
        self.assertEqual("white pawn", self.board.e3)

    def test_moveBishopIfLegal(self):
        self.board.move_if_legal("e2", "e4", "white")
        self.board.move_if_legal("f1", "c4", "white")
        self.assertEqual("empty", self.board.f1)
        self.assertEqual("white bishop", self.board.c4)


class TestCastlingPiecesHaveMoved(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_kingHasNotMoved_ifInitialBoard(self):
        self.assertFalse(self.board.white_king_has_moved)
        self.assertFalse(self.board.black_king_has_moved)

    def test_whiteKingHasMoved(self):
        self.board.free_square("e2")
        self.board.move_if_legal("e1", "e2", "white")
        self.assertTrue(self.board.white_king_has_moved)

    def test_blackKingHasMoved(self):
        self.board.free_square("e7")
        self.board.move_if_legal("e8", "e7", "black")
        self.assertTrue(self.board.black_king_has_moved)

    def test_RooksHaveNotMoved_ifInitialBoard(self):
        self.assertFalse(self.board.a1_rook_has_moved)
        self.assertFalse(self.board.h1_rook_has_moved)
        self.assertFalse(self.board.a8_rook_has_moved)
        self.assertFalse(self.board.h8_rook_has_moved)

    def test_a1RookHasMoved(self):
        self.board.free_square("a2")
        self.board.move_if_legal("a1", "a3", "white")
        self.assertTrue(self.board.a1_rook_has_moved)

    def test_h1RookHasMoved(self):
        self.board.free_square("h2")
        self.board.move_if_legal("h1", "h3", "white")
        self.assertTrue(self.board.h1_rook_has_moved)

    def test_a8RookHasMoved(self):
        self.board.free_square("a7")
        self.board.move_if_legal("a8", "a3", "black")
        self.assertTrue(self.board.a8_rook_has_moved)

    def test_h8RookHasMoved(self):
        self.board.free_square("h7")
        self.board.move_if_legal("h8", "h3", "black")
        self.assertTrue(self.board.h8_rook_has_moved)

    def test_moveIsWhiteCastlingKingside(self):
        self.assertTrue(self.board.move_is_white_castling_kingside("e1", "g1"))

    def test_moveIsBlackCastlingKingside(self):
        self.assertTrue(self.board.move_is_black_castling_kingside("e8", "g8"))

    def test_moveIsNotBlackCastlingKingside_ifKingMoved(self):
        self.board.free_square("e7")
        self.board.move_if_legal("e8", "e7", "black")
        self.board.move_if_legal("e7", "e8", "black")
        self.assertFalse(self.board.move_is_black_castling_kingside("e8", "g8"))

    def test_moveIsNotBlackCastlingKingside_ifRookMoved(self):
        self.board.free_square("h7")
        self.board.move_if_legal("h8", "h7", "black")
        self.board.move_if_legal("h7", "h8", "black")
        self.assertFalse(self.board.move_is_black_castling_kingside("e8", "g8"))

    def test_moveIsWhiteCastlingQueenside(self):
        self.assertTrue(self.board.move_is_white_castling_queenside("e1", "c1"))

    def test_moveIsBlackCastlingQueenside(self):
        self.assertTrue(self.board.move_is_black_castling_queenside("e8", "c8"))

    def test_moveIsNotBlackCastlingQueenside_ifKingMoved(self):
        self.board.free_square("e7")
        self.board.move_if_legal("e8", "e7", "black")
        self.board.move_if_legal("e8", "e7", "black")
        self.assertFalse(self.board.move_is_black_castling_queenside("e8", "c8"))

    def test_moveIsNotBlackCastlingQueenside_ifRookMoved(self):
        self.board.free_square("a7")
        self.board.move_if_legal("a8", "a7", "black")
        self.board.move_if_legal("a8", "a7", "black")
        self.assertFalse(self.board.move_is_black_castling_queenside("e8", "c8"))

    def test_moveIsCastlingMove(self):
        self.assertTrue(self.board.move_is_castling("e1", "g1", "white"))
        self.assertTrue(self.board.move_is_castling("e1", "c1", "white"))
        self.assertTrue(self.board.move_is_castling("e8", "g8", "black"))
        self.assertTrue(self.board.move_is_castling("e8", "c8", "black"))
        self.assertFalse(self.board.move_is_castling("e1", "g1", "black"))
        self.assertFalse(self.board.move_is_castling("e1", "c1", "black"))
        self.assertFalse(self.board.move_is_castling("e8", "g8", "white"))
        self.assertFalse(self.board.move_is_castling("e8", "c8", "white"))


class TestCastlingMove(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_castlingKingsideFieldIsReachable(self):
        self.board.free_square("f1")
        self.board.free_square("g1")
        self.assertTrue(self.board.is_reachable("e1", "g1", "white"))
        self.board.free_square("f8")
        self.board.free_square("g8")
        self.assertTrue(self.board.is_reachable("e8", "g8", "black"))

    def test_castlingKingsideIsLegal(self):
        self.board.free_square("f1")
        self.board.free_square("g1")
        self.assertTrue(self.board.move_is_legal("e1", "g1", "white"))
        self.board.free_square("f8")
        self.board.free_square("g8")
        self.assertTrue(self.board.move_is_legal("e8", "g8", "black"))

    def test_castlingKingsideFieldIsNotReachable_ifPathNotClear(self):
        self.assertFalse(self.board.is_reachable("e1", "g1", "white"))
        self.assertFalse(self.board.move_is_legal("e8", "g8", "black"))

    def test_castlingQueensideFieldIsReachable(self):
        self.board.free_square("d1")
        self.board.free_square("c1")
        self.board.free_square("b1")
        self.assertTrue(self.board.is_reachable("e1", "c1", "white"))
        self.board.free_square("d8")
        self.board.free_square("c8")
        self.board.free_square("b8")
        self.assertTrue(self.board.is_reachable("e8", "c8", "black"))

    def test_castlingQueensideIsLegal(self):
        self.board.free_square("d1")
        self.board.free_square("c1")
        self.board.free_square("b1")
        self.assertTrue(self.board.move_is_legal("e1", "c1", "white"))
        self.board.free_square("d8")
        self.board.free_square("c8")
        self.board.free_square("b8")
        self.assertTrue(self.board.move_is_legal("e8", "c8", "black"))

    def test_castlingQueensideFieldIsNotReachable_ifPathNotClear(self):
        self.assertFalse(self.board.is_reachable("e1", "c1", "white"))
        self.assertFalse(self.board.move_is_legal("e8", "c8", "black"))

    def test_piecesOnTargetSquares_afterWhiteCastlingKingside(self):
        self.board.free_square("f1")
        self.board.free_square("g1")
        self.board.move_if_legal("e1", "g1", "white")
        self.assertEqual("white king", self.board.g1)
        self.assertEqual("white rook", self.board.f1)

    def test_piecesOnTargetSquares_afterBlackCastlingKingside(self):
        self.board.free_square("f8")
        self.board.free_square("g8")
        self.board.move_if_legal("e8", "g8", "black")
        self.assertEqual("black king", self.board.g8)
        self.assertEqual("black rook", self.board.f8)

    def test_piecesOnTargetSquares_afterWhiteCastlingQueenside(self):
        self.board.free_square("d1")
        self.board.free_square("c1")
        self.board.free_square("cb")
        self.board.move_if_legal("e1", "c1", "white")
        self.assertEqual("white king", self.board.c1)
        self.assertEqual("white rook", self.board.d1)

    def test_piecesOnTargetSquares_afterBlackCastlingQueenside(self):
        self.board.free_square("d8")
        self.board.free_square("c8")
        self.board.free_square("b8")
        self.board.move_if_legal("e8", "c8", "black")
        self.assertEqual("black king", self.board.c8)
        self.assertEqual("black rook", self.board.d8)


if __name__ == '__main__':
    unittest.main()
