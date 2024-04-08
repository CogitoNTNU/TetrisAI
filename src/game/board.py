import pygame
import random
import copy
from block import Block

'''
Denne skriver ut brettet i terminal bare. 
Vi lager brettet med en matrise. Det er 0 overalt i matrisen. legger du en brikke så nendrer vi i matrisen.
Dersom en hel rad i matrisen er full, så fjerner vi denne raden og flytter alt sammen nedover + oppdatererr poengsummen"
En brikke i matrisen represneteres med 1-er. 
'''

class Board:
    rows = 20
    columns = 10
    gameOver = False
    rowsRemoved = 0
    board=[]
    block= None
    # block = Block(0,5, random.randint(0,6)) #random.randint(0,6) er for å velge en tilfeldig brikke

    def __init__(self):
        for i in range(0,self.rows-1):
            newLine= []
            for j in range(0,self.columns-1):
                newLine.append(0)
            self.board.append(newLine)

        self.prevBoard = copy.deepcopy(self.board)

        self.block = Block(3,0,0)
        # self.block = Block(3,0, random.randint(0,6))
        self.placeBlock()

    def printBoard(self):
        print("___________________________________")
        for row in self.board:
            print('|' + '   '.join(self.checkCharacter(cell) for cell in row) + '|')
        
        print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

    def checkCharacter(self, character):
        if character == 1:
            return '■'
        else:
            return '▧'



    def rotateBlockRight(self):
        if self.validMove(self.block.rotateRight):
            self.placeBlock()
          

            
    def moveBlockDown(self):
        if self.validMove(self.block.moveDown):
            self.placeBlock()
     

    
    def moveBlockLeft(self):
        if self.validMove(self.block.moveLeft):
            self.placeBlock()
      
        
            
    def moveBlockRight(self): 
        if self.validMove(self.block.moveRight):
            self.placeBlock()
          
         
        
    def rotateBlockLeft(self):
        if self.validMove(self.block.rotateLeft):
            self.placeBlock()
          
                
    def gameOver(self):
        return self.gameOver

    def setGameOver(self,state):
        self.gameOver = state

    
    

    
    def blockLanded(self):
        
        pass

   



    # def validMove(self):
    #     for i in range(4):
    #         for j in range(4):
    #             if i * 4 + j in self.block.image():
    #                 if i + self.block.y > self.rows - 1 or \
    #                         j + self.block.x > self.columns - 1 or \
    #                         j + self.block.x < 0 or \
    #                         self.board[i + self.block.y][j + self.block.x] > 0:
    #                     return False  # Returnerer False ved kollisjon eller ugyldig trekk

    def validMove(self, simulateimulatedMove):
        # if simulated move fails = move out of bounds and should be disallowed
        simulateimulatedMove()
        
        for row in range(4, 1, -1):
            for column in range(4, 1, -1):
                if row * 4 + column in self.block.image():
                    if (
                        row + self.block.y > self.rows - 1 or
                        row + self.block.y < 0 or
                        column + self.block.x > self.columns - 1 or
                        column + self.block.x < 0 or
                        self.prevBoard[row + self.block.y][column + self.block.x] > 0
                       ):
                        simulateimulatedMove(Undo = True)
                        return False
        return True  # Return True if the move is valid


    def clearRow(self, rownumber):
        # Fjerner den angitte raden og legger til en ny tom rad ved bunnen av matrisen
        newMatrix = self.board[:rownumber] + self.board[rownumber+1:]
        newMatrix.append([0 for _ in range(self.columns)])
        self.matrix = newMatrix  # Oppdaterer matrisen med den nye matrisen
        self.rowsRemoved += 1  # Oppdaterer antall fjernede rader

        
    def checkGameState(self):
        amount = 0
        fullRows = []

        for rowIndex, row in enumerate(self.board):   # Itererer over matrisen for å finne fulle rader
            if 0 not in row:  # Sjekker om raden er full
                fullRows.append(rowIndex)  # Legger til indeksen til listen over fulle rader
       
        for rowIndex in reversed(fullRows):  # Går gjennom listen over fulle rader i reversert rekkefølge for å fjerne dem
            self.clearRow(rowIndex)  # Fjerner raden basert på dens indeks
            amount += 1  # Øker telleren for antall fjernede rader
        return amount   # Returnerer totalt antall fjernede rader

    
    def placeBlock(self):
        self.board = copy.deepcopy(self.prevBoard)
        # if self.validMove():
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.image():
                    self.board[i + self.block.y][j + self.block.x] = 1 #self.block.color
        return self.checkGameState() #hvis denne sjekkes hver gang og gir false, var det ikke mulig å plassere blokken og spillet er over ffs.
    
    def newBlock(self):
        self.block = Block(0,5, random.randint(0,6))
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.image():
                    self.board[i + self.block.y][j + self.block.x] = 1 #self.block.color
        return self.checkGameState() #hvis denne sjekkes hver gang og gir false, var det ikke mulig å plassere blokken og spillet er over ffs.

    


    

    


    
