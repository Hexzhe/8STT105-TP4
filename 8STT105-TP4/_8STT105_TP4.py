from tkinter import *
import walk_random as wr
import walk_nonreversing as wnr
import walk_selfavoiding as wsa
import rover_varspeed as rvsp
import rover_fixedstops as rfst
import rover_varstops as rvst

doRenderTk = True #Enable graphic rendering
windowSize = "1280x960+0+0"

print("8STT105-TP4 - Jason Gilbert &  Dominique Boivin")
print("Menu:")
print("  C - Walk  - Random") #1.2.1
print("  S - Walk  - Nonreversing") #1.2.2
print("  U - Walk  - Self-Avoiding") #1.2.3
print("  V - Rover - Variable speed") #2.1
print("  F - Rover - Fixed length stops") #2.2
print("  T - Rover - Variable length stops") #2.3

valid = False
while not valid:
    menuChoice = str(input(">")).upper()
    valid = (menuChoice == "C" or menuChoice == "S" or menuChoice == "U" or menuChoice == "V" or menuChoice == "F" or menuChoice == "T")

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
    model = rvsp.Model(root)
elif menuChoice == "F":
    model = rfst.Model(root)
elif menuChoice == "T":
    model = rvst.Model(root)

model.run()
if root is not None: 
    root.mainloop()