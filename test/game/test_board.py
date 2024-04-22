from src.game.block import Block
from src.game.tetris import Action, Tetris, transition_model

import copy


def test_get_possible_boards_for_line():
    i_block = Block(0, 3, 0)
    board: Tetris = Tetris(block=i_block)
    possible_boards = board.getPossibleBoards()
    for board in possible_boards:
        board.printBoard()
    assert isinstance(possible_boards, list)
    for move in possible_boards:
        assert isinstance(move, Tetris)

    standing_up_right = 10
    laying_down_right = 7
    assert len(possible_boards) == standing_up_right + laying_down_right


def test_get_possible_moves_for_square():
    first_block = Block(0, 3, 6)
    board: Tetris = Tetris(block=first_block)

    possible_moves = board.getPossibleBoards()
    assert isinstance(possible_moves, list)
    for move in possible_moves:
        assert isinstance(move, Tetris)

    assert len(possible_moves) == 9


def test_board_equal_for_the_same_object():
    board1 = Tetris()
    assert board1 == board1


def test_clear_row():
    board: Tetris = Tetris()
    board.board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
    expected_board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    lines_to_remove = 1
    board.printBoard()
    rows_removed = board._checkForFullRows()
    board.printBoard()
    for expected_row, board_row in zip(expected_board, board.board):
        assert expected_row == board_row

    assert rows_removed == lines_to_remove


def test_clear_rows():
    board: Tetris = Tetris()
    board.board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
    expected_board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    lines_to_remove = 3
    board.printBoard()
    rows_removed = board._checkForFullRows()
    board.printBoard()
    for expected_row, board_row in zip(expected_board, board.board):
        assert expected_row == board_row

    assert rows_removed == lines_to_remove


def test_do_not_clear_not_full_row():
    board: Tetris = Tetris()
    board.board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
    lines_to_remove = 0
    board.printBoard()
    rows_removed = board._checkForFullRows()
    board.printBoard()

    assert rows_removed == lines_to_remove


def test_transition_model_for_no_transition():
    current_board: Tetris = Tetris()
    target_board: Tetris = current_board

    actions = transition_model(current_board, target_board)
    assert isinstance(actions, list)
    assert len(actions) == 1


def test_transition_model_x_direction():
    current_board: Tetris = Tetris()
    target_board: Tetris = copy.deepcopy(current_board)
    action = Action.MOVE_RIGHT
    target_board.doAction(action)
    actions = transition_model(current_board, target_board)
    assert isinstance(actions, list)
    assert len(actions) == 1


def test_transition_model_complex_target():
    current_board: Tetris = Tetris()
    target_board: Tetris = copy.deepcopy(current_board)
    actual_actions = [
        Action.ROTATE_CLOCKWISE,
        Action.MOVE_RIGHT,
        Action.MOVE_RIGHT,
        Action.MOVE_RIGHT,
        Action.HARD_DROP,
    ]
    for action in actual_actions:
        target_board.doAction(action)
    target_board.updateBoard()

    actions = transition_model(current_board, target_board)
    assert isinstance(actions, list)
    assert len(actions) == len(actual_actions)
    assert actions == actual_actions


def test_transition_model_left_movement():
    current_board: Tetris = Tetris()
    target_board: Tetris = copy.deepcopy(current_board)
    actual_actions = [
        Action.ROTATE_CLOCKWISE,
        Action.ROTATE_CLOCKWISE,
        Action.MOVE_LEFT,
        Action.HARD_DROP,
    ]
    for action in actual_actions:
        target_board.doAction(action)
    target_board.updateBoard()

    actions = transition_model(current_board, target_board)
    assert isinstance(actions, list)
    assert len(actions) == len(actual_actions)
    print(actual_actions)
    assert actions == actual_actions


def test_transition_model_execution():
    current_board: Tetris = Tetris()
    target_board: Tetris = copy.deepcopy(current_board)
    actual_actions = [
        Action.ROTATE_CLOCKWISE,
        Action.ROTATE_CLOCKWISE,
        Action.MOVE_LEFT,
        Action.HARD_DROP,
    ]
    for action in actual_actions:
        target_board.doAction(action)
        if target_board.blockHasLanded:
            target_board.updateBoard()

    actions = transition_model(current_board, target_board)
    for action in actions:
        current_board.doAction(action)
        if current_board.blockHasLanded:
            current_board.updateBoard()
    assert current_board == target_board


def test_transition_model_execution_complex():
    current_board: Tetris = Tetris()
    target_board: Tetris = copy.deepcopy(current_board)
    actual_actions = [
        Action.ROTATE_CLOCKWISE,
        Action.MOVE_LEFT,
        Action.MOVE_LEFT,
        Action.ROTATE_COUNTERCLOCKWISE,
        Action.MOVE_RIGHT,
        Action.HARD_DROP,
    ]
    for action in actual_actions:
        target_board.doAction(action)
        if target_board.blockHasLanded:
            target_board.updateBoard()

    actions = transition_model(current_board, target_board)
    for action in actions:
        current_board.doAction(action)
        if current_board.blockHasLanded:
            current_board.updateBoard()
    assert current_board == target_board


def test_transition_model_execution_of_invalid_move_sequence():
    current_board: Tetris = Tetris()
    target_board: Tetris = copy.deepcopy(current_board)
    actual_actions = [Action.MOVE_LEFT] * 20
    actual_actions += [Action.MOVE_RIGHT] * 20
    actual_actions += [Action.HARD_DROP]
    for action in actual_actions:
        target_board.doAction(action)
        if target_board.blockHasLanded:
            target_board.updateBoard()

    actions = transition_model(current_board, target_board)
    for action in actions:
        current_board.doAction(action)
        if current_board.blockHasLanded:
            current_board.updateBoard()
    assert current_board == target_board
