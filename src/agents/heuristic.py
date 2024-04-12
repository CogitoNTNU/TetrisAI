""" The heuristic module contains the heuristics used by the agents. """

from src.game.board import Tetris


def utility(gameState: Tetris) -> int:
    """Returns the utility of the given game state."""
    pass


def aggregate_heights(gameState: Tetris) -> int:
    """Returns the sum of the heights of the columns in the game state."""
    checkedList = [0 for i in range(gameState.COLUMNS)]
    for i in range(gameState.ROWS):
        for j in range(gameState.COLUMNS):
            if gameState.board[i][j] > 0:
                if checkedList[j] == 0:
                    checkedList[j] = gameState.ROWS - i
    return sum(checkedList)


def max_height(gameState: Tetris) -> int:
    """Returns the maximum height of the columns in the game state."""
    checkedList = [0 for i in range(gameState.COLUMNS)]
    for i in range(gameState.ROWS):
        for j in range(gameState.COLUMNS):
            if gameState.board[i][j] > 0:
                if checkedList[j] == 0:
                    checkedList[j] = gameState.ROWS - i
    return max(checkedList)


def lines_cleaned(gameState: Tetris) -> int:
    """Retrurns the number of lines cleared."""
    sum = 0
    for row in gameState.board:
        if all(cell == 1 for cell in row):
            sum += 1
    return sum


def bumpiness(gameState: Tetris) -> int:
    """Returns the sum of the absolute height between all the columns"""
    total_bumpiness = 0
    max_height = 20
    columnHeightMap = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    for column in range(gameState.COLUMNS):
        for row in range(gameState.ROWS):
            if gameState.board[row][column] > 0:
                if columnHeightMap[column] == 0:
                    columnHeightMap[column] = max_height - row

    for key in range(gameState.COLUMNS - 1):
        total_bumpiness += abs(columnHeightMap[key] - columnHeightMap[key + 1])
    return total_bumpiness


def aggregate_height(gameState: Tetris) -> int:
    "Returns the sum of all column-heights"
    max_height = 20
    total_height = 0
    columnHeightMap = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    for column in range(gameState.COLUMNS):
        for row in range(gameState.ROWS):
            if gameState.board[row][column] > 0:
                if columnHeightMap[column] == 0:
                    columnHeightMap[column] = max_height - row

    for key in range(gameState.COLUMNS):
        total_height += columnHeightMap[key]
    return total_height


def find_holes(gameState: Tetris) -> int:
    """Returns number of empty cells on the board.

    Args:
        gameState (Board): the state to check

    Returns:
        The heuristic value
    """
    holes = 0
    for i in range(gameState.COLUMNS):
        top_block = 20
        for j in range(gameState.ROWS):
            if (gameState.board[j][i] == 1) and (j < top_block):
                top_block = j
            if (gameState.board[j][i] == 0) and (j > top_block):
                holes += 1

    return holes
