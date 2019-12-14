import sys
from tkinter import *
from time import sleep

doRenderTk = True #Enable graphic rendering
windowSize = (1280, 960)
backgroundColor = "white"

class Modele(object):
    def __init__(self, master = None):
        self.initModel()
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
        self.tick = 1.0 #Global speed
        self.n = 10 #Number of step (while i < n)
        self.i = 0 #Current step
        self.x = 628 #Start X
        self.y = 468 #Start Y
        self.boxSize = 25 #Determine the x and y move size even in non-graphic mode
        self.spacing = 2 #Determine the x and y added padding (on top of boxSize) even in non-graphic mode
        self.startWait = 3 #Pause at launch

        #Graphic
        self.borderWidth = 2
        self.borderColorDefault = "gray5" #Box border
        self.borderColor = "medium sea green" #borderColorStart and borderColorCurrent
        self.borderColorEnd = "indian red"
        self.borderColorActive = "gold"
        self.fillColor = "Gray75" #Box fill
        self.textColor = "gray5"
        self.font = "times"
        self.fontSize = self.boxSize // 2
        self.fontWeight = "bold"
        self.clearAfterEach = False #Disable to see a path forming

    def update(self): #Model update after each tick
        self.x += self.boxSize + self.spacing

    def render(self, g): #Render a box at the current coordinates
        bfont = (self.font, self.fontSize, self.fontWeight)
        bbox = (self.x, self.y, self.x + self.boxSize, self.y + self.boxSize)
        g.create_rectangle(bbox, width = self.borderWidth, outline = self.borderColor, fill = self.fillColor)
        g.create_text((bbox[0] + (self.boxSize / 2), bbox[1] + (self.boxSize / 2)), text = str(self.i % 10), font = bfont, fill = self.textColor)

    def run(self): #Boucle de simulation de la dynamique
        for self.i in range(self.n):
            if self.g is not None: #Pre-rendering
                if self.i - 1 > 0 and not self.clearAfterEach:
                    self.i -= 1
                    self.borderColor = self.borderColorDefault
                    self.render(self.g)
                    self.i += 1
                elif self.clearAfterEach:
                    self.g.delete(ALL)

            self.update() 

            if self.g is not None: #Rendering
                if self.i == self.n - 1:
                    self.borderColor = self.borderColorEnd
                elif self.i > 0:
                    self.borderColor = self.borderColorActive

                self.render(self.g)
                self.g.update()
                sleep(self.tick)

                if self.i == 0:
                    sleep(self.startWait)

#Execute on run, not on import
if __name__ == '__main__':
    if doRenderTk: #Graphic rendering enabled
        root = Tk()
        root.geometry("+0+0")
        root.title("8STT105-TP4")
    else: 
        root = None
    x = Modele(root)
    x.run()
    if root is not None: 
        root.mainloop()
