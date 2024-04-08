""" The heuristic module contains the heuristics used by the agents. """

from src.game.board import Board

def utility(gameState: Board) -> int:
    """ Returns the utility of the given game state. """
    pass


def aggregate_heights(gameState: Board) -> int:
    """ Returns the sum of the heights of the columns in the game state. """
    checkedList = [0 for i in range(gameState.columns)]
    for i in range(gameState.rows):
        for j in range(gameState.columns):
            if gameState.board[i][j] > 0:
                if checkedList[j] == 0:
                    checkedList[j] = gameState.rows - i+1
    return sum(checkedList)
                    
                    


if __name__ == "__main__":
    board = Board()
    board.board =\
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0], 
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    assert aggregate_heights(board) == 27