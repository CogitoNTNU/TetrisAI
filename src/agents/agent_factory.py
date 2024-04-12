""" This module contains the factory function for creating agents. """

from src.agents.agent import Agent
from src.agents.random_agent import RandomAgent
from src.agents.heuristic_agent import HeuristicAgent


def create_agent(agent_type: str) -> Agent:
    """Create an agent of the specified type."""

    match agent_type.lower():
        case "random":
            return RandomAgent()
        case "heuristic":
            return HeuristicAgent()
        case _:
            raise ValueError(f"Unknown agent type: {agent_type}")
