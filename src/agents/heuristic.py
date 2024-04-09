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
                    checkedList[j] = gameState.rows - i
    return sum(checkedList)

def max_height(gameState: Board) -> int:
    """ Returns the maximum height of the columns in the game state. """
    checkedList = [0 for i in range(gameState.columns)]
    for i in range(gameState.rows):
        for j in range(gameState.columns):
            if gameState.board[i][j] > 0:
                if checkedList[j] == 0:
                    checkedList[j] = gameState.rows - i
    return max(checkedList)

def find_holes(gameState: Board) -> int:
    """ Returns number of empty cells on the board. 
    
    Args:
        gameState (Board): the state to check

    Returns: 
        The heuristic value
    """
    holes = 0
    for i in range(gameState.columns):
        top_block = 20
        for j in range(gameState.rows):
            if (gameState.board[j][i] == 1) and (j < top_block):
                top_block = j
            if (gameState.board[j][i] == 0) and (j > top_block):
                holes += 1

    return holes