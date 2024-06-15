import argparse
from src.game.tetris import Tetris
from src.game.TetrisGameManager import TetrisGameManager
from src.agents.agent_factory import create_agent
from src.agents.geneticAlgAgentJon import GeneticAlgAgentJM


def self_play():
    """Start a self-playing Tetris game."""
    board = Tetris()
    manager = TetrisGameManager(board)
    manager.startGame()


def demonstrate(agent_type: str):
    """Demonstrate gameplay with a specified agent."""
    board = Tetris()
    agent = create_agent(agent_type)
    manager = TetrisGameManager(board)
    manager.startDemo(agent)


def train_genetic_algorithm(population_size: int = 10):
    """Train the genetic algorithm agent."""
    alg_agent = GeneticAlgAgentJM()
    alg_agent.number_of_selection(population_size)
    print(alg_agent.getBestPop())


def main():
    """Main entry point to handle command-line arguments."""
    parser = argparse.ArgumentParser(description="Tetris Game with different options.")
    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")
    # Self-play parser
    subparsers.add_parser("play", help="Start a self-playing Tetris game.")
    # Demonstrate parser
    demonstrate_parser = subparsers.add_parser(
        "agent", help="Demonstrate gameplay with a specific agent."
    )
    demonstrate_parser.add_argument(
        "agent", type=str, help="Agent type for demonstration."
    )
    # Genetic algorithm training parser
    train_parser = subparsers.add_parser(
        "train", help="Train the genetic algorithm agent."
    )
    train_parser.add_argument(
        "--population_size",
        type=int,
        default=10,
        help="Population size for the genetic algorithm.",
    )
    # Parse the arguments
    args = parser.parse_args()
    # Route commands to the appropriate functions
    if args.command == "play":
        self_play()
    elif args.command == "agent":
        demonstrate(args.agent)
    elif args.command == "train":
        train_genetic_algorithm(args.population_size)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
