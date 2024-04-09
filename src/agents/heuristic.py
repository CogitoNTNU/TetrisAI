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

def lines_cleaned(gameState: Board) -> int:
    """ Retrurns the number of lines cleared. """
    sum = 0
    for row in gameState.board:
        if all(cell == 1 for cell in row):
            sum += 1
    return sum

def bumpiness(gameState: Board) -> int:
    """ Returns the sum of the absolute height between all the columns"""
    total_bumpiness = 0
    max_height = 20
    columnHeightMap = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
    for column in range(gameState.columns):
        for row in range (gameState.rows):
            if gameState.board[row][column] > 0:
                if columnHeightMap[column] == 0:
                    columnHeightMap[column] = max_height - row 
                
    for key in range(gameState.columns-1):
        total_bumpiness += abs(columnHeightMap[key] - columnHeightMap[key+1])
    return total_bumpiness

def aggregate_height(gameState: Board) -> int:
    " Returns the sum of all column-heights "
    max_height = 20
    total_height = 0
    columnHeightMap = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
    for column in range(gameState.columns):
        for row in range (gameState.rows):
            if gameState.board[row][column] > 0:
                if columnHeightMap[column] == 0:
                    columnHeightMap[column] = max_height - row
                
    for key in range(gameState.columns):
        total_height += columnHeightMap[key]
    return total_height
    
