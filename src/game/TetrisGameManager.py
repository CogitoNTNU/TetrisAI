import keyboard

baseScore = 100
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class TetrisGameManager:

    currentPiece = None
    nextPiece = None
    score = 0
    updateTimer = 1
    streak = 1

    def __init__(self, board):
        self.board = board
        self.score = 0

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

    def newPiece(self):
        return self.pieces.getNewPiece()

    def legalMove(self, x, y):
        return self.board.legalMove(x, y)

    def clearLines(self):
        linesCleared = self.board.checkGameState()
        if linesCleared == 4:
            self.streak += 1
        else:
            self.streak = 1
            
        self.updateScore(linesCleared)

    def updateScore(self, linesCleared):
        self.score += self.streak*(baseScore**linesCleared)

    def placePiece(self, direction):
        x = direction[0]
        y = direction[1]
        if self.legalMove(x, y):
            self.board.placePiece(x, y, self.currentPiece)
            self.currentPiece = self.nextPiece
            self.next_piece = self.nextPiece()
        if self.isGameOver():
            self.stopGame()
        
        
    def stopGame(self):
        self.board.stop_game()