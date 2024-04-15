from src.game.tetris import Tetris
from src.game.TetrisGameManager import *
from src.agents.agent import Agent, play_game
from src.agents.agent_factory import create_agent
from src.agents.heuristic_trainer import train

if __name__ == "__main__":
    # game = Tetris()
    # agent: Agent = create_agent("heuristic")
    # end_board = play_game(agent, game, 7)
    # print(f"There was {end_board.rowsRemoved} rows removed")
    
    # board = Tetris()
    # manager = TetrisGameManager(board)
    
    # manager.startGame()

    train()
