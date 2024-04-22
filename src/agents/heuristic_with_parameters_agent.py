from src.agents.agent import Agent
from src.game.tetris import Action, Tetris, transition_model, get_all_actions
from src.agents.heuristic import (
    utility
)

class HeuristicWithParametersAgent(Agent):

    aggregate_heights_weight: float
    max_height_weight: float
    lines_cleared_weight: float
    bumpiness_weight: float
    holes_weight: float

    def __init__(self, params: list[float]):
        self.aggregate_heights_weight = params[0]
        self.max_height_weight = params[1]
        self.lines_cleared_weight = params[2]
        self.bumpiness_weight = params[3]
        self.holes_weight = params[4]

    def result(self, board: Tetris) -> list[Action]:
        # Get all possible boards
        possible_boards = board.getPossibleBoards()

        best_board: Tetris
        best_utility = float("-inf")
        # Check which board has the best outcome based on the heuristic
        for boards in possible_boards:
            current_utility = utility(boards, self.aggregate_heights_weight, self.max_height_weight,
                                    self.lines_cleared_weight, self.bumpiness_weight, self.holes_weight)
            
            if current_utility > best_utility:
                best_board = boards
                best_utility = current_utility

            
        # Find the actions needed to transform the current board to the new board
        actions = []
        try:
            actions = transition_model(board, best_board)
            return actions
        except:
            return actions
