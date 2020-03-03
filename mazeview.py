import tkinter 
import maze as mazelib
import astarsearch as asslib
from queue import PriorityQueue
from primmazegenerator import randomizedPrim
import sys



class Rectangle:
    def __init__(self, canvas, x1, y1, x2, y2):
        self.canvas = canvas
        (self.x1, self.y1) = (x1,y1)
        (self.x2, self.y2) = (x2, y2)
        self.colorFill = None
        self.rectangle = self.canvas.create_rectangle(self.x1,self.y1, self.x2, self.y2)

    def changeFill(self, color):
        self.canvas.itemconfig(self.rectangle, fill=color)
        self.colorFill = color

    def changeOutline(self, color):
        self.canvas.itemconfig(self.rectangle, outline=color)

    def reset(self):
        self.changeFill('')


class MazeCanvas:
    def __init__(self, size ,window, width, height):
        self.window = window
        self.size = size
        self.canvas = tkinter.Canvas(self.window, width=width, height=height, highlightthickness=0, background='#fbfef9')
        self.canvas.pack(side='left')
        self.board = None
        
        self.visited = []
        self.path = None
        self.path_counter = 0
        self.visited_counter = 0
        
        self.board = None
        self.finish = (-1,-1)
        self.start = (-1,-1)
    
        self.generateBoard(size)

    
    def generateBoard(self, size):
        self.board = [[None for x in range(size)] for y in range(size)]
        for x in range(size):
            for y in range(size):
                rect = Rectangle(self.canvas,x*25,y*25, (x*25+25), (y*25+25))
                rect.changeOutline('black')
                self.board[x][y] = rect

    def setWall(self, position):
        (x,y) = position
        self.board[y][x].changeFill('#191923')
                         
    def setStart(self, position):
        x,y = position
        oldx,oldy = self.start
        self.board[oldy][oldx].reset()
        self.board[y][x].changeFill('#44cf6c')
        self.start = (x,y)

    def setFinish(self,position):
        x,y = position
        oldx,oldy = self.finish
        self.board[oldy][oldx].reset()
        self.board[y][x].changeFill('#ff8484')
        self.finish = (x,y)

    def generatePath(self, path, closed_list):
        self.path,self.visited = path, closed_list
        self.path.reverse()
        self.updateVisited() 

    def clickedBox(self,x,y):  
        return int(y/25),int(x/25)

    def isStart(self, position):
        return position == self.start

    def isFinish(self, position):
        return position == self.finish
       
    def updatePath(self):
        position = self.path[self.path_counter]
        self.path_counter = self.path_counter + 1

        if not self.isStart(position) and not self.isFinish(position):
            x,y = position
            self.board[y][x].changeFill('yellow')

        if(self.path_counter < len(self.path)):
            self.window.after(50, self.updatePath)
        else:
            self.path_counter = 0
            self.path = None

    def updateVisited(self):
        position = self.visited[self.visited_counter]
        self.visited_counter = self.visited_counter + 1

        if not self.isStart(position) and not self.isFinish(position):
            x,y = position
            self.board[y][x].changeFill('gray')

        if self.visited_counter == len(self.visited):
            self.visited_counter = 0
            self.visited = None
            self.updatePath()
        else:
            self.window.after(10, self.updateVisited)

    def reset(self):
        self.finish = (-1,-1)
        self.start = (-1,-1)
        for x in range(self.size):
            for y in range(self.size):
                self.board[x][y].reset()

    def randomBoard(self, maze):
        maze.showMaze()
        for x in range (maze.size):
            for y in range(maze.size):
                if maze.maze[x][y] == "X":
                    self.setWall((x,y))




class MazeWindowController:
    def __init__(self, title, maze):  
        self.maze = maze
        self.width, self.height = self.generateWindowSize(maze)
        self.window = tkinter.Tk()
        self.window.title(title)
        self.canvas = MazeCanvas(self.maze.size, self.window, self.width, self.height)
        self.configureWindow()
        self.configureBinding()
        self.editModeOn = False
  
    def changeEditMode(self):
        self.editModeOn = not self.editModeOn

    def configureWindow(self):
        self.window.configure(background='#fbfef9')
        self.window.geometry(self.generateSize(self.width, self.height))
        self.window.resizable(width = False, height = False)
    
    def configureBinding(self):
        self.window.bind_all('<Key>', self.keyPressed)
        self.canvas.canvas.bind('<B1-Motion>', self.updateWall)
        self.canvas.canvas.bind('<Double-Button-1>', self.updateFinish)
        self.canvas.canvas.bind('<Button-3>', self.updateStart)

    def updateWall(self, event):
        if self.editModeOn is True:
            position = self.canvas.clickedBox(event.x, event.y)
            if not self.canvas.isStart(position) and not self.canvas.isFinish(position):
                self.canvas.setWall(position)
                self.maze.addWall(position)
                
    def updateStart(self, event):
        position = self.canvas.clickedBox(event.x, event.y)
        self.maze.setEmpty(self.canvas.start)
        self.maze.addStart(position)
        self.canvas.setStart(position)

    def updateFinish(self, event):
        position = self.canvas.clickedBox(event.x, event.y)
        self.maze.setEmpty(self.canvas.finish)
        self.maze.addFinish(position)
        self.canvas.setFinish(position)

    def generateSize(self, width, height):
        return str(width)+"x"+str(height)

    def generateWindowSize(self, maze):
        return (self.maze.size * 25 + 1, self.maze.size * 25 + 1)

    def keyPressed(self, event):
        if(event.char == 'm'):
            self.changeEditMode()

        if(event.char == 'c'):
            path,closed_list = asslib.AstarSearch(self.canvas.start,self.canvas.finish, self.maze)
            for item in path:
                self.maze.setPath(item)
            self.canvas.generatePath(path, closed_list)

        if(event.char == 'r'):
            self.editModeOn = False
            self.maze.reset()
            self.canvas.reset()

        if(event.char == 'g'):
            self.maze = randomizedPrim(self.maze.size, (0,0))
            self.maze.showMaze()
            self.editModeOn = False
            self.canvas.reset()
            self.canvas.randomBoard(self.maze)

    def show(self):
        self.window.mainloop()



def main():
    if(len(sys.argv) != 2 or sys.argv[1] is None):
        size = 21
    else:
        size = int(sys.argv[1])

    maze = mazelib.Maze(size)
    
    window = MazeWindowController("A* Visualizer", maze)
    window.show()

main()
