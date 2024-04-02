import pygame
import random
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
    block = Block(0,5, random.randint(0,6)) #random.randint(0,6) er for å velge en tilfeldig brikke

    def __init__(self):
        for i in range(0,self.rows-1):
            newLine= []
            for j in range(0,self.columns-1):
                newLine.append(0)
            self.board.append(newLine)

        self.block = Block(0,5, random.randint(0,6))


    def printBoard(self):
        for row in self.board:
            print((' ').join(str(row)))


    def rotateBlockRight(self):
        if self.block.rotateRight().validMove():
            self.placeBlock(self.block.rotate_right())

            
    def moveBlockDown(self):
        if self.block.moveDown().validMove():
            self.placeBlock(self.block.move_down())
     

    
    def moveBlockLeft(self):
        if self.block.moveLeft().validMove():
            self.placeBlock(self.block.move_left())
        
            
    def moveBlockRight(self): 
        if self.block.moveRight().validMove():
            self.placeBlock(self.block.move_right())
         
        
    def rotateBlockLeft(self):
        if self.block.rotateLeft().validMove():
            self.placeBlock(self.block.rotate_left())
          
                
    def gameOver(self):
        return self.gameOver

    def validMove(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.image():
                    if i + self.block.y > self.rows - 1 or \
                            j + self.block.x > self.columns - 1 or \
                            j + self.block.x < 0 or \
                            self.board[i + self.block.y][j + self.block.x] > 0:
                        return False  # Returnerer False ved kollisjon eller ugyldig trekk


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
        if not self.block.validMove():
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.block.image():
                        self.board[i + self.block.x][j + self.block.y] = 1 #self.block.color
        return self.checkGameState() #hvis denne sjekkes hver gang og gior false, var det ikke mulig å plassere blokken og spillet er over ffs.
    
    






















