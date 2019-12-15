from tkinter import *
import walk_random as wr
import walk_nonreversing as wnr
import walk_selfavoiding as wsa
import rover_varspeed as rvs

doRenderTk = True #Enable graphic rendering
windowSize = "1280x960+0+0"

print("8STT105-TP4 - Jason Gilbert &  Dominique Boivin")
print("Menu:")
print("  C - Walk  - Random")
print("  S - Walk  - Nonreversing")
print("  U - Walk  - Self-Avoiding")
print("  V - Rover - Variable speed")

valid = False
while not valid:
    menuChoice = str(input(">")).upper()
    valid = (menuChoice == "C" or menuChoice == "S" or menuChoice == "U" or menuChoice == "V")

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
elif menuChoice == "V":
    model = rvs.Model(root)

model.run()
if root is not None: 
    root.mainloop()