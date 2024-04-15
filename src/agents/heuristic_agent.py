from src.agents.agent import Agent
from src.game.tetris import Action, Tetris, transition_model, get_all_actions
from src.agents.heuristic import (
    utility,
    find_holes,
    aggregate_height,
    max_height,
    bumpiness,
)


class HeuristicAgent(Agent):

    def result(self, board: Tetris) -> list[Action]:
        
        all_posible_boards = board.getPossibleBoards()
        best_board: Tetris
        for possible_board in all_posible_boards:
            best_score = float("-inf")
            
            board_utility = utility(possible_board, 1,1,1,1,1)
            if board_utility > best_board:
                best_board = possible_board
                best_score = board_utility
                

        
        # for alle mulige trekk, sjekk heurstikk med utility og velg den beste.

        # TODO: Check which board has the best outcome based on the heuristic

        # TODO: Find the actions needed to transform the current board to the new board
        return transition_model(board, best_board)
