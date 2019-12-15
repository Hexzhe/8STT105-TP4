from tkinter import *
import walk_random as wr
import walk_nonreversing as wnr
import walk_self_avoiding as wsa

doRenderTk = True #Enable graphic rendering
windowSize = "1280x960+0+0"

print("8STT105-TP4 - Jason Gilbert &  Dominique Boivin")
print("Menu:")
print("  C - Random")
print("  S - Nonreversing")
print("  U - Self-Avoiding")

valid = False
while not valid:
    menuChoice = str(input(">")).upper()
    valid = (menuChoice == "C" or menuChoice == "S" or menuChoice == "U")

if doRenderTk: #Graphic rendering enabled
    root = Tk()
    root.geometry(windowSize)
    root.title("8STT105-TP4")
else: 
    root = None

#Uncomment the model you want to run
if menuChoice == "C":
    model = wr.Model(root)
elif menuChoice == "S":
    model = wnr.Model(root)
elif menuChoice == "U":
    model = wsa.Model(root)

model.run()
if root is not None: 
    root.mainloop()