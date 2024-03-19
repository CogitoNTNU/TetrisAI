from pynput.keyboard import Key, Listener
import time as t
from Board import Board
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

    def __init__(self, board):
        self.board = board
        self.score = 0
        self.currentTime = int(round(t.time() * 1000))

        # while True:
        #     with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
        #         listener.join()

        
    def onPress(self, key):

        switcher = {
            Key.down: self.movePiece("DOWN"),
            Key.left: self.movePiece("LEFT"),
            Key.right: self.movePiece("RIGHT"),
            Key.space: "HardDrop",
            Key.esc: self.stopGame(),
            Key.up: self.rotatePiece("UP"),
        }

        # Default action if key not found
        default_action = lambda: "Key not recognized"

        # Get the function to execute based on the key, or default action
        switcher.get(key, default_action)
        print("_____________________________________________________")
        self.board.printBoard()
        #print(action)
        # Execute the function
        #return action

    def onRelease(self, key):
        pass

    def rotatePiece(self, direction):
        pass
        # self.currentPiece.rotate(direction)

    def movePiece(self, direction):
        if self.legalMove():
            if direction == "DOWN":
                self.board.moveBlockDown()
            elif direction == "LEFT":
                self.board.moveBlockLeft()
            elif direction == "RIGHT":
                self.board.moveBlockRight()

        # if self.legalMove():
        #     self.board.moveBlockDown(direction)

    def dropPiece(self, newPiece):
        self.movePiece("DOWN")

    def isGameOver(self):
        return self.board.validMove()
        #return self.board.isGameOver()

    def startGame(self):
        self.currentPiece = self.newPiece()
        self.nextPiece = self.newPiece()
        self.board.printBoard()

        with Listener(
        on_press=self.onPress,
        on_release=self.onRelease) as listener:
            listener.join()
            while not self.isGameOver():
                #action = input("Enter action: ") ## valid commands: [moveLeft, moveRight, moveDown, softDrop, hardDrop, quitGame, rotateLeft, rotateRight, rotate180]
                if action == "moveLeft" and self.legalMove():
                    self.movePiece(LEFT)
                elif action == "moveRight" and self.legalMove():
                    self.movePiece(RIGHT)
                elif action == "moveDown" and self.legalMove():
                    self.dropPiece(DOWN)
                elif action == "softDrop":
                    self.softDrop()
                elif action == "h":
                    self.hardDrop()
                elif action == "rotateLeft":
                    self.rotatePiece(-1)
                elif action == "rotateRight":
                    self.rotatePiece(1)
                elif action == "rotate180":
                    self.rotatePiece(2)
                elif action == "q":
                    self.stopGame()
                    break
                else:
                    self.checkTimer()
                
                t.sleep(0.1)  # Add a small delay to reduce CPU usage
            
            # Stop the listener when the game is over
            listener.stop()

        

    def newPiece(self):
        pass
        #return self.pieces.getNewPiece()

    def legalMove(self):
        return self.board.validMove()

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
        if self.isGameOver():
            self.stopGame()
            return True
        clearLines = self.board.checkGameState()
        if clearLines:
            self.board.clearLines(clearLines)
            self.updateScore(clearLines)
        return True
        
    
    def checkTimer(self):
        checkTime = self.currentTime + 1000
        newTime = int(round(t.time() * 1000))
        if (checkTime > newTime):
            self.movePiece("DOWN")
            print("Timer checked")

        
        return True
        
    def stopGame(self):
        print("Game Over")
        sys.exit()
        self.board.stop_game()

if __name__ == "__main__":
    board = Board()
    game = TetrisGameManager(board)
    game.startGame()

