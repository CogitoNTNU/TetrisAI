import os
import json
from dataclasses import asdict, dataclass

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from src.game.tetris import Tetris
from src.game.TetrisWebGameManager import TetrisGameManager
from src.agents.agent_factory import create_agent, AVAILABLE_AGENTS


app = FastAPI(
    title="Cogito TetrisAI API",
    description="This API provides a WebSocket interface to play Tetris and watch a Tetris AI agent play the game.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to allow specific origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/agents", response_model=list)
async def get_available_agents():
    """
    Returns a list of available agents for playing the game.
    """
    return AVAILABLE_AGENTS


@dataclass
class Score:
    name: str
    score: int
    date: str


HIGHSCORES_FILE = "highscores.json"


def initialize_file():
    """Ensure the highscores file exists and contains valid JSON."""
    if not os.path.isfile(HIGHSCORES_FILE):
        with open(HIGHSCORES_FILE, "w") as file:
            json.dump([], file)
    else:
        # Check if the file is empty or invalid
        try:
            with open(HIGHSCORES_FILE, "r") as file:
                if not file.read().strip():
                    # If the file is empty, write an empty list
                    with open(HIGHSCORES_FILE, "w") as file:
                        json.dump([], file)
        except json.JSONDecodeError:
            # If the file contains invalid JSON, reset it
            with open(HIGHSCORES_FILE, "w") as file:
                json.dump([], file)


@app.get("/highscores", response_model=list[Score])
async def get_highscores():
    initialize_file()

    with open(HIGHSCORES_FILE, "r") as file:
        scores_data = json.load(file)
        scores = [Score(**score) for score in scores_data]
    return scores


@app.post("/highscores", response_model=Score)
async def add_highscore(raw_score: dict):
    initialize_file()

    # Read existing scores
    with open(HIGHSCORES_FILE, "r") as file:
        scores_data = json.load(file)

    # Create new score instance
    score = Score(**raw_score)
    scores_data.append(asdict(score))

    # Write the updated scores back to the file
    with open(HIGHSCORES_FILE, "w") as file:
        json.dump(scores_data, file)

    return score


@app.websocket("/ws/game")
async def websocket_endpoint(websocket: WebSocket):
    board = Tetris()  # Initialize the game board
    manager = TetrisGameManager(board, websocket)
    await websocket.accept()
    print("WebSocket connection established")

    try:
        await manager.startGame()  # Start the game loop with automatic block dropping
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        print("WebSocket connection closed")
        await websocket.close()


@app.websocket("/ws/demo/{agent_type}")
async def websocket_demo_endpoint(websocket: WebSocket, agent_type: str):
    agent = create_agent(agent_type)  # Create agent for demo
    board = Tetris()  # Initialize the game board
    manager = TetrisGameManager(board, websocket)

    await websocket.accept()
    print("WebSocket demo connection established")

    try:
        await manager.startDemo(agent)
    except Exception as e:
        print(f"WebSocket demo error: {e}")
    finally:
        print("WebSocket demo connection closed")
        await websocket.close()


# Dummy route for documentation purposes
@app.get("/ws/game/info", include_in_schema=True)
async def websocket_game_info():
    """
    This endpoint provides information about the `/ws/game` WebSocket.

    ### WebSocket Connection:
    - **URL:** `/ws/game`
    - **Expected Messages:**
      - `"MOVE_LEFT"`: Move the Tetris block to the left
      - `"MOVE_RIGHT"`: Move the Tetris block to the right
      - `"SOFT_DROP"`: Drop the Tetris block one row
      - `"HARD_DROP"`: Drop the Tetris block to the bottom
      - `"ROTATE_CLOCKWISE"`: Rotate the block clockwise

    ### Responses:
    - The server will periodically send the updated game state via WebSocket.
    - The game state is sent as a JSON object with the following fields:
      - `"board"`: 2D array representing the Tetris board
      - `"score"`: The current score of the player
      - `"gameOver"`: Whether the game is over or not

    ### Example Game State Response:
    ```json
    {
      "board": [[0, 0, 1, 1], [1, 1, 0, 0], ...],
      "score": 10,
      "gameOver": false
    }
    ```
    """

    return JSONResponse(
        {"info": "This is the documentation for the /ws/game WebSocket endpoint."}
    )
