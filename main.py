from src.game.TetrisGameManager import TetrisGameManager
from src.game.tetris import Tetris


if __name__ == "__main__":
    board = Tetris()
    game = TetrisGameManager(board)
    game.startGame()
