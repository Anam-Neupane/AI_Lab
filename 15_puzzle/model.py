from random import choice

class Puzzle: 
    
    # Constraints for the 15-puzzle moves
    UP = (1,0) # they are opposite to the direction of the blank square
    # because the blank square is the one that moves to the new position
    DOWN = (-1,0)
    LEFT = (0,1)
    RIGHT = (0,-1)

    DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
    
    def __init__(self, boardSize = 4): # Default to 4x4 board
        
        self.boardSize = boardSize
        self.board = [[0] * boardSize for i in range(boardSize)] # Initialize the board with zeros creating a 2D list [0, 0, 0, 0] of boardSize rows
        self.blankPos = (boardSize - 1, boardSize - 1)
        
        for i in range(boardSize):# Fill the board with numbers from 1 to boardSize^2 - 1
            for j in range(boardSize):
                self.board[i][j] = i * boardSize + j + 1
                
        # 0 represents the blank square, init in bottom right corner of board
        self.board[self.blankPos[0]][self.blankPos[1]] = 0
        
        self.shuffle() # Shuffle the board to create a solvable puzzle
        
    #-------------------------- For Console Output ----------------------------------  
    def __str__(self): # String representation of the board for console output
        
        outStr = '' # Initialize an empty string to build the output
        for i in self.board: # Iterating through each row of the board
            outStr += '\t'.join(map(str,i)) # Join each row's elements with a tab character
            outStr += '\n' # Add a newlline after each row 
        return outStr
    
    def __getitem__(self, key): # Allows access to the board using the syntax puzzle[key]
        return self.board[key] # Returns the row at the specified index
    
    
    def shuffle(self):
        
        nofShuffles = 1000
        for i in range(nofShuffles):
            dir = choice(self.DIRECTIONS) # Randomly select a direction from the list of possible moves
            self.move(dir) # Move the blank square in the selected direction
            
    def move(self, dir):
        
        newBlankPos = (self.blankPos[0] + dir[0], self.blankPos[1] + dir[1]) # Calculate the new position of the blank square based on the direction
        
        #('\' used for new line continuation)
        if newBlankPos[0] < 0 or newBlankPos[0] >= self.boardSize or \
            newBlankPos[1] < 0 or newBlankPos[1] >= self.boardSize: # Check if the new position is out of bounds
                return False
        
        # Swap the blank square with the same square in the specified direction
        self.board[self.blankPos[0]][self.blankPos[1]] = self.board[newBlankPos[0]][newBlankPos[1]]
        self.board[newBlankPos[0]][newBlankPos[1]] = 0 
        self.blankPos = newBlankPos
        return True 
            
    def checkWin(self):
        
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.board[i][j] != i * self.boardSize + j + 1 and self.board[i][j] != 0:
                    return False
        
        return True