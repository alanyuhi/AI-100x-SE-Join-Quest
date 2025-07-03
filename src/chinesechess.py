from enum import Enum
from typing import Tuple, Dict, Optional

class PieceType(Enum):
    GENERAL = 'General'
    GUARD = 'Guard'
    ROOK = 'Rook'
    HORSE = 'Horse'
    CANNON = 'Cannon'
    ELEPHANT = 'Elephant'
    SOLDIER = 'Soldier'

class Color(Enum):
    RED = 'Red'
    BLACK = 'Black'

class Piece:
    def __init__(self, piece_type: PieceType, color: Color, position: Tuple[int, int]):
        self.piece_type: PieceType = piece_type
        self.color: Color = color
        self.position: Tuple[int, int] = position
    def __repr__(self):
        return f"{self.color.value} {self.piece_type.value} at {self.position}"

class ChineseChessBoard:
    def __init__(self):
        self.pieces: Dict[Tuple[int, int], Piece] = {}

    def clear(self):
        self.pieces = {}

    def add_piece(self, piece_type: str, color: str, position: Tuple[int, int]):
        # 兼容舊步驟定義（str），自動轉 Enum
        pt = PieceType(piece_type.capitalize()) if not isinstance(piece_type, PieceType) else piece_type
        c = Color(color.capitalize()) if not isinstance(color, Color) else color
        self.pieces[position] = Piece(pt, c, position)

    def move_piece(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        if from_pos not in self.pieces:
            return False
        piece = self.pieces[from_pos]
        rule_func = self._get_rule_func(piece.piece_type)
        if not rule_func(piece, to_pos):
            return False
        # 執行移動與吃子（先模擬移動）
        captured = self.pieces.get(to_pos)
        self.pieces[to_pos] = piece
        del self.pieces[from_pos]
        piece.position = to_pos
        # 只有 General 移動時才檢查將帥對面
        if piece.piece_type == PieceType.GENERAL and self._would_generals_face(None, None):
            # 還原
            self.pieces[from_pos] = piece
            piece.position = from_pos
            if captured:
                self.pieces[to_pos] = captured
            else:
                del self.pieces[to_pos]
            return False
        return True

    def _get_rule_func(self, piece_type: PieceType):
        return {
            PieceType.GENERAL: self.is_general_move_legal,
            PieceType.GUARD: self.is_guard_move_legal,
            PieceType.ROOK: self.is_rook_move_legal,
            PieceType.HORSE: self.is_horse_move_legal,
            PieceType.CANNON: self.is_cannon_move_legal,
            PieceType.ELEPHANT: self.is_elephant_move_legal,
            PieceType.SOLDIER: self.is_soldier_move_legal,
        }[piece_type]

    def is_general_move_legal(self, piece: Piece, to_pos: Tuple[int, int]) -> bool:
        """General 只能在九宮格內直橫移動一格"""
        row, col = to_pos
        if piece.color == Color.RED:
            if not (1 <= row <= 3 and 4 <= col <= 6):
                return False
        else:
            if not (8 <= row <= 10 and 4 <= col <= 6):
                return False
        from_row, from_col = piece.position
        if abs(from_row - row) + abs(from_col - col) != 1:
            return False
        return True

    def is_guard_move_legal(self, piece: Piece, to_pos: Tuple[int, int]) -> bool:
        """Guard 只能在九宮格內斜對角移動一格"""
        row, col = to_pos
        if piece.color == Color.RED:
            if not (1 <= row <= 3 and 4 <= col <= 6):
                return False
        else:
            if not (8 <= row <= 10 and 4 <= col <= 6):
                return False
        from_row, from_col = piece.position
        if abs(from_row - row) == 1 and abs(from_col - col) == 1:
            return True
        return False

    def is_rook_move_legal(self, piece: Piece, to_pos: Tuple[int, int]) -> bool:
        """Rook 只能直行或橫行，且路徑上不能有其他棋子"""
        from_row, from_col = piece.position
        to_row, to_col = to_pos
        if from_row != to_row and from_col != to_col:
            return False
        if from_row == to_row:
            step = 1 if to_col > from_col else -1
            for col in range(from_col + step, to_col, step):
                if (from_row, col) in self.pieces:
                    return False
        else:
            step = 1 if to_row > from_row else -1
            for row in range(from_row + step, to_row, step):
                if (row, from_col) in self.pieces:
                    return False
        return True

    def is_horse_move_legal(self, piece: Piece, to_pos: Tuple[int, int]) -> bool:
        """Horse 走日字，且不能被蹩馬腳"""
        from_row, from_col = piece.position
        to_row, to_col = to_pos
        dr, dc = abs(from_row - to_row), abs(from_col - to_col)
        if (dr, dc) not in [(2, 1), (1, 2)]:
            return False
        if dr == 2 and dc == 1:
            leg = (from_row + (1 if to_row > from_row else -1), from_col)
        elif dr == 1 and dc == 2:
            leg = (from_row, from_col + (1 if to_col > from_col else -1))
        else:
            return False
        if leg in self.pieces:
            return False
        return True

    def is_cannon_move_legal(self, piece: Piece, to_pos: Tuple[int, int]) -> bool:
        """Cannon 走法類似 Rook，但吃子時必須隔一子"""
        from_row, from_col = piece.position
        to_row, to_col = to_pos
        if from_row != to_row and from_col != to_col:
            return False
        count = 0
        if from_row == to_row:
            step = 1 if to_col > from_col else -1
            for col in range(from_col + step, to_col, step):
                if (from_row, col) in self.pieces:
                    count += 1
        else:
            step = 1 if to_row > from_row else -1
            for row in range(from_row + step, to_row, step):
                if (row, from_col) in self.pieces:
                    count += 1
        if to_pos in self.pieces:
            return count == 1
        return count == 0

    def is_elephant_move_legal(self, piece: Piece, to_pos: Tuple[int, int]) -> bool:
        """Elephant 只能走田字，不能過河，且中點不能被擋"""
        from_row, from_col = piece.position
        to_row, to_col = to_pos
        dr, dc = abs(from_row - to_row), abs(from_col - to_col)
        if dr != 2 or dc != 2:
            return False
        if piece.color == Color.RED and to_row > 5:
            return False
        if piece.color == Color.BLACK and to_row < 6:
            return False
        mid = ((from_row + to_row) // 2, (from_col + to_col) // 2)
        if mid in self.pieces:
            return False
        return True

    def is_soldier_move_legal(self, piece: Piece, to_pos: Tuple[int, int]) -> bool:
        """Soldier 未過河只能直行，過河後可左右移動但不能後退"""
        from_row, from_col = piece.position
        to_row, to_col = to_pos
        dr, dc = to_row - from_row, abs(to_col - from_col)
        if abs(dr) + abs(dc) != 1:
            return False
        if piece.color == Color.RED:
            # 紅兵前進是 row 減少（dr == -1）
            if from_row >= 6:
                # 過河後可左右，但不能後退（dr == 1）
                if dr == 1:
                    return False
            else:
                # 未過河只能前進
                if dr != -1 or dc != 0:
                    return False
        else:
            # 黑卒前進是 row 增加（dr == 1）
            if from_row <= 5:
                # 過河後可左右，但不能後退（dr == -1）
                if dr == -1:
                    return False
            else:
                # 未過河只能前進
                if dr != 1 or dc != 0:
                    return False
        return True

    def get_piece(self, position: Tuple[int, int]) -> Optional[Piece]:
        return self.pieces.get(position)

    def _would_generals_face(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        generals = [p for p in self.pieces.values() if p.piece_type == PieceType.GENERAL]
        if len(generals) != 2:
            return False
        g1, g2 = generals
        if g1.position[1] != g2.position[1]:
            return False
        col = g1.position[1]
        r1, r2 = g1.position[0], g2.position[0]
        min_row, max_row = min(r1, r2), max(r1, r2)
        for row in range(min_row + 1, max_row):
            if (row, col) in self.pieces:
                return False
        return True 