from src.agents.agent import Agent
from src.game.tetris import Action, Tetris, transition_model
from src.agents.heuristic import (
    utility
)


class HeuristicAgent(Agent):

    def result(self, board: Tetris) -> list[Action]:
        # Get all possible boards
        possible_boards = board.getPossibleBoards()

        best_board: Tetris
        best_utility = 0
        # Check which board has the best outcome based on the heuristic
        for board in possible_boards:
            current_utility = utility(board, 1, 1, 1, 1,1)
            
            if current_utility > best_utility:
                best_board = board
                best_utility = current_utility

            
        # Find the actions needed to transform the current board to the new board
        actions = transition_model(board, best_board)
        return actions
