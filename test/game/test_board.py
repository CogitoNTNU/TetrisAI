from src.game.block import Block
from src.game.board import Board, transition_model

import copy

def test_get_possible_moves():
    board: Board = Board()

    board.setBlock(Block(0,5, 5))
    possible_moves = board.getPossibleMoves()
    assert isinstance(possible_moves, list)
    for move in possible_moves:
        assert isinstance(move, Board)
    
    assert len(possible_moves) == 9


def test_transition_model():
    current_board: Board = Board()
    target_board: Board = copy.deepcopy(current_board)

    # Make a move
    target_board.placeBlock()

    actions = transition_model(current_board, target_board) 
    assert isinstance(actions, list)
    assert len(actions) == 1

