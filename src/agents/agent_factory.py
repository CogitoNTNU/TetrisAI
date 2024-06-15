""" This module contains the factory function for creating agents. """

from src.agents.agent import Agent
from src.agents.random_agent import RandomAgent
from src.agents.heuristic_agent import HeuristicAgent


def create_agent(agent_type: str) -> Agent:
    """Create an agent of the specified type."""

    if agent_type.lower() == "random":
        return RandomAgent()
    elif agent_type.lower() == "heuristic":
        hyperparameters = [1, 1, 1, 1, 1]
        return HeuristicAgent()
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")
