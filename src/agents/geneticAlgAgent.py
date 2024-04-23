# From paper: https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
# the weigts the author got:
#  a x (Aggregate Height) + b x (Complete Lines) + c x (Holes) + d x (Bumpiness)
# a = -0.510066 b = 0.760666 c = -0.35663 d = -0.184483
# TODO Read the part of the article about the genetic algorithm
# TODO Create a fitness function
# TODO Create a genetic algorithm based on the
import random
import numpy as np
import operator
from math import sqrt
from src.agents.agent import Agent, play_game
from src.game.tetris import Action, Tetris, transition_model, get_all_actions
from src.agents.heuristic import utility


class GeneticAgent(Agent):

    NUMBER_OF_GAMES = 10

    def __init__(self):
        self.weight_vector = [random.uniform(-2.00, 2.00) for _ in range(5)]

    def result(self, board: Tetris) -> list[Action]:
        possible_boards = board.getPossibleBoards()
        best_board = possible_boards[0]
        best_utility = utility(possible_boards[0], self.weight_vector[0], self.weight_vector[1], self.weight_vector[2], self.weight_vector[3], self.weight_vector[4])
        # Check which board has the best outcome based on the heuristic
        for boards in possible_boards:
            current_utility = utility(boards, self.weight_vector[0], self.weight_vector[1], self.weight_vector[2], self.weight_vector[3], self.weight_vector[4])
            
            if current_utility > best_utility:
                best_board = boards
                best_utility = current_utility

            
        # Find the actions needed to transform the current board to the new board
        actions = []
        try:
            actions = transition_model(board, best_board)
            return actions
        except:
            return actions

    def get_weight_vector(self) -> list[float]:
        return self.weight_vector
            

    def _fitness(self, board: Tetris) -> float:
        fitness = 0
        for _ in range(self.NUMBER_OF_GAMES):
            end_board = play_game(self, board, max_pieces_dropped=500)
            fitness += end_board.rowsRemoved
        return fitness
        
    def _normalize_weights(self):
        ## TODO: Fix this function 
        
        self.weight_vector = [x/sqrt(sum([i**2 for i in self.weight_vector])) for x in self.weight_vector]


    def mutate_child(self):
        for i in range(5):
            if random.random() < 0.05:
                self.get_weight_vector()[i] +=  random.uniform(-0.20, 0.20)
    
    def _crossover(self, parent1: tuple[float, 'GeneticAgent'], parent2: 
                tuple[float, 'GeneticAgent']   ) -> None:
        for i in range(len(self.get_weight_vector())):
            self.weight_vector[i] = ((parent1[0]*parent1[1].get_weight_vector()[i] + parent2[0]*parent2[1].get_weight_vector()[i]))
        

    
    

def average_weight_values(agents: list[float, GeneticAgent]) -> float:
    sum_of_weights = 0
    for agent in agents:
        sum_of_weights += sum(agent[1].get_weight_vector())/len(agent[1].get_weight_vector())
    return sum_of_weights/len(agents)
        


def train_genetic_algorithm(init_population_size: int, tol = 1e-6) -> list[tuple[float, GeneticAgent]]:
    candidates = []     # List of genetic agents on the form (fitness, agent)
    candidate_fitness = np.array([])

    print("Starting genetic algorithm")
    for i in range(init_population_size):
        print("Creating candidate ", i)
        candidate = GeneticAgent()
        board = Tetris()
        fitness = candidate._fitness(board)
        candidates.append((fitness, candidate))
    # Sort the candidates based on their fitness
    print("Initial population done")
    child_candidates = []
    tolerance = average_weight_values(candidates)
    iterations = 0
    print("Starting iterations")
    while abs(tolerance) > tol:
        iterations += 1
        print("Tolerance: ", tolerance)
        print("Starting new generation")
        while len(child_candidates) < 0.3*init_population_size:
            random_indices = select_random_parents(init_population_size)
            parent_candidates = []
            for i in random_indices:
                parent_candidates.append((candidates[i][0], candidates[i][1]))
            parent_candidates = sorted(parent_candidates, key=operator.itemgetter(0), reverse=True)
            print(len(parent_candidates))
            child_tuple = make_offspring(board, parent_candidates[0], parent_candidates[1])
            child_candidates.append((child_tuple))
        tolerance = average_weight_values(candidates)
        candidates = sorted(candidates, key=operator.itemgetter(0), reverse=True)
        candiates = candiates[:init_population_size*0.7+1]
        for child in child_candidates:
            candidates.append(child)
        tolerance -= average_weight_values(candidates)
        print("Generation done")
        print("-------------------")
    print(iterations, " iterations done")
    candidates = sorted(candidates, key=operator.itemgetter(0), reverse=True)
    print("Best candidates weights: [", candidate[0].get_weight_vector()[0], ", ", candidate[0].get_weight_vector()[1], ", ", candidate[0].get_weight_vector()[2], ", ", candidate[0].get_weight_vector()[3], "]")

    return candidates


    
def select_random_parents(init_population_size: int) -> list[int]:
    """
    Selects 10% of the population randomly to be parents for the next generation.
    
    Returns:
      list of indices of unique selected agents.
    """
    random_selection = []
    while len(random_selection) < max(2, init_population_size/10):
        random_index = random.randint(0, init_population_size - 1)
        if random_index not in random_selection:
            random_selection.append(random_index)
    return random_selection
    


def make_offspring(board: Tetris,  parent1: tuple[float, GeneticAgent], parent2: tuple[float, GeneticAgent]) -> tuple[float, GeneticAgent]:
    child = GeneticAgent()
    child.weight_vector = child._crossover(parent1, parent2)
    child.mutate_child()
    child._normalize_weights()
    child_fitness = child._fitness(board)

    return (child_fitness, child)

# def mutate_child(child: geneticAgent) -> geneticAgent:
#     for i in range(len(child.get_weight_vector())):
#         if random.random() < 0.05:
#             child.get_weight_vector()[i] +=  random.uniform(-0.20, 0.20)
#     return child
