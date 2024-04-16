from src.agents.agent_factory import create_agent
from src.agents.random_agent import RandomAgent


def test_create_agent_random():
    agent = create_agent("random")
    assert isinstance(agent, RandomAgent)


def test_create_agent_unknown():
    try:
        create_agent("unknown")
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "Unknown agent type: unknown"
