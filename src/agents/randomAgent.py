from src.agents.agent import Agent
from src.game.board import Action, Board, get_all_actions

from random import choice


class RandomAgent(Agent):
    """Random agent that selects a random move from the list of possible moves"""

    def result(self, board: Board) -> Action:
        # TODO: Get all possible actions

        # TODO: Return a random action
        pass
