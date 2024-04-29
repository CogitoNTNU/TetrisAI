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

    def __init__(self, weight_vector = None):
        self.weight_vector = weight_vector
        if weight_vector is None:
            self.weight_vector = np.random.uniform(-2, 2, 5)
        self._normalize_weights()

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
        actions = transition_model(board, best_board)
        return actions

    def get_weight_vector(self):
        return self.weight_vector
            

    def _fitness(self, board: Tetris) -> float:
        fitness = 0
        for _ in range(self.NUMBER_OF_GAMES):
            end_board = play_game(self, board, max_pieces_dropped=1500)
            fitness += end_board.rowsRemoved / self.NUMBER_OF_GAMES
        return fitness
        
    def _normalize_weights(self):
        self.weight_vector /= np.linalg.norm(self.weight_vector)
        


    def mutate_child(self):
        for i in range(5):
            if random.random() < 0.05:
                self.get_weight_vector()[i] +=  random.uniform(-0.20, 0.20)
    
    
    def _crossover(self, parent1, parent1_fitness : float, parent2, parent2_fitness : float):
        if parent1_fitness == 0 and parent2_fitness == 0:
            parent1_weight = 0.5
            parent2_weight = 0.5
        else:
            parent1_weight = parent1_fitness / (parent1_fitness + parent2_fitness)
            parent2_weight = parent2_fitness / (parent1_fitness + parent2_fitness)
        self.weight_vector = np.add(parent1_weight * parent1, parent2_weight * parent2)
        self._normalize_weights()

def indices_sorted_by_fitness(fitness):
    return np.argsort(-fitness)
    

def norm_of_weights(weights) -> float:
    norm = 0
    transposed_weights = weights.transpose()
    for weight_type in transposed_weights:
        norm += (np.amax(weight_type) - np.amin(weight_type))**2
    return sqrt(norm)


def calculate_fitnesses(candidates):
    fitness = np.array([])
    for candidate in candidates:
        agent = GeneticAgent(candidate)
        board = Tetris()
        fitness = np.append(fitness, agent._fitness(board))
    print("Parents fitnesses: ", fitness[np.argsort(-fitness)])
    return fitness


def train_genetic_algorithm(init_population_size: int, tol = 1e-6):
    weight_candidates = np.array([np.random.uniform(-2, 2, 5) for _ in range(init_population_size)])
    weight_fitnesses = np.array([])

    print("Starting genetic algorithm")
    for i in range(init_population_size):
        print("Creating candidate ", i)
        candidate = GeneticAgent(weight_candidates[i])
        board = Tetris()
        fitness = candidate._fitness(board)
        weight_fitnesses = np.append(weight_fitnesses, fitness)
    # Sort the candidates based on their fitness
    print("Initial population done")
    print("Fitnesses: ", weight_fitnesses[np.argsort(-weight_fitnesses)])
    child_candidates = np.array([[]])
    child_fitnesses = np.array([])
    tolerance = norm_of_weights(weight_candidates)
    iterations = 0
    print("Starting iterations")
    while abs(tolerance) > tol:
        iterations += 1
        print("Tolerance: ", tolerance)
        print("Starting new generation")
        while len(child_candidates) < 0.3*init_population_size:
            random_indices = select_random_parents(init_population_size)
            print("Parents selected")
            parent_candidates = np.array([[]])
            for i in random_indices:
                parent_candidates = np.append(parent_candidates, weight_candidates[i]).reshape(-1, 5)
            parent_fitness = calculate_fitnesses(parent_candidates)
            parent_candidates = parent_candidates[np.argsort(-parent_fitness)]
            parent_fitness = parent_fitness[np.argsort(-parent_fitness)]
            child, child_fitness = make_offspring(board, parent_candidates[0], parent_fitness[0], parent_candidates[1], parent_fitness[1])
            child_candidates = np.append(child_candidates, child).reshape(-1, 5)
            child_fitnesses = np.append(child_fitnesses, child_fitness)
            print("Child ", len(child_candidates), " done")
        tolerance = norm_of_weights(weight_candidates)
        print("Children appended")

        weight_fitnesses = calculate_fitnesses(weight_candidates)
        weight_candidates = weight_candidates[np.argsort(-weight_fitnesses)]
        weight_fitnesses = weight_fitnesses[np.argsort(-weight_fitnesses)]
        weight_candidates = weight_candidates[:(int(np.floor(init_population_size*0.7))+1)]
        weight_fitnesses = weight_fitnesses[:(int(np.floor(init_population_size*0.7))+1)]        

        for c_candidate in child_candidates:
            weight_candidates = np.append(weight_candidates, c_candidate).reshape(-1, 5)
        for c_fitness in child_fitnesses:
            weight_fitnesses = np.append(weight_fitnesses, c_fitness)
        print("Children added to population")
        tolerance -= norm_of_weights(weight_candidates)
        child_candidates = np.array([[]])
        child_fitnesses = np.array([])
        print("Generation of iteration ", iterations, " done")
        print("-------------------")
    print(iterations, " iterations done")
    weight_fitnesses = calculate_fitnesses(weight_candidates)
    weight_candidates = weight_candidates[np.argsort(-weight_fitnesses)]
    weight_fitnesses = weight_fitnesses[np.argsort(-weight_fitnesses)]
    print("Best candidate weights: [", weight_candidates[0][0], ", ", weight_candidates[0][1], ", ", weight_candidates[0][2], ", ", weight_candidates[0][3], ", ", weight_candidates[0][4], "]")
    return weight_candidates[0]
    #print("Best candidates weights: [", candidate[0].get_weight_vector()[0], ", ", candidate[0].get_weight_vector()[1], ", ", candidate[0].get_weight_vector()[2], ", ", candidate[0].get_weight_vector()[3], "]")


    
def select_random_parents(init_population_size: int):
    """
    Selects 10% of the population randomly to be parents for the next generation.
    
    Returns:
      list of indices of unique selected agents.
    """
    random_selection = []
    while len(random_selection) < max(2, (init_population_size/10)):
        random_index = random.randint(0, init_population_size - 1)
        if random_index not in random_selection:
            random_selection.append(random_index)
    return random_selection
    


def make_offspring(board: Tetris,  parent1, parent1_fitness : float, parent2, parent2_fitness : float):
    child = GeneticAgent()
    child._crossover(parent1, parent1_fitness, parent2, parent2_fitness)
    child.mutate_child()
    child._normalize_weights()
    board = Tetris()
    child_fitness = child._fitness(board)
    return child.weight_vector, child_fitness

# def mutate_child(child: geneticAgent) -> geneticAgent:
#     for i in range(len(child.get_weight_vector())):
#         if random.random() < 0.05:
#             child.get_weight_vector()[i] +=  random.uniform(-0.20, 0.20)
#     return child


"""""""""
weights = np.array([
        [0.0, 0.0, 0.0, 0.0, 1.0],
        [0.1, 0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 1.0],
        [0.1, 0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 1.0]
    ])
    fitness = np.array([3, 4, 2, 6, 4])

    weights = weights[np.argsort(-fitness)]

    print(weights)"""