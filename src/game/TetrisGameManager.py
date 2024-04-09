from pynput.keyboard import Key, Listener
import time as t
import sys

from src.game.board import Action, Board

baseScore = 100
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

""" TODO:   Timer for piece drop 
            keyboard input for piece movement
            keyboard input for piece rotation
            keyboard input for piece drop
            keyboard input for game start
            soft drop and hard drop implementation
            """


class TetrisGameManager:

    currentPiece = None
    nextPiece = None
    updateTimer = 1
    streak = 1

    def __init__(self, board: Board):
        self.board = board
        self.score = 0
        self.currentTime = int(round(t.time() * 1000))

        self.switcher = {
            Key.f1: Action.SOFT_DROP,
            Key.left: Action.MOVE_LEFT,
            Key.right: Action.MOVE_RIGHT,
            Key.space: Action.DROP,
            Key.up: Action.ROTATE_CLOCKWISE,
        }

        # while True:
        #     with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
        #         listener.join()

    def onPress(self, key):
        # Default action if key not found
        default_action = lambda: "Key not recognized"

        # Get the function to execute based on the key, or default action
        action = self.switcher.get(key, default_action)
        self.movePiece(action)

    def onRelease(self, key):
        pass

    def movePiece(self, direction: Action):
        self.board.doAction(direction)
        self.board.printBoard()

    def isGameOver(self):
        return self.board.isGameOver()

    def startGame(self):
        self.currentPiece = self.newPiece()
        self.nextPiece = self.newPiece()
        self.board.printBoard()

        listener = Listener(on_press=self.onPress, on_release=self.onRelease)
        listener.start()

        while not self.board.gameOver:

            self.checkTimer()

            t.sleep(0.1)  # Add a small delay to reduce CPU usage

        # Stop the listener when the game is over
        print("Stopping listener")
        listener.stop()

    def newPiece(self):
        pass
        # return self.pieces.getNewPiece()

    def updateScore(self, linesCleared):
        self.score += self.streak * (baseScore**linesCleared)

    def checkTimer(self):
        checkTime = self.currentTime + 1000 / self.updateTimer
        newTime = int(round(t.time() * 1000))
        # if (checkTime < newTime):
        #     self.currentTime = newTime
        #     self.movePiece("DOWN")
        #     print("Timer checked")
        #     self.board.printBoard()

        return True

    def stopGame(self):
        self.board.gameOver = True
        sys.exit()
