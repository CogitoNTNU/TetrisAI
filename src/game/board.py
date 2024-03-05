import pygame

'''
Vi lager brettet med en matrise. Det er O overalt i matrisen. legger du en brikke så nendrer vi i matrisen.
Dersom en hel rad i matrisen er full, så fjerner vi denne raden og flytter alt sammen nedover + oppdatererr poengsummen"
En brikke i matrisen represneteres med x-er. 
'''

class Board:
    rows = 20
    columns = 10
    gameOver = False
    rowsRemoved = 0

    def __init__(self):
        self.matrix = [["O" for _ in range(self.columns)] for _ in range(self.rows)]

    def print_matrix(self):
        for row in self.matrix:
            print(' '.join(row))
            
    def placeBlock(self, block):
        if block.isValidMove():
            block.position = [(x,y),(x,y)(x,y),(x,y)]
            
            for gridPositions in block.position:
                for x, y in gridPositions:
                    self.matrix[x][y] = "X"
                    
            #logikk for å sette tilbake til 0
        
    def rotater_brikke(self):
        self.plaser_brikke(self, center, block, rotation +1)
            
    def gameOver(self):
        return self.gameOver
        
    def isvalidMove(self, block):
        #block.position
        #block skal gi oss 4 kordinater
        #hvis kordinatene er ledig, returer true
        
        pass
    
    def clearRow(self, rownumber): #tar vare på alt under randen som skal fjernes og legger alt over den som skal fjernes over + lager ny tom rad
        newMatrix = self.matrix[0, rownumber] + self.matrix[rownumber+1, self.rows] + ["O" for _ in range(self.columns)]
        self.Matrix = newMatrix
        rowsRemoved += 1
        
    def checkGameState(self): #itterer over alle rader og sjekker om de er fulle. fjerner alle som er fulle og teller hvor mange på rad som ble fjernet
        amount = 0
        for row in self.matrix:
            if "O" not in row:
                self.clearRow(row)
                amount += 1
        return amount
    
    
    
#     def plaser_brikke():
#         def plaser_brikke(self):
#             # Choose a random position on the board to place the brick.
#             row = random.randint(0, self.rows - 1)
#             col = random.randint(0, self.columns - 1)
            
#             # Place the brick on the board.
#             self.board[row][col] = 1
            
#             # Print the updated board.
#             self.print_board()''
    

# # Create an instance of the Board class.

my_board = Board()
my_board.print_matrix()
