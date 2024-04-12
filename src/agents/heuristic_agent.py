from src.agents.agent import Agent
from src.game.tetris import Action, Tetris, transition_model
from src.agents.heuristic import (
    find_holes,
    aggregate_height,
    max_height,
    bumpiness,
)


class HeuristicAgent(Agent):

    def result(self, board: Tetris) -> Action:
        # TODO: Get all possible boards

        # TODO: Check which board has the best outcome based on the heuristic

        # TODO: Find the actions needed to transform the current board to the new board
        pass
