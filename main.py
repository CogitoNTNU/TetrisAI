from src.game.TetrisGameManager import TetrisGameManager
from src.game.board import Board


if __name__ == "__main__":
    board = Board()
    game = TetrisGameManager(board)
    game.startGame()
