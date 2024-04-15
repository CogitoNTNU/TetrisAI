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
from src.agents.heuristic_agent import HeuristicAgent


def train():
    agents = _create_heuristic_agents(10)
    best_agent = None
    best_agent_lines_cleared = float("-inf")

    print(len(agents))

    for agent in agents:
        game = Tetris()
        end_state = play_game(agent, game)
        print("[INFO] new agent train")
        if end_state.rowsRemoved > best_agent_lines_cleared:
            best_agent = agent
            best_agent_lines_cleared = end_state.rowsRemoved
            
    print(f'Dette var de beste hyperparameterne: {best_agent.hyperparameters}')
    print(f"Dette er antall linjer vi fjernet med dem! :-) {best_agent_lines_cleared}")

    game = Tetris()
    end_state = play_game(best_agent, game, shall_render=True)


def _create_heuristic_agents(num_agents: int):
    agents = [HeuristicAgent(create_random_hyperparameters()) for _ in range(num_agents)]
    return agents


def create_random_hyperparameters():
    return [random.uniform(-1, 0), #aggregate_heights_weight
            random.uniform(-1, 0), #max_height_weight
            random.uniform(0, 1), #lines_cleared_weight
            random.uniform(-1, 0), #bumpiness_weight
            random.uniform(-1, 0)  #holes_weight
            ]
    
def play_game(agent: Agent, board: Tetris, actions_per_drop: int = 10, max_moves: int = 1000, shall_render = False) -> Tetris:
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

