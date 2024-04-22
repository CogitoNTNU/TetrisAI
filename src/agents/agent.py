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


def play_game(agent: Agent, board: Tetris, actions_per_drop: int = 1, max_pieces_dropped: int = 1_000_000_000) -> Tetris:
    """
    Plays a game of Tetris with the given agent.

    Args:
        agent (Agent): The agent to play the game.
        board (Board): The initial state of the board.
        actions_per_drop (int, optional): The number of actions to perform per soft drop. Defaults to 1.

    Returns:
        The final state of the board after the game is over.
    """
    pieces_dropped = 0
    while not board.isGameOver() and pieces_dropped < max_pieces_dropped:
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
        pieces_dropped += 1

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
    
    if Action.HARD_DROP in result:
        result.remove(Action.HARD_DROP)
        result.append([Action.SOFT_DROP] * 20)
    # Perform the action(s) on the board
    if isinstance(result, list):
        for action in result:
            board.doAction(action, demo=True)
    else:
        board.doAction(action, demo=True)
    # Advance the game by one frame
    board.doAction(Action.SOFT_DROP)
    if board.blockHasLanded:
        board.updateBoard()
