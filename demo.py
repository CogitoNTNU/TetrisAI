from src.agents.agent_factory import create_agent
from src.game.tetris import Tetris
from src.game.TetrisGameManager import *

if __name__ == "__main__":
    board = Tetris()
    agent = create_agent("heuristic")
    manager = TetrisGameManager(board)
    manager.startDemo(agent)
