""""
This module contains the Agent class, which is the base 
class for all agents in the simulation.
"""

from abc import ABC, abstractmethod
from typing import Any

from src.game.board import Board

class Agent(ABC):
    """Base class for all agents in the simulation."""

    @classmethod
    def __instancecheck__(cls, instance: Any) -> bool:
        return cls.__subclasscheck__(type(instance))
    
    @classmethod
    def __subclasscheck__(cls, subclass: Any) -> bool:
        return (
            hasattr(subclass, 'result') and
            callable(subclass.result)
        )   

    @abstractmethod
    def result(board: Board) -> Board:
        """
        Determines the next move for the agent based on the current state of the board.

        Args:
            board (Board): The current state of the board.
        
        Returns:
            The new state of the board after the agent has made a move.
        """
        pass

