from typing import Tuple
from src.agents.agent import Agent
from src.game.tetris import Action, Tetris, transition_model, get_all_actions
from src.agents.heuristic import utility


class HeuristicAgent(Agent):

    def result(self, board: Tetris) -> Tuple[list[Action], Tetris, Tetris]:
        # Get all possible boards
        possible_boards = board.getPossibleBoards()

        # Check which board has the best outcome based on the heuristic
        best_board = self.checkHeuristic(possible_boards)
        possible_boards.remove(best_board)
        nextBest_board = self.checkHeuristic(possible_boards)

        assert best_board is not None, "No best board found"

        # Find the actions needed to transform the current board to the new board
        actions = transition_model(board, best_board)
        return actions, best_board, nextBest_board

    def checkHeuristic(self, possible_boards: list[Tetris]) -> Tuple[Tetris, float]:
        """
        Check the heuristic of the board
        """

        best_board = None
        best_utility = float("-inf")

        for candidate_board in possible_boards:
            # current_utility = utility(candidate_board, -0.8, -1.2, 4, -0.3,-0.6)
            current_utility = utility(
                candidate_board, -0.510066, 0, 0.760666, -0.184483, -0.3566
            )

            if current_utility > best_utility:
                best_board = candidate_board
                best_utility = current_utility

        return best_board
