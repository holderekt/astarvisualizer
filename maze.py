from math import sqrt

class Maze:
    def __init__(self, size):
        self.size = size
        self.maze = [["0" for x in range(size)] for y in range(size)]
    
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
        self.maze[y][x] = "1"

    def isWall(self, cell):
        (x,y) = cell
        return (self.maze[y][x] is "X")
    
    def addWall(self, cell):
        (x, y) = cell
        self.maze[y][x] = "X"

    def addStart(self, cell):
        (x, y) = cell
        self.maze[y][x] = "A"

    def heuristic(self, start, finish):
        (x1, y1) = start
        (x2, y2) = finish
        return sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    def addFinish(self, cell):
        (x, y) = cell
        self.maze[y][x] = "S"

    def getWeight(self, cell1, cell2):
        cell = (abs(cell1[0] - cell2[0]), abs(cell1[1] - cell2[1]))
        if cell == (1,1):
            return 1.42
        else:
            return 1
    
    def setEmpty(self, cell):
        (x, y) = cell
        self.maze[y][x] = "0"

    def reset(self):
        for x in range(self.size):
            for y in range(self.size):
                self.setEmpty((x,y))

    def getNeighbor(self, cell):
        (x, y) = cell
        neighbor = [(x+1,y),(x,y+1),(x-1,y),(x,y-1),(x+1,y-1),(x-1,y+1),(x+1, y+1),(x-1,y-1)]
        neighbor = [element for element in neighbor if not self.isBorder(element) and not self.isWall(element)]
        return neighbor


