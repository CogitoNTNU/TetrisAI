import random
import numpy as np
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

from src.game.tetris import *
from src.agents.agent_factory import create_agent
from src.agents.agent import Agent
from src.agents.heuristic_with_parameters_agent import *
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

@dataclass
class Individual:
    parameters: list[float]
    lines_cleared: float

@dataclass 
class Population:
    agents: list[Individual]


class GeneticAlgAgentJM:
    pop: Population = Population([])

    def number_of_selection(self, number_of_selections: int):
        self.initAgent(20)
        for number in range(number_of_selections):
            # Select new pops
            print(f"[INFO] Selecting new pops: {self.pop}")
            
            self.pop.agents = self.replace_30_percent(self.pop)

            # Run new test
            for agent in self.pop.agents:
            # for i in range(len(self.pop)):
                
                param_list = agent.parameters
                average_cleared = self.play_game(param_list[0], param_list[1], param_list[2], param_list[3], param_list[4])                
                agent.lines_cleared = average_cleared
        
            print(f"[INFO] Best individual: {self.getBestPop()}")

    def initAgents(self, number_of_agents: int = 5) -> list[list[list[float], float]]:
        with ThreadPoolExecutor() as executor:
            executor.map(self.initAgent, range(number_of_agents))
            return self.agents

    def initAgent(self, number_of_agents: int):
        for _ in range(0, number_of_agents):
            agg_height = random.randrange(-1000, 0)/1000
            max_height = random.randrange(-1000, 0)/1000
            lines_cleared = random.randrange(0, 1000)/1000
            bumpiness = random.randrange(-1000, 0)/1000
            holes = random.randrange(-1000, 0)/1000

            average_cleared = self.play_game(agg_height, max_height, lines_cleared, bumpiness, holes)
            self.pop.agents.append(Individual([agg_height, max_height, lines_cleared, bumpiness, holes], average_cleared))
            print(_)
    
        
    def play_game(self, agg_height, max_height, lines_cleared, bumpiness, holes):

        board = Tetris()
        agent: Agent = HeuristicWithParametersAgent([agg_height, max_height, lines_cleared, bumpiness, holes])
        total_cleared = 0
        number_of_rounds = 20
        for _ in range(0, number_of_rounds):
                
            max_moves = number_of_rounds
            move = 0
            actions_per_drop = 7
                
            while not board.isGameOver() and move < max_moves:
            # Get the result of the agent's action
                for _ in range(actions_per_drop):
                    result = agent.result(board)
                    # Perform the action(s) on the board
                    if isinstance(result, list):
                        for action in result:
                            board.doAction(action)
                    else:
                        board.doAction(result)
                
                move += 1
            # Advance the game by one frame
            board.doAction(Action.SOFT_DROP)
            #board.printBoard()

            total_cleared += board.rowsRemoved
        
        return total_cleared / number_of_rounds
    

    def replace_30_percent(self, pop_list: Population) -> Population:
        """" Creates 30% new agents from existing agents, and replaces the worst 30% with the new agents """
        # Number of pops needed for 30% of total number
        num_pops_needed = int(len(pop_list.agents) * 0.3)

        new_list = [self.paring_pop(pop_list) for _ in range(num_pops_needed)]

        pop_list.agents = sorted(pop_list.agents, key=lambda x: x[1], reverse=False)[num_pops_needed:]

        pop_list.extend(new_list)

        return pop_list
    

     # TODO create method for fetching a random 10%, and finds the two with highest lines cleared, and makes a child (with 5% chance of mutation)
    def paring_pop(self, pop_list: Population) -> Population:
        # Gets the number of pops to select
        num_pops_to_select = int(len(pop_list.agents) * 0.1)

        # Get a sample of pops based on the previous number
        random_pop_sample = random.sample(pop_list.agents, num_pops_to_select)

        # Gets the two pops with the highest lines cleared
        highest_values = sorted(random_pop_sample, key=lambda x: x[1], reverse=True)[:2] 

        # Gets the child pop of the two pops
        new_pop = self.fitness_crossover(highest_values[0], highest_values[1])
        
        # Mutate 5% of children pops
        if random.randrange(0,1000)/1000 < 0.05:
            random_parameter = int(random.randint(0,4))
            new_pop[0][random_parameter] = (random.randrange(-200, 200)/1000) * new_pop[0][random_parameter]

        new_pop[0] = (new_pop[0] / np.linalg.norm(new_pop[0])).tolist()

        return new_pop


    def fitness_crossover(self, pop1: Population, pop2: Population) -> Population:
        # Combines the two vectors proportionaly by how many lines they cleared
        child_pop = [h1 * pop1[1] + h2 * pop2[1] for h1, h2 in zip(pop1[0], pop2[0])]
        return [child_pop, 0.0]
    

    def getBestPop(self) -> Individual:
        pop_list = self.pop
        pop_list = sorted(pop_list, key=lambda x: x[1], reverse=True)
        return pop_list[0]
