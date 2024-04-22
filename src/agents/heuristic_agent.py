from src.agents.agent import Agent
from src.game.tetris import Action, Tetris, transition_model, get_all_actions
from src.agents.heuristic import (
    utility
)


class HeuristicAgent(Agent):

    def result(self, board: Tetris) -> list[Action]:
        # Get all possible boards
        possible_boards = board.getPossibleBoards()

        best_board = possible_boards[0]
        best_utility = utility(best_board, -0.8, -1.2, 3, -0.3,-3)
        # Check which board has the best outcome based on the heuristic
        for candidate_board in possible_boards[1:]:
            current_utility = utility(candidate_board, -0.8, -1.2, 4, -0.3,-0.6)
            

            if current_utility > best_utility:
                best_board = candidate_board
                best_utility = current_utility
        
        # Find the actions needed to transform the current board to the new board
        actions = []
        try:
            actions = transition_model(board, best_board)
            return actions
        except:
            return actions
