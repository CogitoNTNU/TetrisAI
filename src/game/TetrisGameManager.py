from pynput.keyboard import Key, Listener
import time as t

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

    def __init__(self, board):
        self.board = board
        self.score = 0
        self.currentTime = int(round(t.time() * 1000))

        # while True:
        #     with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
        #         listener.join()

        
    def onPress(self, key):
        switcher = {
    
        }
    
    def onRelease(self, key):
        pass


    def rotatePiece(self, direction):
        self.currentPiece.rotate(direction)


    def movePiece(self, direction):

        if self.legalMove(direction):
            self.currentPiece.move(direction)

    def dropPiece(self, newPiece):
        self.movePiece(DOWN)

    def isGameOver(self):
        return self.board.isGameOver()

    def startGame(self):
        self.currentPiece = self.newPiece()
        self.nextPiece = self.newPiece()
        
        while not self.isGameOver():
            action = input("Enter action: ") ## valid commands: [moveLeft, moveRight, moveDown, softDrop, hardDrop, quitGame, rotateLeft, rotateRight, rotate180]
            if action == "moveLeft" and self.legalMove(LEFT):
                self.movePiece(LEFT)
            elif action == "moveRight" and self.legalMove(RIGHT):
                self.movePiece(RIGHT)
            elif action == "moveDown" and self.legalMove(DOWN):
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
                self.moveDown()


        

    def newPiece(self):
        return self.pieces.getNewPiece()

    def legalMove(self, x, y):
        return self.board.legalMove(x, y)

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
            self.movePiece(DOWN)

        
        return True
        
    def stopGame(self):
        self.board.stop_game()


    if __name__ == "__main__":
        millisec = int(round(t.time() * 1000))
        print(millisec)