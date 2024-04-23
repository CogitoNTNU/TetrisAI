import random
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

class GeneticAlgAgentJM:
    agents: list[list[list[float], float]] = []

    def number_of_selection(self, number_of_selections: int):
        self.initAgents()
        for i in range(0, number_of_selections):
            # Select new pops
            print(len(self.agents))
            self.agents = self.replace_30_percent(self.agents)

            # Run new test
            for i in range(len(self.agents)):
                param_list = self.agents[i][0]
                average_cleared = self.play_game(param_list[0], param_list[1], param_list[2], param_list[3], param_list[4])
                self.agents[i][1] = average_cleared
            

    def initAgents(self) -> list[list[list[float], float]]:
        number_of_agents = 20
        for _ in range(0, number_of_agents):
            agg_height = random.randrange(-1000, 0)/1000
            max_height = random.randrange(-1000, 0)/1000
            lines_cleared = random.randrange(0, 1000)/1000
            bumpiness = random.randrange(-1000, 0)/1000
            holes = random.randrange(-1000, 0)/1000

            # agents = [] 
            average_cleared = self.play_game(agg_height, max_height, lines_cleared, bumpiness, holes) / number_of_agents
            self.agents.append([[agg_height, max_height, lines_cleared, bumpiness, holes], average_cleared])
            print(_)
            
        # return agents
    
        
    def play_game(self, agg_height, max_height, lines_cleared, bumpiness, holes):

        board = Tetris()
        agent: Agent = HeuristicWithParametersAgent([agg_height, max_height, lines_cleared, bumpiness, holes])
        total_cleared = 0
        number_of_rounds = 10
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
        
        return total_cleared
    

    def replace_30_percent(self, pop_list: list[list[list[float], float]]) -> list[list[float], float]:
        new_list = []#: list[list[list[float], float]]
        
        
        # Number of pops needed for 30% of total number
        num_pops_needed = int(len(pop_list) * 0.3)

        for _ in range(0, num_pops_needed):
            new_list.append(self.paring_pop(pop_list))  # liste.append(liste[liste, float]) = liste[liste[liste, float]]

        pop_list: sorted(pop_list, key=lambda x: x[1], reverse=False)[:num_pops_needed]

        pop_list.extend(new_list)

        return pop_list
    

     # TODO create method for fetching a random 10%, and finds the two with highest lines cleared, and makes a child (with 5% chance of mutation)
    def paring_pop(self, pop_list: list[list[list[float], float]]) -> list[list[float], float]:
        # Gets the number of pops to select
        num_pops_to_select = int(len(pop_list) * 0.1)

        # Get a sample of pops based on the previous number
        random_pop_sample = random.sample(pop_list, num_pops_to_select)

        # Gets the two pops with the highest lines cleared
        highest_values = sorted(random_pop_sample, key=lambda x: x[1], reverse=True)[:2] 

        # Gets the child pop of the two pops
        new_pop = self.fitness_crossover(highest_values[0], highest_values[1])  # liste[liste, float]
        
        # Mutate 5% of children pops
        if random.randrange(0,1000)/1000 < 0.2:
            random_parameter = int(random.randint(0,4))
            new_pop[0][random_parameter] = (random.randrange(-200, 200)/1000) * new_pop[0][random_parameter]
            
        return new_pop  # liste[liste, float]


    def fitness_crossover(self, pop1: list[list[float], float], pop2: list[list[float], float]) -> list[list[float], float]:
        # Combines the two vectors proportionaly by how many lines they cleared
        parent_pop1 = [h * pop1[1] for h in pop1[0]]
        parent_pop2 = [h * pop2[1] for h in pop2[0]]
        child_pop = [h1 + h2 for h1, h2 in zip(parent_pop1, parent_pop2)]

        return [child_pop, 0.0]  # liste[liste, float]
    

    def getBestPop(self) -> list[list[float], float]:
        pop_list = self.agents
        pop_list = sorted(pop_list, key=lambda x: x[1], reverse=False)
        return pop_list[0]
