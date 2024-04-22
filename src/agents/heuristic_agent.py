from src.agents.agent import Agent
from src.game.tetris import Action, Tetris, transition_model, get_all_actions
from src.agents.heuristic import (
    utility
)


class HeuristicAgent(Agent):

    def result(self, board: Tetris) -> list[Action]:
        # Get all possible boards
        possible_boards = board.getPossibleBoards()

        best_board: Tetris
        best_utility = float("-inf")
        # Check which board has the best outcome based on the heuristic
        for boards in possible_boards:
            current_utility = utility(boards, -0.5, -1.2, 2, -0.3,-0.6)
            
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

    
