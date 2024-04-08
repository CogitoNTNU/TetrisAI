from pynput.keyboard import Key, Listener
import time as t
from board import Board
import sys


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
    score = 0
    updateTimer = 1
    streak = 1
    currentTime = None
    board = None
    switcher = None

    def __init__(self, board):
        self.board = board
        self.score = 0
        self.currentTime = int(round(t.time() * 1000))
        self.board.setGameOver(False)

        self.switcher = {
            Key.f1: lambda: self.movePiece("DOWN"),
            Key.left: lambda: self.movePiece("LEFT"),
            Key.right: lambda: self.movePiece("RIGHT"),
            Key.space: lambda: "HardDrop",
            Key.esc: lambda: self.stopGame(),
            Key.up: lambda: self.movePiece("UP"),
        }

        # while True:
        #     with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
        #         listener.join()

        
    def onPress(self, key):

        # Default action if key not found
        default_action = lambda: "Key not recognized"

        # Get the function to execute based on the key, or default action
        action = self.switcher.get(key, default_action)
        action()
        #self.board.printBoard()
        #print(action)
        # Execute the function
        #return action

    def onRelease(self, key):
        pass

    # def rotatePiece(self, direction):
    #     if direction == "UP":
    #         self.board.rotateBlockRight()
    #     self.board.printBoard()
    #     # self.currentPiece.rotate(direction)

    def movePiece(self, direction):
        print(direction)
        if direction == "DOWN":
            self.board.moveBlockDown()
        elif direction == "LEFT":
            self.board.moveBlockLeft()
        elif direction == "RIGHT":
            self.board.moveBlockRight()
        elif direction == "UP":
            self.board.rotateBlockRight()

        self.board.printBoard()

    def dropPiece(self, newPiece):
        self.movePiece("DOWN")

    def isGameOver(self):
        return self.board.isGameOver()
        #return self.board.isGameOver()

    def startGame(self):
        self.currentPiece = self.newPiece()
        self.nextPiece = self.newPiece()
        self.board.printBoard()

        listener = Listener(
            on_press=self.onPress, 
            on_release=self.onRelease)
        listener.start()

        while not self.board.gameOver:
            
            self.checkTimer()
            
            t.sleep(0.1)  # Add a small delay to reduce CPU usage
            
        # Stop the listener when the game is over
        print("Stopping listener")
        listener.stop()

        

    def newPiece(self):
        pass
        #return self.pieces.getNewPiece()

    # def clearLines(self):
    #     linesCleared = self.board.checkGameState()
    #     if linesCleared == 4:
    #         self.streak += 1
    #     else:
    #         self.streak = 1
              

    def updateScore(self, linesCleared):
        self.score += self.streak*(baseScore**linesCleared)

    def softDrop(self):
        if self.legalMove(DOWN):
            self.dropPiece()
        else:
            self.placePiece(DOWN)

    def hardDrop(self):
        while self.legalMove(DOWN):
            self.dropPiece()
        self.placePiece(DOWN)

    def placePiece(self, direction):
        x = direction[0]
        y = direction[1]
        if not self.legalMove(x, y):
            self.board.placePiece(x, y, self.currentPiece)
            self.currentPiece = self.nextPiece
            self.next_piece = self.nextPiece()
        else:
            self.movePiece(DOWN)
            return False
        if self.board.gameOver:
            self.stopGame()
            return True
        clearLines = self.board.checkGameState()
        if clearLines:
            self.board.clearLines(clearLines)
            self.updateScore(clearLines)
        return True
        
    
    def checkTimer(self):
        checkTime = self.currentTime + 1000/self.updateTimer
        newTime = int(round(t.time() * 1000))
        # if (checkTime < newTime):
        #     self.currentTime = newTime
        #     self.movePiece("DOWN")
        #     print("Timer checked")
        #     self.board.printBoard()

        
        return True
        
    def stopGame(self):
        #print("Game Over")
        self.board.setGameOver(True)
        sys.exit()

if __name__ == "__main__":
    board = Board()
    game = TetrisGameManager(board)
    game.startGame()

