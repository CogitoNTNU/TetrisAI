import random
from src.agents.agent import Agent
from src.game.tetris import Action, Tetris, transition_model, get_all_actions
from src.agents.heuristic import (
    utility,
    find_holes,
    aggregate_height,
    max_height,
    bumpiness,
)
from src.agents.heuristic_agent_Henrik import HeuristicAgentHenrik

#kan visualisere lines cleared hvordan den bederer seg over tid.

def train():
    current_itteration = 0
    agents = _create_heuristic_agents(30)
    max_itterations = len(agents)
    best_agent = None
    best_agent_lines_cleared = 10
    min_lines_cleared = 8
    
    hyperparameters_seed = [-0.9550579397805573, -1.713732853744936, 0.48480501821908994, -0.8785318347320727, -1.828473435227082]
    epsilon = 0.001
    learning_rate = 0.01

    print(len(agents))

    for agent in agents:
        game = Tetris()
        newAgent = _create_heuristic_agents_hyper(hyperparameters_seed)
        end_state = play_game(newAgent, game)
        current_itteration += 1
        print(f"[INFO] new agent train, itteration {current_itteration} of {max_itterations}, current best {best_agent_lines_cleared}, this took {end_state.rowsRemoved} ")
        if end_state.rowsRemoved > best_agent_lines_cleared:
            print(f"[UPDATE] Ny beste agent funnet med {end_state.rowsRemoved} rader fjernet.")
            improvement_factor = (end_state.rowsRemoved - best_agent_lines_cleared) / (best_agent_lines_cleared + epsilon)
            hyperparameters_seed = [
                seed + learning_rate * improvement_factor * (agent_param - seed)
                for seed, agent_param in zip(hyperparameters_seed, agent.hyperparameters)
            ]
            best_agent = agent
            best_agent_lines_cleared = end_state.rowsRemoved

        elif end_state.rowsRemoved > min_lines_cleared:
            relative_improvement = (end_state.rowsRemoved - min_lines_cleared) / (best_agent_lines_cleared - min_lines_cleared + epsilon)
            hyperparameters_seed = [
                seed + learning_rate * relative_improvement * epsilon * (agent_param - seed)
                for seed, agent_param in zip(hyperparameters_seed, agent.hyperparameters)
            ]
    
    #return best_agent, hyperparameters_seed 
            
    print(f'Dette var de beste hyperparameterne: {best_agent.hyperparameters}')
    print(f"Dette er antall linjer vi fjernet med dem! :-) {best_agent_lines_cleared}")

    game = Tetris()
    end_state = play_game(best_agent, game, shall_render=False)
    
def check_average():
    hyperparameters = [-0.9550579397805573, -1.713732853744936, 0.48480501821908994, -0.8785318347320727, -1.828473435227082]
    agents = [HeuristicAgentHenrik(hyperparameters) for _ in range(10)]
    current_itteration = 0
    max_itterations = 10
    best_agent_lines_cleared = 0
    best_agent = None
    
    for agent in agents:
        game = Tetris()
        end_state = play_game(agent, game)
        current_itteration += 1
        print(f"[INFO] new agent train, itteration {current_itteration} of {max_itterations}, current best {best_agent_lines_cleared}, this took {end_state.rowsRemoved} ")
        if end_state.rowsRemoved > best_agent_lines_cleared:
            print(f"[UPDATE] Ny beste agent funnet med {end_state.rowsRemoved} rader fjernet.")
            best_agent = agent
            best_agent_lines_cleared = end_state.rowsRemoved

    print(f'Dette var de beste hyperparameterne: {best_agent.hyperparameters}')
    print(f"Dette er antall linjer vi fjernet med dem! :-) {best_agent_lines_cleared}")
    
    

def train_random():
    current_itteration = 0
    agents = _create_heuristic_agents(50)
    max_itterations = len(agents)
    best_agent = None
    best_agent_lines_cleared = 0
    
    print(f'Det er {len(agents)} agenter som nå skaø prøve seg med tilfeldige hyperparametere!')

    for agent in agents:
        game = Tetris()
        end_state = play_game(agent, game)
        current_itteration += 1
        print(f"[INFO] new agent train, itteration {current_itteration} of {max_itterations}, current best {best_agent_lines_cleared}, this took {end_state.rowsRemoved} ")
        if end_state.rowsRemoved > best_agent_lines_cleared:
            print(f"[UPDATE] Ny beste agent funnet med {end_state.rowsRemoved} rader fjernet.")
            best_agent = agent
            best_agent_lines_cleared = end_state.rowsRemoved
            
    print(f'Dette var de beste hyperparameterne: {best_agent.hyperparameters}')
    print(f"Dette er antall linjer vi fjernet med dem! :-) {best_agent_lines_cleared}")

    game = Tetris()
    end_state = play_game(best_agent, game, shall_render=False)
    

def _create_heuristic_agents(num_agents: int):
    agents = [HeuristicAgentHenrik(create_random_hyperparameters()) for _ in range(num_agents)]
    return agents

def _create_heuristic_agents_hyper(hyperparameters):
    return HeuristicAgentHenrik(hyperparameters)


def create_random_hyperparameters():
    return [random.uniform(-1, 0), #aggregate_heights_weight
            random.uniform(-3, 0), #max_height_weight
            random.uniform(0, 10), #lines_cleared_weight
            random.uniform(-1, 0), #bumpiness_weight
            random.uniform(-2, 0)  #holes_weight
            ]
    
def play_game(agent: Agent, board: Tetris, actions_per_drop: int = 10, max_moves: int = 50000, shall_render = False) -> Tetris:
    """
    Plays a game of Tetris with the given agent.

    Args:
        agent (Agent): The agent to play the game.
        board (Board): The initial state of the board.
        actions_per_drop (int, optional): The number of actions to perform per soft drop. Defaults to 1.

    Returns:
        The final state of the board after the game is over.
    """
    

    move = 0
    try: 
        while not board.isGameOver() or move < max_moves:
            move += 1
            # Get the result of the agent's action
            for _ in range(actions_per_drop):
                result = agent.result(board)
                # Perform the action(s) on the board
                if isinstance(result, list):
                    for action in result:
                        board.doAction(action)
                else:
                    board.doAction(result)
            # Advance the game by one frame
            board.doAction(Action.SOFT_DROP)
            if shall_render:
                board.printBoard()
                
    except Exception:
        return board

    return board           



def train_beta():
    current_iteration = 0
    agents = _create_heuristic_agents(500)
    max_iterations = len(agents)
    best_agent = None
    best_agent_lines_cleared = 10
    min_lines_cleared = 8
    
    hyperparameters_seed = [-0.6272731926460421, -0.029942858429951258, 1.1576374779977394, -0.9984880816033778, -0.4298512882832837]
    best_hyperparameters = list(hyperparameters_seed)
    learning_rate = 0.1
    learning_rate_decay = 0.9
    exploration_rate = 0.1
    
    print(len(agents))

    for agent in agents:
        game = Tetris()
        end_state = play_game(agent, game)
        current_iteration += 1
        lines_cleared = end_state.rowsRemoved
        
        print(f"[INFO] Ny agent trener, iterasjon {current_iteration} av {max_iterations}, nåværende beste {best_agent_lines_cleared}, dette tok {lines_cleared} rader")
        
        # Utforsk nye hyperparametre med en sjanse på exploration_rate
        if random.random() < exploration_rate:
            hyperparameters_seed = create_random_hyperparameters()
        
        # Hvis agenten presterer bedre, oppdater de beste hyperparametrene
        if lines_cleared > best_agent_lines_cleared:
            print(f"[UPDATE] Ny beste agent funnet med {lines_cleared} rader fjernet.")
            best_hyperparameters = list(agent.hyperparameters)
            best_agent_lines_cleared = lines_cleared
            best_agent = agent
            learning_rate *= learning_rate_decay  # Reduser læringsraten etter en vellykket oppdatering
        elif lines_cleared < best_agent_lines_cleared:
            # Tilbakestill til de beste kjente hyperparametrene hvis ytelsen er dårlig
            hyperparameters_seed = list(best_hyperparameters)
            learning_rate /= learning_rate_decay  # Øk læringsraten for å utforske mer
            

    
    print(f'Dette var de beste hyperparameterne: {best_agent.hyperparameters}')
    print(f"Dette er antall linjer vi fjernet med dem! :-) {best_agent_lines_cleared}")
    

