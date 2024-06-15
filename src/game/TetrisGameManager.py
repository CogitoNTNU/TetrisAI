from copy import deepcopy
import pygame
from pygame.locals import *
import time as t
import sys

from src.agents.agent import Agent, playGameDemoStepByStep
from src.game.tetris import Action, Tetris
from src.game.block import COLORS

baseScore = 100

# pygame visuals setup
BLOCK_SIZE = 40
WIDTH = 10
HEIGHT = 23
START_HEIGHT = 3
SCREEN_WIDTH = WIDTH * BLOCK_SIZE
SCREEN_HEIGHT = (HEIGHT - START_HEIGHT) * BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class TetrisGameManager:
    currentPiece = None
    nextPiece = None
    updateTimer = 1
    streak = 1

    def __init__(self, board: Tetris):
        self.board = board
        self.score = 0
        self.currentTime = int(round(t.time() * 1000))

    def movePiece(self, direction: Action):
        self.board.doAction(direction)
        self.board.printBoard()

    def isGameOver(self):
        return self.board.isGameOver()

    def startGame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")  # Set window title

        clock = pygame.time.Clock()

        while not self.board.gameOver:
            self.draw_board(self.board)
            self.inputHandling()
            if self.board.blockHasLanded:
                self.board.updateBoard()  # Update the board after a block has landed and spawn a new block
            self.checkTimer()
            pygame.display.update()
            clock.tick(60)  # Cap the frame rate to 60 FPS

        self.stopGame()

    def startDemo(self, agent: Agent):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")  # Set window title

        clock = pygame.time.Clock()

        while not self.board.gameOver:
            self.draw_board(self.board)
            playGameDemoStepByStep(agent, self.board)
            pygame.display.update()
            clock.tick(60)  # Cap the frame rate to 60 FPS

        self.stopGame()

    def inputHandling(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.stopGame()
            else:
                keys = pygame.key.get_pressed()
                if keys[K_DOWN]:
                    self.movePiece(Action.SOFT_DROP)
                elif keys[K_LEFT]:
                    self.movePiece(Action.MOVE_LEFT)
                elif keys[K_RIGHT]:
                    self.movePiece(Action.MOVE_RIGHT)
                elif keys[K_SPACE]:
                    self.movePiece(Action.HARD_DROP)
                elif keys[K_UP]:
                    self.movePiece(Action.ROTATE_CLOCKWISE)

    def checkTimer(self):
        checkTime = self.currentTime + 1000 / self.updateTimer
        newTime = int(round(t.time() * 1000))
        if checkTime < newTime:
            self.currentTime = newTime
            self.movePiece(Action.SOFT_DROP)

    def draw_board(self, gameState: Tetris):
        self.screen.fill(BLACK)
        temp = deepcopy(gameState)
        temp_board = temp.board[START_HEIGHT:]
        for y in range(HEIGHT - START_HEIGHT):
            for x in range(WIDTH):
                if temp_board[y][x] != 0:
                    pygame.draw.rect(
                        self.screen,
                        COLORS[temp_board[y][x] - 1],
                        (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    )
                pygame.draw.rect(
                    self.screen,
                    WHITE,
                    (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    1,
                )

    def stopGame(self):
        pygame.quit()
        sys.exit()
