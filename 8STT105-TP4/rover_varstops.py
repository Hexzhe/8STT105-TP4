import sys
import os
from tkinter import *
from time import sleep
import random
import csv

def popupmsg(msg, title):
    popup = Tk()
    popup.wm_title(title)
    label = Label(popup, text=msg, font=("Verdana", 10))
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="OK", command = popup.destroy)
    B1.pack()
    popup.mainloop()

class Model(object):
    def __init__(self, master = None):
        self.initModel()
        if master is not None: #Graphic rendering
            self.frame = Frame(master)
            self.frame.pack()
            self.bframe = Frame(self.frame)
            self.bframe.pack(side = TOP)
            self.gframe = Frame(self.frame, bd = 2, relief = RAISED)
            self.g = Canvas(self.gframe, bg = self.canevasBackgroundColor, width = self.canevasSize[0], height = self.canevasSize[1]) 
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
        sleep(int(60 * event.x // self.canevasSize[0]) + 1)

    def onClick1(self, event):
        #Slow down from 0 to 100% on left click
        self.tick *= 1.0 + event.x / self.canevasSize[0]

    def onClick3(self, event):
        #Speed up from 0 to 100% on right click
        self.tick *= 0.5 * event.x / self.canevasSize[0]

    def fillStopDurationSample(self):
        with open('ResourceFiles/arrets.csv') as csv_file: #Fill stop settings from data
            csv_reader = csv.reader(csv_file, delimiter = ",")
            c = 0
            period = 120 * (60 * 24) #The file contain data for 120 days with one data per day
            for row in csv_reader:
                c += 1
                if row[1] not in self.stopDurationSample:
                    self.stopDurationSample.append(int(row[1])) #Duration
            self.stopOdds = c / period

    def initModel(self): #Settings that are initialized once
        #Core
        self.simulationCount = 5 #Number of valid simulation to run back-to-back
        self.pauseLength = 3 #The pause between each simulation
        self.tick = 0 #Global speed (pause length after each main loop)
        self.n = 500 #Maximum number of step (while i < n)
        self.targetN = self.n // 4 #Minimum n to consider the simulation valid (in the case of a simulation that can fail by e.g. deadlocking itself)
        self.lineLength = 10 #Determine the x and y move size even in non-graphic mode
        self.lineSpacing = 0 #Determine the x and y added padding (on top of lineLength) even in non-graphic mode
        self.speedMin = 1 #Minimum speed. Speed represent the number of point drawn in a single step (i)
        self.speedMax = 3 #Maximum speed
        self.speedChangeInderval = 12 #The interval of i at which speed is going to change
        self.stopOdds = 0.0 #The odd to stop, evaluated every step (i) (Poisson)
        self.stopDurationSample = [] #Upon stop, a duration will be randomly picked (Uniform distribution)
        fillStopDurationSample() #Fill the stopDurationSample with data

        #Graphic
        self.lineWidth = 2 #The width of the line drawn
        self.lineColorDefault = "gray5" #The default (not start, not end, not highlight) color of the line drawn
        self.lineColorEnd = "indian red" #The color of the last line of the current simulation
        self.lineColorHighlight = "gold" #The color of the last line drawn
        self.clearAfterEachLine = False #Disable to make lines persistend and see a path forming
        self.canevasSize = (1920, 1080) #The actual drawing space. The canevas can be larger than the window.
        self.canevasBackgroundColor = "white" #Drawing space's background color

    def resetModel(self): #Settings that are reinitialized every self.simulationCount
        #Core
        self.i = 0 #Current step/minute
        self.x = 628 #current x
        self.y = 468 #current y
        self.speed = self.speedMin #The number of line generated in a single tick (startSpeed)
        self.points = [(self.x, self.y)] #Point history
        self.isDeadlock = False #Determine the current deadlock status. Do not enable.

        #Graphic
        self.lineColor = "medium sea green" #Current line color (set different than default to highlight the first line)
        self.orientation = 0 #Current orientation. Only relevant on line drawn where i > 0. 0=N, 1=W, 2=S, 3=E
        self.orientations = [self.orientation] #Orientation history

    def writeResult(self):
        f = open("ResourceFiles/Results/result-rover-varstops.csv", "a+")

        if os.stat("ResourceFiles/Results/result-rover-varstops.csv").st_size == 0:
            f.write("i;targetN;n;startX;startY;endX;endY\n")

        f.write(str(self.i + 1) + ";" + str(self.targetN) + ";" + str(self.n) + ";" + str(self.points[0][0]) + ";" + str(self.points[0][1]) + ";" + str(self.points[len(self.points) - 1][0]) + ";" + str(self.points[len(self.points) - 1][1]) + "\n")
        f.close()

    def checkDeadlock(self):
        if self.orientation == 0: #North
            isNorthOk = (self.x, self.y + (self.lineLength + self.lineSpacing)) not in self.points
            isWestOk = (self.x + (self.lineLength + self.lineSpacing), self.y) not in self.points
            isSouthOk = False
            isEastOk = (self.x - (self.lineLength + self.lineSpacing), self.y) not in self.points
        elif self.orientation == 1: #West
            isNorthOk = (self.x, self.y + (self.lineLength + self.lineSpacing)) not in self.points
            isWestOk = (self.x + (self.lineLength + self.lineSpacing), self.y) not in self.points
            isSouthOk = (self.x, self.y - (self.lineLength + self.lineSpacing)) not in self.points
            isEastOk = False
        elif self.orientation == 2: #South
            isNorthOk = False
            isWestOk = (self.x + (self.lineLength + self.lineSpacing), self.y) not in self.points
            isSouthOk = (self.x, self.y - (self.lineLength + self.lineSpacing)) not in self.points
            isEastOk = (self.x - (self.lineLength + self.lineSpacing), self.y) not in self.points
        elif self.orientation == 3: #East
            isNorthOk = (self.x, self.y + (self.lineLength + self.lineSpacing)) not in self.points
            isWestOk = False
            isSouthOk = (self.x, self.y - (self.lineLength + self.lineSpacing)) not in self.points
            isEastOk = (self.x - (self.lineLength + self.lineSpacing), self.y) not in self.points

        return not (isNorthOk or isWestOk or isSouthOk or isEastOk)

    def update(self): #Model update after each tick
        previousOrientation = self.orientation
        previousX = self.x
        previousY = self.y

        if self.checkDeadlock():
            self.isDeadlock = True
            return

        first = True
        while first or ((self.orientation != previousOrientation and (self.orientation % 2 == previousOrientation % 2)) or ((self.x, self.y) in self.points)):
            first = False
            self.orientation = random.randint(0, 3)

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

        self.points.append((self.x, self.y))
        self.orientations.append(self.orientation)

    def render(self, g): #Render a line at the current coordinates
        j = self.speed
        for j in range(1, j + 1):
            if self.orientations[(len(self.points) - 1) - (j - 1)] == 0: #North
                line = (self.points[(len(self.points) - 1) - (j - 1)][0], self.points[(len(self.points) - 1) - (j - 1)][1], self.points[(len(self.points) - 2) - (j - 1)][0], self.points[(len(self.points) - 2) - (j - 1)][1] + self.lineSpacing)
            elif self.orientations[(len(self.points) - 1) - (j - 1)] == 1: #West
                line = (self.points[(len(self.points) - 1) - (j - 1)][0], self.points[(len(self.points) - 1) - (j - 1)][1], self.points[(len(self.points) - 2) - (j - 1)][0] + self.lineSpacing, self.points[(len(self.points) - 2) - (j - 1)][1])
            elif self.orientations[(len(self.points) - 1) - (j - 1)] == 2: #South
                line = (self.points[(len(self.points) - 1) - (j - 1)][0], self.points[(len(self.points) - 1) - (j - 1)][1], self.points[(len(self.points) - 2) - (j - 1)][0], self.points[(len(self.points) - 2) - (j - 1)][1] - self.lineSpacing)
            elif self.orientations[(len(self.points) - 1) - (j - 1)] == 3: #East
                line = (self.points[(len(self.points) - 1) - (j - 1)][0], self.points[(len(self.points) - 1) - (j - 1)][1], self.points[(len(self.points) - 2) - (j - 1)][0] - self.lineSpacing, self.points[(len(self.points) - 2) - (j - 1)][1])

            g.create_line(line, width = self.lineWidth, fill = self.lineColor)

    def run(self): #Simulation loop
        for j in range(self.simulationCount):
            finalCount = 0
            while finalCount < self.targetN: #Quality insurance loop
                self.g.delete(ALL)
                self.resetModel()
                for self.i in range(self.n):

                    if random.uniform(0, 1) < self.stopOdds: #Stop
                        self.i += random.choice(self.stopDurationSample)
                        continue
                    
                    if self.g is not None: #Pre-rendering
                        if self.i - 1 > 0 and not self.clearAfterEachLine:
                            self.lineColor = self.lineColorDefault
                            self.render(self.g)
                            self.g.update()
                        elif self.clearAfterEachLine:
                            self.g.delete(ALL)

                    if (self.i + 1) % self.speedChangeInderval == 0: #Change speed
                        if bool(random.getrandbits(1)): #Faster
                            if self.speedMin < self.speed == self.speedMax: #Can't go faster, go slower
                                self.speed -= 1
                            elif self.speedMin <= self.speed < self.speedMax: #Ok, go faster
                                self.speed += 1
                        else: #Slower
                            if self.speedMin == self.speed < self.speedMax: #Can't go slower, go faster
                                self.speed += 1
                            elif self.speedMin < self.speed <= self.speedMax: #Ok, go slower
                                self.speed -= 1

                    j = self.speed
                    for j in range(1, j + 1):
                        self.update()
                
                    if self.g is not None: #Rendering
                        if self.isDeadlock:
                            self.lineColor = self.lineColorEnd
                            self.render(self.g)
                            self.g.update()
                            break

                        if self.i == self.n - 1:
                            self.lineColor = self.lineColorEnd
                        elif self.i > 0:
                            self.lineColor = self.lineColorHighlight
                
                        self.render(self.g)
                        self.g.update()
                        sleep(self.tick)
                finalCount = self.i
            self.writeResult()
            sleep(self.pauseLength)
        popupmsg("Simulation run: " + str(self.simulationCount) + "\nn: " + str(self.n) + "\nMinimum target: " + str(self.targetN) + "\n\n Check ResourceFiles/Results/result-rover-varstops.csv for results.\nYou can now exit.", "Done!")
