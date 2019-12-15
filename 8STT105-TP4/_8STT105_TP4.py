import sys
from tkinter import *
from time import sleep
from secrets import randbelow

doRenderTk = True #Enable graphic rendering
windowSize = (1280, 960)
backgroundColor = "white"
points = []

class Model(object):
    def __init__(self, master = None):
        self.initModel()
        points.append((self.x, self.y)) #Mark the first point as visited
        if master is not None: #Graphic rendering
            self.frame = Frame(master)
            self.frame.pack()
            self.bframe = Frame(self.frame)
            self.bframe.pack(side = TOP)
            self.gframe = Frame(self.frame, bd = 2, relief = RAISED)
            self.g = Canvas(self.gframe, bg = backgroundColor, width = windowSize[0], height = windowSize[1]) 
            self.g.pack()
            self.g.bind("<ButtonPress-1>", self.onClick1) #Left click
            self.g.bind("<ButtonPress-2>", self.onClick2) #Middle click
            self.g.bind("<ButtonPress-3>", self.onClick3) #Right click
            self.gframe.pack(side = TOP)
            self.g.delete(ALL)
        else: 
            self.g = None

    def onClick2(self, event):
        #Sleep from 1 to 60s on middle click
        sleep(int(60 * event.x // windowSize[0]) + 1)

    def onClick1(self, event):
        #Slow down from 0 to 100% on left click
        self.tick *= 1.0 + event.x / windowSize[0]

    def onClick3(self, event):
        #Speed up from 0 to 100% on right click
        self.tick *= 0.5 * event.x / windowSize[0]

    def initModel(self):
        #Core
        self.tick = 0.1 #Global speed
        self.n = 1000 #Number of step (while i < n)
        self.i = 0 #Current step
        self.x = 628 #Start X
        self.y = 468 #Start Y
        self.lineLength = 10 #Determine the x and y move size even in non-graphic mode
        self.lineSpacing = 0 #Determine the x and y added padding (on top of lineLength) even in non-graphic mode

        #Graphic
        self.orientation = 0 #0=N, 1=W, 2=S, 3=E
        self.borderWidth = 2
        self.lineColorDefault = "gray5"
        self.lineColor = "medium sea green" #Set different than default to highlight the first line
        self.lineColorEnd = "indian red"
        self.lineColorActive = "gold"
        self.clearAfterEach = False #Disable to see a path forming

    def update(self): #Model update after each tick
        previousOrientation = self.orientation
        previousX = self.x
        previousY = self.y

        first = True
        while first or (self.orientation != previousOrientation and (self.orientation % 2 == previousOrientation % 2)) or ((self.x, self.y) in points):
            first = False
            self.orientation = randbelow(4)

            if self.orientation == 0: #North
                self.x = previousX
                self.y = previousY + (self.lineLength + self.lineSpacing)
            elif self.orientation == 1: #West
                self.x = previousX + (self.lineLength + self.lineSpacing)
                self.y = previousY
            elif self.orientation == 2: #South
                self.x = previousX
                self.y = previousY - (self.lineLength + self.lineSpacing)
            elif self.orientation == 3: #East
                self.x = previousX - (self.lineLength + self.lineSpacing)
                self.y = previousY

        points.append((self.x, self.y))

    def render(self, g): #Render a box at the current coordinates
        if self.orientation == 0: #North
            line = (self.x, self.y, self.x, self.y - self.lineLength)
            line2 = (self.x, self.y, self.x, self.y - 2)
        elif self.orientation == 1: #West
            line = (self.x, self.y, self.x - self.lineLength, self.y)
            line2 = (self.x, self.y, self.x - 2, self.y)
        elif self.orientation == 2: #South
            line = (self.x, self.y, self.x, self.y + self.lineLength)
            line2 = (self.x, self.y, self.x, self.y + 2)
        elif self.orientation == 3: #East
            line = (self.x, self.y, self.x + self.lineLength, self.y)
            line2 = (self.x, self.y, self.x + 2, self.y)

        g.create_line(line, width = self.borderWidth, fill = self.lineColor)
        g.create_line(line2, width = self.borderWidth, fill = self.lineColorEnd)

    def run(self): #Boucle de simulation de la dynamique
        for self.i in range(self.n):
            if self.g is not None: #Pre-rendering
                if self.i - 1 > 0 and not self.clearAfterEach:
                    self.i -= 1
                    self.lineColor = self.lineColorDefault
                    self.render(self.g)
                    self.i += 1
                elif self.clearAfterEach:
                    self.g.delete(ALL)

            self.update() 

            if self.g is not None: #Rendering
                if self.i == self.n - 1:
                    self.lineColor = self.lineColorEnd
                elif self.i > 0:
                    self.lineColor = self.lineColorActive

                self.render(self.g)
                self.g.update()
                sleep(self.tick)

#Execute on run, not on import
if __name__ == '__main__':
    if doRenderTk: #Graphic rendering enabled
        root = Tk()
        root.geometry("+0+0")
        root.title("8STT105-TP4")
    else: 
        root = None
    x = Model(root)
    x.run()
    if root is not None: 
        root.mainloop()
