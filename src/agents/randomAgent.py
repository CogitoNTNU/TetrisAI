from src.agents.agent import Agent
from src.game.board import Action, Board, get_all_actions

from random import choice


class RandomAgent(Agent):
    """Random agent that selects a random move from the list of possible moves"""

    def result(self, board: Board) -> Action:
        possible_moves = get_all_actions()
        move = choice(possible_moves)
        return move
