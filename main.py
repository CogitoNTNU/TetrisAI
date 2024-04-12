from src.game.tetris import Tetris
from src.agents.agent import Agent, play_game
from src.agents.agent_factory import create_agent

if __name__ == "__main__":
    game = Tetris()
    agent: Agent = create_agent("heuristic")
    end_board = play_game(agent, game, 7)
    print(f"There was {end_board.rowsRemoved} rows removed")
