""""
This module contains the Agent class, which is the base 
class for all agents in the simulation.
"""

from abc import ABC, abstractmethod
from typing import Any, Union

from src.game.tetris import Action, Tetris
from time import sleep


class Agent(ABC):
    """Base class for all agents in the simulation."""

    @classmethod
    def __instancecheck__(cls, instance: Any) -> bool:
        return cls.__subclasscheck__(type(instance))

    @classmethod
    def __subclasscheck__(cls, subclass: Any) -> bool:
        return hasattr(subclass, "result") and callable(subclass.result)

    @abstractmethod
    def result(board: Tetris) -> Union[Action, list[Action]]:
        """
        Determines the next move for the agent based on the current state of the board.

        Args:
            board (Board): The current state of the board.

        Returns:
            The next move for the agent. This can be a single action or a list of actions.
        """
        pass


def play_game(agent: Agent, board: Tetris, actions_per_drop: int = 1) -> Tetris:
    """
    Plays a game of Tetris with the given agent.

    Args:
        agent (Agent): The agent to play the game.
        board (Board): The initial state of the board.
        actions_per_drop (int, optional): The number of actions to perform per soft drop. Defaults to 1.

    Returns:
        The final state of the board after the game is over.
    """
    while not board.isGameOver():
        # Get the result of the agent's action
        result = agent.result(board)
        # Perform the action(s) on the board
        if isinstance(result, list):
            for action in result:
                board.doAction(action)
                # board.printBoard()
        else:
            board.doAction(result)
            # board.printBoard()
        # Advance the game by one frame
        board.doAction(Action.SOFT_DROP)
        if board.blockHasLanded:
            board.updateBoard()
        #board.printBoard()

    return board

def playGameDemoStepByStep(agent: Agent, board: Tetris) -> Tetris:
    """
    Plays a game of Tetris with the given agent where actions are slowed down for demonstration purposes.

    Args:
        agent (Agent): The agent to play the game.
        board (Board): The initial state of the board.
    """
    
    # Get the result of the agent's action
    result = agent.result(board)
    # Perform the action(s) on the board
    if isinstance(result, list):
        for action in result:
            board.doAction(action)
            sleep(0.3)
            # board.printBoard()
    else:
        board.doAction(result)
        sleep(0.1)
        # board.printBoard()
    # Advance the game by one frame
    board.doAction(Action.SOFT_DROP)
    if board.blockHasLanded:
        board.updateBoard()
    # board.printBoard()
