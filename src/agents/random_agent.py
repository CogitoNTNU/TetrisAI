from src.agents.agent import Agent
from src.game.tetris import Action, Tetris, get_all_actions

from random import choice


class RandomAgent(Agent):
    """Random agent that selects a random move from the list of possible moves"""

    def result(self, board: Tetris) -> Action:
        # TODO: Get all possible actions
        possible_actions = get_all_actions()
        # TODO: Return a random action
        return choice(possible_actions)
        
        
