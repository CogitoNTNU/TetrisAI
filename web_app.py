from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from src.game.tetris import Tetris
from src.game.TetrisWebGameManager import TetrisGameManager
from src.agents.agent_factory import create_agent


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to allow specific origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
