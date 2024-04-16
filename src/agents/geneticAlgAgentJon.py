import random
from src.game.tetris import *
from src.agents.agent_factory import create_agent
from src.agents.agent import Agent, play_game
# From paper: https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
# the weigts the author got:
#  a x (Aggregate Height) + b x (Complete Lines) + c x (Holes) + d x (Bumpiness)
# a = -0.510066 b = 0.760666 c = -0.35663 d = -0.184483
# TODO Read the part of the article about the genetic algorithm
# TODO Create a fitness function

# TODO Create a genetic algorithm based on the

# List over vectors with boards attached:
# [(List over parameters, board), ...]

# TODO create init-method that creates agents with random vectors
# TODO create run_games-method that goes through the agents, and play 100 games each, return average lines cleared
# TODO create method for fetching a random 10%, and finds the two with highest lines cleared, and makes a child (with 5% chance of mutation)
# TODO create method that makes 30% new agents from existing agents (last method), replace worst 30% with the new agents

list = []

for _ in range(0, 100):
    agg_height = random.random(-1, 0)
    max_height = random.random(-1, 0)
    lines_cleared = random.random(0, 1)
    bumpiness = random.random(-1, 0)
    holes = random.random(-1, 0)
    
    game = Tetris()
    agent: Agent = create_agent("heuristic")
    total_cleared = 0
    for _ in range(0, 100):
        board = play_game(agent, game, 5)
        total_cleared += board.rowsRemoved
    list.append = ([agg_height, max_height, lines_cleared, bumpiness, holes], total_cleared/100)
    
    

def fitness_crossover(pop1: tuple(list[int], int), pop2: tuple(list[int], int)) -> tuple(list[int], int):
    return_pop: tuple(list[int], int)
    # Combines the two vectors proportionaly by how many lines they cleared
    child_pop = pop1[1] * pop1[0] + pop2[1] * pop2[0]

    return tuple(child_pop, 0)