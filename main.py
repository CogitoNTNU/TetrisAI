from src.game.tetris import Tetris
from src.game.TetrisGameManager import *
from src.agents.agent import Agent, play_game
from src.agents.agent_factory import create_agent
from src.agents.heuristic import (
    utility
)
from src.agents.heuristic_trainer import train
from src.agents.geneticAlgAgentJon import GeneticAlgAgentJM

def test():
    # algAgent = GeneticAlgAgentJM()
    # algAgent.number_of_selection(2)
    # print(algAgent.getBestPop())
    
    board = Tetris()
    agent = create_agent("heuristic")
    manager = TetrisGameManager(board)
    manager.startDemo(agent)
    
if __name__ == "__main__":

    # game = Tetris()
    # agent: Agent = create_agent("heuristic")
    # sum_rows_removed = 0
    # for i in range(10):
    #     end_board = play_game(agent, game, 7)
    #     end_board.printBoard()
    #     sum_rows_removed += end_board.rowsRemoved

    # print(f"Average rows removed: {sum_rows_removed / 10}")

    # possible_moves = game.getPossibleBoards()
    # for boards in possible_moves:
    #     print(utility(boards, 0, -1, 0, 0, 0))
    #     boards.printBoard()
    
    # board = Tetris()
    # manager = TetrisGameManager(board)
    # agent = create_agent("heuristic")
    
    # # manager.startGame()

<<<<<<< HEAD
    # # train()


    # algAgent = GeneticAlgAgentJM()
    # algAgent.number_of_selection(2)
    # print(algAgent.getBestPop())
    
    test()
    
        
    # cProfile.run('main()', 'restats')  
=======
    #train()
    
>>>>>>> c14418b (feat: :rocket: genetic agent class and it's training algorithm commenced)
