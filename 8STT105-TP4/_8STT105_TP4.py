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
print("  1 - Walk  - Random") #1.2.1
print("  2 - Walk  - Nonreversing") #1.2.2
print("  3 - Walk  - Self-Avoiding") #1.2.3
print("  4 - Rover - Variable speed") #2.1
print("  5 - Rover - Fixed length stops") #2.2
print("  6 - Rover - Variable length stops") #2.3

valid = False
while not valid:
    menuChoice = str(input(">")).upper()
    valid = (menuChoice == "1" or menuChoice == "2" or menuChoice == "3" or menuChoice == "4" or menuChoice == "5" or menuChoice == "6")

if doRenderTk: #Graphic rendering enabled
    root = Tk()
    root.geometry(windowSize)
    root.title("8STT105-TP4")
else: 
    root = None

#Uncomment the model you want to run
if menuChoice == "1":
    model = wr.Model(root)
elif menuChoice == "2":
    model = wnr.Model(root)
elif menuChoice == "3":
    model = wsa.Model(root)
elif menuChoice == "4":
    model = rvsp.Model(root)
elif menuChoice == "5":
    model = rfst.Model(root)
elif menuChoice == "6":
    model = rvst.Model(root)

model.run()
if root is not None: 
    root.mainloop()