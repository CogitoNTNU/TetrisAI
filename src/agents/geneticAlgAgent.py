# From paper: https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
# the weigts the author got:
#  a x (Aggregate Height) + b x (Complete Lines) + c x (Holes) + d x (Bumpiness)
# a = -0.510066 b = 0.760666 c = -0.35663 d = -0.184483
# TODO Read the part of the article about the genetic algorithm
# TODO Create a fitness function
# TODO Create a genetic algorithm based on the
import random
from math import sqrt
from src.agents.agent import Agent, play_game
from src.game.tetris import Action, Tetris, transition_model, get_all_actions
from src.agents.heuristic import utility


class geneticAgent(Agent):

    NUMBER_OF_GAMES = 10

    def __init__(self):
        self.weight_vector = [random.uniform(-2.00, 2.00) for _ in range(4)]

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
        self.weight_vector = sqrt(sum([v**2 for v in self.get_weight_vector()]))
    
    def _crossover(self, parent1: geneticAgent, parent2: geneticAgen) -> geneticAgent:
        for i in range(len(parent1)):
            self.weight_vector[i] = ((parent1[i]*parent1.get_weight_vector()[i] + parent2[i]*parent2.get_weight_vector()[i]))




def train_genetic_algorithm(init_population_size: int) -> list[tuple[float, geneticAgent]]:
    candidates = []     # List of genetic agents on the form (fitness, agent)
   
    for _ in range(init_population_size):
        candidate = geneticAgent()
        board = Tetris()
        fitness = candidate._fitness(board)
        candidates.append((fitness, candidate))
    # Sort the candidates based on their fitness
    child_candidates = []
    
    while len(child_candidates) < 0.3*init_population_size:
        random_indices = select_random_parents(init_population_size)
        parent_candidates = []
        for i in random_indices:
            parent_candidates.append(candidates[i])
        parent_candidates.sort(reverse=True)
        child_candidates.append(make_offspring(board, parent_candidates[0], parent_candidates[1]))

    return candidates


    
def select_random_parents(init_population_size: int) -> list[int]:
    """
    Selects 10% of the population randomly to be parents for the next generation.
    
    Returns:
      list of indices of unique selected agents.
    """
    random_selection = []
    while len(random_selection) < (init_population_size/10):
        random_index = random.randint(0, init_population_size - 1)
        if random_index not in random_selection:
            random_selection.append(random_index)
    return random_selection
    


def make_offspring(board: Tetris,  parent1: tuple[float, geneticAgent], parent2: tuple[float, geneticAgent]) -> tuple[float, geneticAgent]:
    child = geneticAgent()
    child.weight_vector = child._crossover(parent1, parent2)
    child_fitness = child._fitness(board)

    return (child_fitness, child)


