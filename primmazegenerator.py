import random as rand
from math import ceil
from datetime import datetime
from maze import *
rand.seed(datetime.now())


def getFrontier(maze, cell):
    if(not maze.isBorder(cell)):
        (x, y) = cell
        neighbor = [(x+2,y),(x,y+2),(x-2,y),(x,y-2)]
        neighbor = [element for element in neighbor if not maze.isBorder(element) and maze.isWall(element)]
        return neighbor
    return []

def getConnector(maze, cell):
    if(not maze.isBorder(cell)):
        (x, y) = cell
        neighbor = [(x+2,y),(x,y+2),(x-2,y),(x,y-2)]
        neighbor = [element for element in neighbor if not maze.isBorder(element) and not maze.isWall(element)]
        return neighbor
    return []

def setPassage(maze, cell1, cell2):
    x1,y1 = cell1
    x2,y2 = cell2

    maze.setEmpty(cell1)
    maze.setEmpty(cell2)
    
    if(x1 == x2):
        if(y1 < y2):    
            maze.setEmpty((x1,y1+1))  
        else:
            maze.setEmpty((x1,y1-1))
    if(y1 == y2):
        if(x1 < x2):
            maze.setEmpty((x1+1,y1))
        else:
            maze.setEmpty((x1-1,y1))


def randomizedPrim(height, width, starting_point):
    maze = Maze(height, width, "X")
    maze.setEmpty(starting_point)
    frontiera = getFrontier(maze, starting_point)
    
    while  len(frontiera) != 0:
        frontier_cell = frontiera[rand.randint(0, len(frontiera)-1)]
        connectors = getConnector(maze, frontier_cell)
        connect_point = connectors[rand.randint(0, len(connectors)-1)]

        if (maze.isEmpty(frontier_cell) and not maze.isEmpty(connect_point)) or (not maze.isEmpty(frontier_cell) and maze.isEmpty(connect_point)):
            setPassage(maze, frontier_cell, connect_point)
   
        for x in getFrontier(maze, frontier_cell):
            frontiera.append(x)
        
        frontiera.remove(frontier_cell)
    return maze