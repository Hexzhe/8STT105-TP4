import sys
from tkinter import *
from time import sleep

doRenderTk = True #Choix de faire un rendering Tk ou pas

class Modele(object):
    def __init__(self, master = None):
        self.init_modele() #init du modele lui-meme
        #Canvas pour le rendering graphique 
        self.canvas_size = (600, 600) #Taille du canvas pour le rendering
        if master is not None: #Fenetre de rendering si necessaire
            self.refreshTk = 1.0
            self.waitTk = 3
            self.frame = Frame(master)
            self.frame.pack()
            self.bframe = Frame(self.frame)
            self.bframe.pack(side = TOP)
            self.gframe = Frame(self.frame, bd = 2, relief = RAISED)
            self.g = Canvas(self.gframe, bg = 'white', width = self.canvas_size[0], height = self.canvas_size[1]) 
            self.g.pack()
            self.g.bind('<ButtonPress-1>', self.onClick1) #Click 1 (left)
            self.g.bind('<ButtonPress-2>', self.onClick2) #Click 2 (centre)
            self.g.bind('<ButtonPress-3>', self.onClick3) #Click 3 (right)
            self.gframe.pack(side = TOP)
            self.g.delete(ALL) #Clean du canvas
        else: 
            self.g = None

    def onClick2(self, event):
        #On sleep pendant 1 a 60 secondes proportionnel a x, d'un click centre
        sleep(int(60 * event.x // self.canvas_size[0]) + 1)

    def onClick1(self, event):
        #On ralentie l'affichage d'un % proportionnel a x (i.e. 0 a 100%), d'un click left
        self.refreshTk *= 1.0 + event.x / self.canvas_size[0]

    def onClick3(self, event):
        #On accelere l'affichage d'un % proportionnel a x (i.e. 0 a 100%), d'un click right
        self.refreshTk *= 0.5 * event.x / self.canvas_size[0]

    def init_modele(self): #Init du modele
        self.nbPas = 5 #Nombre de pas de simulation
        self.etat = 0 #Variable d'etat

    def update(self): #Update du modele
        self.etat = self.etat + 1 #Mise a jour de l'etat du modele
        #TODO: Ajouter la logique pour un step ici

    def render(self, g): #Rendering du modele dans le canvas Tk g
        bfont = ('times', 14, 'bold')
        bbox = (100, 100, 100, 100)
        g.create_rectangle(bbox, width = 1, outline = "black", fill = "yellow")
        g.create_text((bbox[0] + 25, bbox[1] + 20), text = str(self.etat), font = bfont, fill = 'black')

    def run(self): #Boucle de simulation de la dynamique
        for i in range(self.nbPas):
            # On opere le systeme pour un pas
            self.update() 
            #Rendering tkinter
            if self.g is not None: 
                self.g.delete(ALL) #Commenter ceci pour laisser chaque step affiché
                self.render(self.g)
                self.g.update()
                sleep(self.refreshTk)
                if i==0: 
                    sleep(self.waitTk) #On attends pour laisser voir l'etat initial

#A executer seulement si ce n'est pas un import, mais bien un run du code
if __name__ == '__main__':
    if doRenderTk: #Avec rendering Tk (animation)
        root = Tk()
        root.geometry("+0+0")
        root.title("simulation")
    else: 
        root = None
    x = Modele(root) #Creation du modele
    x.run() #Run du modele (simulation) avec ou sans animation
    if root is not None: 
        root.mainloop()
