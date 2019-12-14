import sys
from tkinter import *
from time import sleep

doRenderTk = True #Choix de faire un rendering Tk ou pas

class Modele(object):
    def __init__(self, master = None):
        self.init_modele() #init du modele lui-meme
        #Canvas pour le rendering graphique 
        if master is not None: #Fenetre de rendering si necessaire
            self.frame = Frame(master)
            self.frame.pack()
            self.bframe = Frame(self.frame)
            self.bframe.pack(side = TOP)
            self.gframe = Frame(self.frame, bd = 2, relief = RAISED)
            self.g = Canvas(self.gframe, bg = self.backgroundColor, width = self.windowSize[0], height = self.windowSize[1]) 
            self.g.pack()
            self.g.bind("<ButtonPress-1>", self.onClick1) #Click 1 (left)
            self.g.bind("<ButtonPress-2>", self.onClick2) #Click 2 (centre)
            self.g.bind("<ButtonPress-3>", self.onClick3) #Click 3 (right)
            self.gframe.pack(side = TOP)
            self.g.delete(ALL) #Clean du canvas
        else: 
            self.g = None

    def onClick2(self, event):
        #On sleep pendant 1 a 60 secondes proportionnel a x, d'un click centre
        sleep(int(60 * event.x // self.windowSize[0]) + 1)

    def onClick1(self, event):
        #On ralenti l'affichage d'un % proportionnel a x (i.e. 0 a 100%), d'un click left
        self.tick *= 1.0 + event.x / self.windowSize[0]

    def onClick3(self, event):
        #On accelere l'affichage d'un % proportionnel a x (i.e. 0 a 100%), d'un click right
        self.tick *= 0.5 * event.x / self.windowSize[0]

    def init_modele(self): #Init du modele
        self.n = 10 #Nombre de pas de simulation
        self.i = 0 #Variable d'etat
        self.borderColor = "medium sea green" #borderColorStart
        self.borderColorEnd = "indian red"
        self.borderColorDefault = "gray5"
        self.borderColorActive = "gold"
        self.fillColor = "Gray75"
        self.textColor = "gray5"
        self.font = "times"
        self.fontSize = 14
        self.fontWeight = "bold"
        self.x = 628 #Start X
        self.y = 468 #Start Y
        self.boxSize = 25
        self.spacing = 2
        self.windowSize = (1280, 960)
        self.startWait = 3
        self.tick = 1.0
        self.backgroundColor = "white"
        self.clearAfterEach = False

    def update(self): #Update du 
        self.x += self.boxSize + self.spacing #TODO: Ajouter la logique pour un step ici

    def render(self, g): #Rendering du modele dans le canvas Tk g
        bfont = (self.font, self.fontSize, self.fontWeight)
        bbox = (self.x, self.y, self.x + self.boxSize, self.y + self.boxSize)
        g.create_rectangle(bbox, width = 2, outline = self.borderColor, fill = self.fillColor)
        g.create_text((bbox[0] + 12.5, bbox[1] + 12.5), text = str(self.i % 10), font = bfont, fill = self.textColor)

    def run(self): #Boucle de simulation de la dynamique
        for self.i in range(self.n):
            # On opere le systeme pour un pas
            self.update() 
            #Rendering tkinter
            if self.g is not None: 
                if self.i == self.n - 1:
                    self.borderColor = self.borderColorEnd
                elif self.i > 0:
                    self.borderColor = self.borderColorDefault

                if self.clearAfterEach:
                    self.g.delete(ALL)

                self.render(self.g)
                self.g.update()
                sleep(self.tick)

                if self.i == 0: #Petite pause au premier pas pour voir l'état initial
                    sleep(self.startWait)

#A executer seulement si ce n'est pas un import, mais bien un run du code
if __name__ == '__main__':
    if doRenderTk: #Avec rendering Tk (animation)
        root = Tk()
        root.geometry("+0+0")
        root.title("8STT105-TP4")
    else: 
        root = None
    x = Modele(root) #Creation du modele
    x.run() #Run du modele (simulation) avec ou sans animation
    if root is not None: 
        root.mainloop()
