from math import sqrt

class Maze:
    def __init__(self, size, starting_value = "0"):
        self.size = size
        self.diagonalPath = False
        self.start = None
        self.finish =  None
        self.maze = [[starting_value for x in range(size)] for y in range(size)]
    
    def setDiagonalPath(self):
        self.diagonalPath = not self.diagonalPath

    def showMaze(self):
        for y in range(self.size):
            for x in range(self.size):
                print(self.maze[x][y], end = "")
            print("")
    
    def isBorder(self, cell):
        (x, y) = cell
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return True
        return False

    def setPath(self, cell):
        (x, y) = cell
        self.maze[x][y] = "1"

    def isWall(self, cell):
        (x,y) = cell
        return (self.maze[x][y] == "X")
    
    def addWall(self, cell):
        (x, y) = cell
        self.maze[x][y] = "X"

    def addStart(self, cell):
        (x, y) = cell
        self.start = cell
        self.maze[x][y] = "A"

    def heuristic(self, start, finish):
        (x1, y1) = start
        (x2, y2) = finish
        return sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    def addFinish(self, cell):
        (x, y) = cell
        self.finish = cell
        self.maze[x][y] = "S"

    def getWeight(self, cell1, cell2):
        cell = (abs(cell1[0] - cell2[0]), abs(cell1[1] - cell2[1]))
        if cell == (1,1):
            return 1.42
        else:
            return 1
    
    def setEmpty(self, cell):
        (x, y) = cell
        self.maze[x][y] = "0"

    def reset(self):
        for x in range(self.size):
            for y in range(self.size):
                self.setEmpty((x,y))

    def isEmpty(self, cell):
        (x, y) = cell
        return self.maze[x][y] == "0"

    def getNeighbor(self, cell):
        (x, y) = cell
        if(self.diagonalPath):
            neighbor = [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]
        else:
            neighbor = [(x+1,y),(x,y+1),(x-1,y),(x,y-1),(x+1,y-1),(x-1,y+1),(x+1, y+1),(x-1,y-1)]
        neighbor = [element for element in neighbor if not self.isBorder(element) and not self.isWall(element)]
        return neighbor

 

           


