import pytest
from src.chinesechess import ChineseChessBoard, PieceType, Color

def setup_board(pieces):
    board = ChineseChessBoard()
    for piece_type, color, pos in pieces:
        board.add_piece(piece_type, color, pos)
    return board

def test_general_move_legal():
    board = setup_board([(PieceType.GENERAL.value, Color.RED.value, (2, 5))])
    assert board.is_general_move_legal(board.get_piece((2, 5)), (1, 5))
    assert not board.is_general_move_legal(board.get_piece((2, 5)), (4, 5))

def test_guard_move_legal():
    board = setup_board([(PieceType.GUARD.value, Color.RED.value, (2, 5))])
    assert board.is_guard_move_legal(board.get_piece((2, 5)), (1, 4))
    assert not board.is_guard_move_legal(board.get_piece((2, 5)), (2, 6))

def test_rook_move_legal():
    board = setup_board([(PieceType.ROOK.value, Color.RED.value, (1, 1))])
    assert board.is_rook_move_legal(board.get_piece((1, 1)), (1, 9))
    assert not board.is_rook_move_legal(board.get_piece((1, 1)), (2, 2))
    # 路徑阻擋
    board.add_piece(PieceType.ROOK.value, Color.RED.value, (1, 5))
    assert not board.is_rook_move_legal(board.get_piece((1, 1)), (1, 9))

def test_horse_move_legal():
    board = setup_board([(PieceType.HORSE.value, Color.RED.value, (3, 3))])
    assert board.is_horse_move_legal(board.get_piece((3, 3)), (5, 4))
    assert not board.is_horse_move_legal(board.get_piece((3, 3)), (4, 4))
    # 馬腳被擋
    board.add_piece(PieceType.ROOK.value, Color.RED.value, (4, 3))
    assert not board.is_horse_move_legal(board.get_piece((3, 3)), (5, 4))

def test_cannon_move_legal():
    board = setup_board([(PieceType.CANNON.value, Color.RED.value, (6, 2))])
    assert board.is_cannon_move_legal(board.get_piece((6, 2)), (6, 8))
    # 吃子必須隔一子
    board.add_piece(PieceType.ROOK.value, Color.BLACK.value, (6, 5))
    board.add_piece(PieceType.ROOK.value, Color.BLACK.value, (6, 8))
    assert board.is_cannon_move_legal(board.get_piece((6, 2)), (6, 8))
    # 路徑超過一子
    board.add_piece(PieceType.ROOK.value, Color.RED.value, (6, 6))
    assert not board.is_cannon_move_legal(board.get_piece((6, 2)), (6, 8))

def test_elephant_move_legal():
    board = setup_board([(PieceType.ELEPHANT.value, Color.RED.value, (3, 3))])
    assert board.is_elephant_move_legal(board.get_piece((3, 3)), (5, 5))
    assert not board.is_elephant_move_legal(board.get_piece((3, 3)), (6, 6))
    # 過河
    assert not board.is_elephant_move_legal(board.get_piece((3, 3)), (7, 5))
    # 田字中點被擋
    board.add_piece(PieceType.ROOK.value, Color.RED.value, (4, 4))
    assert not board.is_elephant_move_legal(board.get_piece((3, 3)), (5, 5))

def test_soldier_move_legal():
    board = setup_board([(PieceType.SOLDIER.value, Color.RED.value, (3, 5))])
    assert board.is_soldier_move_legal(board.get_piece((3, 5)), (2, 5))  # 合法，向上
    assert not board.is_soldier_move_legal(board.get_piece((3, 5)), (4, 5))  # 不合法，向下
    assert not board.is_soldier_move_legal(board.get_piece((3, 5)), (3, 4))
    # 過河後可左右
    board = setup_board([(PieceType.SOLDIER.value, Color.RED.value, (6, 5))])
    assert board.is_soldier_move_legal(board.get_piece((6, 5)), (6, 4))
    assert board.is_soldier_move_legal(board.get_piece((6, 5)), (5, 5))
    assert not board.is_soldier_move_legal(board.get_piece((6, 5)), (7, 5))

def test_capture_and_win():
    # 吃掉 Black General
    board = setup_board([
        (PieceType.ROOK.value, Color.RED.value, (5, 5)),
        (PieceType.GENERAL.value, Color.BLACK.value, (5, 8))
    ])
    assert board.move_piece((5, 5), (5, 8))
    # 應無 Black General
    assert not any(p.piece_type == PieceType.GENERAL and p.color == Color.BLACK for p in board.pieces.values())
    # 吃掉非 General
    board = setup_board([
        (PieceType.ROOK.value, Color.RED.value, (5, 5)),
        (PieceType.CANNON.value, Color.BLACK.value, (5, 8)),
        (PieceType.GENERAL.value, Color.BLACK.value, (8, 5))
    ])
    assert board.move_piece((5, 5), (5, 8))
    # Black General 仍在
    assert any(p.piece_type == PieceType.GENERAL and p.color == Color.BLACK for p in board.pieces.values())

def test_generals_face():
    # 將帥對面不合法
    board = setup_board([
        (PieceType.GENERAL.value, Color.RED.value, (1, 5)),
        (PieceType.GENERAL.value, Color.BLACK.value, (10, 5))
    ])
    board.add_piece(PieceType.ROOK.value, Color.RED.value, (5, 5))
    # 嘗試將 Red General 移到 (2, 5)，有 Rook 阻擋，應合法
    assert board.move_piece((1, 5), (2, 5)) 