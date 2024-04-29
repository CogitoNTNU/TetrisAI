from src.agents.agent import Agent
from src.game.tetris import Action, Tetris, transition_model, get_all_actions
from src.agents.heuristic import (
    utility
)


class HeuristicAgent(Agent):

    def result(self, board: Tetris) -> list[Action]:
        # Get all possible boards
        possible_boards = board.getPossibleBoards()

        best_board = None
        best_utility = float('-inf')
        # Check which board has the best outcome based on the heuristic
        for candidate_board in possible_boards:
            # current_utility = utility(candidate_board, -0.8, -1.2, 4, -0.3,-0.6)
            current_utility = utility(candidate_board, -0.510066, 0, 0.760666, -0.184483, -0.3566)
            
            if current_utility > best_utility:
                best_board = candidate_board
                best_utility = current_utility
        
        # Find the actions needed to transform the current board to the new board
        actions = []
        actions = transition_model(board, best_board)
        return actions
           
