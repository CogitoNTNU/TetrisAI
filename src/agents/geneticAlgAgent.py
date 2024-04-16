from src.agents.agent import Agent
from src.agents.heuristic_agent_Henrik import HeuristicAgentHenrik
from src.game.tetris import Action, Tetris, transition_model, get_all_actions
from src.agents.heuristic import (
    utility,
    find_holes,
    aggregate_height,
    max_height,
    bumpiness,
)
from src.agents.heuristic_agent_Henrik import HeuristicAgentHenrik
from random import *

# From paper: https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
# the weigts the author got:
#  a x (Aggregate Height) + b x (Complete Lines) + c x (Holes) + d x (Bumpiness)
# a = -0.510066 b = 0.760666 c = -0.35663 d = -0.184483
# TODO Read the part of the article about the genetic algorithm
# TODO Create a fitness function

# TODO Create a genetic algorithm based on the


# 1) Randomly initialize populations p
# 2) Determine fitness of population
# 3) Until convergence repeat:
#       a) Select parents from population
#       b) Crossover and generate new population
#       c) Perform mutation on new population
#       d) Calculate fitness for new population


def init_population(population_size: int):
    return [HeuristicAgentHenrik(create_random_hyperparameters()) for _ in range(population_size)]
     

def create_random_hyperparameters():
    return [random.uniform(-1, 0), #aggregate_heights_weight
            random.uniform(-2, 0), #max_height_weight
            random.uniform(0, 10), #lines_cleared_weight
            random.uniform(-1, 0), #bumpiness_weight
            random.uniform(-2, 0)  #holes_weight
            ]

def fitness_function():
    return

def train_genetic(generations: int = 10):
    random_pop = init_population(100)
    top_ten_params = compete(random_pop) # dette er en liste med 10 hyperparm-lister
    parent_population = init_population(10) 
    
    for _ in range(generations): 
        create_population_from_seed(parent_population)
        
    
    
    #lage 50 tilfeldige agenter
    #tren disse, få tilbake de 10 beste
    
    # loop herfra:
    # ta snittet av disse og lag dette til det nye seed-hyperparaemterne
    # muter disse tilfedld9g på 5% f.eks og lag 40 stk
    # lag 10 som er helt tilfeldige og legg dem til i listen
    # konkurer med disse igjen
    #gjenta
    
def create_population_from_seed(seed_population):
    # lag nye agenter der alle aprameterne er justert tilfeldig 
     seed = [[-0.6929074185253369, -2.0111346853425762, 2.109224795114175, -0.7671631536965645, -1.6119464366315754],[-0.6929074185253369, -2.0111346853425762, 2.109224795114175, -0.7671631536965645, -1.6119464366315754] ]
        out = []
        for hyperparams in seed:
            out.append([])
            for params in hyperparams:
                params*= random(0.95,1.05) # dette skal gjøres 10 ganger per underliste
            
        
    
    # return liste med 100 agenter. 10 av dem er helt tilfeldige, 90 av de er mutert fra seed innen 5%

    
      
def compete(agents):
    # Liste for å holde styr på topp 10 agenter
    top_ten_agents = []

    max_itterations = len(agents)
    print(f'Det er {max_itterations} agenter som nå skal prøve seg med tilfeldige hyperparametere!')

    current_iteration = 0

    for agent in agents:
        game = Tetris()
        end_state = play_game(agent, game)
        current_iteration += 1
        print(f"[INFO] Ny agent trent, iterasjon {current_iteration} av {max_itterations}, dette forsøket fjernet {end_state.rowsRemoved} rader.")

        # Legg til agenten og dens resultat i listen
        top_ten_agents.append((agent, end_state.rowsRemoved))

        # Sorter listen basert på antall fjernede rader, og behold kun de ti beste
        top_ten_agents.sort(key=lambda x: x[1], reverse=True)
        top_ten_agents = top_ten_agents[:10]

    # Print informasjon om de ti beste agentene
    print("Topp 10 beste agenter og deres resultater:")
    for index, (agent, score) in enumerate(top_ten_agents, 1):
        print(f"{index}. Agent med hyperparametere {agent.hyperparameters}: {score} rader fjernet.")

    return top_ten_agents