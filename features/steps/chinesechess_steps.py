from behave import given, when, then
from src.chinesechess import ChineseChessBoard

board = ChineseChessBoard()

def parse_position(pos_str):
    # 解析 (row, col) 字串為 tuple，並去除空格
    pos = pos_str.strip('()').split(',')
    return (int(pos[0].strip()), int(pos[1].strip()))

@given('the board is empty except for a Red General at (1, 5)')
def step_impl(context):
    board.clear()
    board.add_piece('General', 'Red', (1, 5))

@when('Red moves the General from (1, 5) to (1, 4)')
def step_impl(context):
    context.move_result = board.move_piece((1, 5), (1, 4))

@then('the move is legal')
def step_impl(context):
    assert context.move_result is True

@given('the board is empty except for a Red General at (1, 6)')
def step_impl(context):
    board.clear()
    board.add_piece('General', 'Red', (1, 6))

@when('Red moves the General from (1, 6) to (1, 7)')
def step_impl(context):
    context.move_result = board.move_piece((1, 6), (1, 7))

@then('the move is illegal')
def step_impl(context):
    assert context.move_result is False

@given('the board has')
def step_impl(context):
    board.clear()
    for row in context.table:
        piece_name = row['Piece']
        color = 'Red' if 'Red' in piece_name else 'Black'
        name = piece_name.replace('Red ', '').replace('Black ', '')
        pos = parse_position(row['Position'])
        board.add_piece(name, color, pos)

@when('Red moves the General from (2, 4) to (2, 5)')
def step_impl(context):
    context.move_result = board.move_piece((2, 4), (2, 5))

@given('the board is empty except for a Red Guard at (1, 4)')
def step_impl(context):
    board.clear()
    board.add_piece('Guard', 'Red', (1, 4))

@when('Red moves the Guard from (1, 4) to (2, 5)')
def step_impl(context):
    context.move_result = board.move_piece((1, 4), (2, 5))

@given('the board is empty except for a Red Guard at (2, 5)')
def step_impl(context):
    board.clear()
    board.add_piece('Guard', 'Red', (2, 5))

@when('Red moves the Guard from (2, 5) to (2, 6)')
def step_impl(context):
    context.move_result = board.move_piece((2, 5), (2, 6))

@given('the board is empty except for a Red Rook at (4, 1)')
def step_impl(context):
    board.clear()
    board.add_piece('Rook', 'Red', (4, 1))

@when('Red moves the Rook from (4, 1) to (4, 9)')
def step_impl(context):
    context.move_result = board.move_piece((4, 1), (4, 9))

@given('the board is empty except for a Red Horse at (3, 3)')
def step_impl(context):
    board.clear()
    board.add_piece('Horse', 'Red', (3, 3))

@when('Red moves the Horse from (3, 3) to (5, 4)')
def step_impl(context):
    context.move_result = board.move_piece((3, 3), (5, 4))

@given('the board is empty except for a Red Cannon at (6, 2)')
def step_impl(context):
    board.clear()
    board.add_piece('Cannon', 'Red', (6, 2))

@when('Red moves the Cannon from (6, 2) to (6, 8)')
def step_impl(context):
    context.move_result = board.move_piece((6, 2), (6, 8))

@given('the board is empty except for a Red Elephant at (3, 3)')
def step_impl(context):
    board.clear()
    board.add_piece('Elephant', 'Red', (3, 3))

@when('Red moves the Elephant from (3, 3) to (5, 5)')
def step_impl(context):
    context.move_result = board.move_piece((3, 3), (5, 5))

@given('the board is empty except for a Red Elephant at (5, 3)')
def step_impl(context):
    board.clear()
    board.add_piece('Elephant', 'Red', (5, 3))

@when('Red moves the Elephant from (5, 3) to (7, 5)')
def step_impl(context):
    context.move_result = board.move_piece((5, 3), (7, 5))

@given('the board is empty except for a Red Soldier at (3, 5)')
def step_impl(context):
    board.clear()
    board.add_piece('Soldier', 'Red', (3, 5))

@when('Red moves the Soldier from (3, 5) to (4, 5)')
def step_impl(context):
    context.move_result = board.move_piece((3, 5), (4, 5))

@when('Red moves the Soldier from (3, 5) to (3, 4)')
def step_impl(context):
    context.move_result = board.move_piece((3, 5), (3, 4))

@when('Red moves the Soldier from (3, 5) to (2, 5)')
def step_impl(context):
    context.move_result = board.move_piece((3, 5), (2, 5))

@given('the board is empty except for a Red Soldier at (6, 5)')
def step_impl(context):
    board.clear()
    board.add_piece('Soldier', 'Red', (6, 5))

@when('Red moves the Soldier from (6, 5) to (6, 4)')
def step_impl(context):
    context.move_result = board.move_piece((6, 5), (6, 4))

@when('Red moves the Soldier from (6, 5) to (5, 5)')
def step_impl(context):
    context.move_result = board.move_piece((6, 5), (5, 5))

@when('Red moves the Rook from (5, 5) to (5, 8)')
def step_impl(context):
    context.move_result = board.move_piece((5, 5), (5, 8))

@when('Red moves the Soldier from (6, 5) to (7, 5)')
def step_impl(context):
    context.move_result = board.move_piece((6, 5), (7, 5))

@then('Red wins immediately')
def step_impl(context):
    assert context.move_result is True
    # 檢查棋盤上已無 Black General
    for piece in board.pieces.values():
        assert not (piece.piece_type.value == 'General' and piece.color.value == 'Black')

@then('the game is not over just from that capture')
def step_impl(context):
    assert context.move_result is True
    # Debug: 輸出棋盤所有棋子
    print('DEBUG: board.pieces =', list(board.pieces.values()))
    # 檢查棋盤上仍有 Black General
    found = False
    for piece in board.pieces.values():
        if piece.piece_type.value == 'General' and piece.color.value == 'Black':
            found = True
    assert found 