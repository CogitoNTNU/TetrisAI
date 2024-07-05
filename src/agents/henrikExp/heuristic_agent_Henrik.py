from src.agents.agent import Agent
from src.game.tetris import Action, Tetris, transition_model, get_all_actions
from src.agents.heuristic import (
    utility,
    find_holes,
    aggregate_height,
    max_height,
    bumpiness,
)


class HeuristicAgentHenrik(Agent):

    def __init__(self, hyperparameters: list[float]): #hyperparameter skal være en liste med 5 tall
        self.hyperparameters = hyperparameters       

    def result(self, board: Tetris) -> list[Action]:

        all_possible_boards = board.getPossibleBoards()
        best_board: Tetris
        best_score = float("-inf")
        for possible_board in all_possible_boards:
            board_utility = utility(possible_board, self.hyperparameters[0], self.hyperparameters[1],self.hyperparameters[2],self.hyperparameters[3],self.hyperparameters[4])
            if board_utility > best_score:
                best_board = possible_board
                best_score = board_utility

        return transition_model(board, best_board)
    