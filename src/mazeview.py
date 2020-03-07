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
    def __init__(self, window, height,  width,rect_size=25):
        self.rect_size = rect_size
        self.window = window
        self.height = height
        self.width = width
        self.canvas = tkinter.Canvas(self.window, width=self.width*self.rect_size+1, height=self.width*self.rect_size+1, highlightthickness=1, background='#fbfef9')
        self.canvas.pack(side='left')
        self.board = None
        
        self.visited = []
        self.path = None
        self.path_counter = 0
        self.visited_counter = 0
        
        self.board = None
        self.finish = (-1,-1)
        self.start = (-1,-1)
    
        self.generateBoard()

    
    def generateBoard(self):
        self.board = [[None for x in range(self.width)] for y in range(self.height)]

        for x in range(self.height):
            for y in range(self.width):
                rect = Rectangle(self.canvas,y*self.rect_size,x*self.rect_size, (y*self.rect_size+self.rect_size), (x*self.rect_size+self.rect_size))
                rect.changeOutline('black')
                self.board[x][y] = rect

    def setWall(self, position):
        (x,y) = position
        self.board[x][y].changeFill('#191923')
                         
    def setStart(self, position):
        x,y = position
        oldx,oldy = self.start
        self.board[oldx][oldy].reset()
        self.board[x][y].changeFill('#44cf6c')
        self.start = (x,y)

    def setFinish(self,position):
        x,y = position
        oldx,oldy = self.finish
        self.board[oldx][oldy].reset()
        self.board[x][y].changeFill('#ff8484')
        self.finish = (x,y)

    def generatePath(self, path, closed_list):
        self.path,self.visited = path, closed_list
        self.path.reverse()
        self.updateVisited() 

    def clickedBox(self,x,y):  
        return int(y/self.rect_size),int(x/self.rect_size)

    def isStart(self, position):
        return position == self.start

    def isFinish(self, position):
        return position == self.finish
       
    def updatePath(self):
        position = self.path[self.path_counter]
        self.path_counter = self.path_counter + 1

        if not self.isStart(position) and not self.isFinish(position):
            x,y = position
            self.board[x][y].changeFill('yellow')

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
            self.board[x][y].changeFill('gray')

        if self.visited_counter == len(self.visited):
            self.visited_counter = 0
            self.visited = None
            self.updatePath()
        else:
            self.window.after(5, self.updateVisited)

    def reset(self):
        self.finish = (-1,-1)
        self.start = (-1,-1)
        for x in range(self.height):
            for y in range(self.width):
                self.board[x][y].reset()

    def randomBoard(self, maze):
        self.setStart(maze.start)
        self.setFinish(maze.finish)
        for x in range (maze.height):
            for y in range(maze.width):
                if maze.maze[x][y] == "X":
                    self.setWall((x,y))




class MazeWindowController:
    def __init__(self, title, maze, rect_size = 25):  
        self.rect_size = rect_size
        self.maze = maze
        self.height, self.width = self.generateWindowSize(maze)
        self.window = tkinter.Tk()
        photo = tkinter.PhotoImage(file="./images/icon.png")
        self.window.iconphoto(False, photo)
        self.window.title(title)
        self.canvas = MazeCanvas(self.window, self.maze.height, self.maze.width, self.rect_size)
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

    def generateSize(self, height, width):
        return str(height)+"x"+str(width)

    def generateWindowSize(self, maze):
        return (self.maze.height * self.rect_size + 1, self.maze.width * self.rect_size + 1)

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
        
        if(event.char == 'd'):
            self.maze.setDiagonalPath()

        if(event.char == 'g'):
            self.maze = randomizedPrim(self.maze.height, self.maze.width, (0,0))
            self.maze.addStart((0,0))
            self.maze.addFinish((self.maze.height -1, self.maze.width -1))
            self.editModeOn = False
            self.canvas.reset()
            self.canvas.randomBoard(self.maze)

    def show(self):
        self.window.mainloop()



def main():
    height = 27
    width = 37
    rect_size = 25
    if(len(sys.argv) == 4):
        height = int(sys.argv[1])
        width = int(sys.argv[2])
        rect_size = int(sys.argv[3])

    maze = mazelib.Maze(height, width)
    window = MazeWindowController("A* Visualizer", maze, rect_size)
    window.show()

main()
