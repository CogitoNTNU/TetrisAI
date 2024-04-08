from src.agents.agent import Agent
from src.game.board import Board

from random import random

class RandomAgent(Agent):
    """Random agent that selects a random move from the list of possible moves"""

    def result(board: Board) -> Board:
        possible_moves = board.getPossibleMoves()
        move = random.choice(possible_moves)
        return board.makeMove(move)
