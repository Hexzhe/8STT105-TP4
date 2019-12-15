from tkinter import *
import walk_random as wr
import walk_nonreversing as wnr
import walk_self_avoiding as wsa

doRenderTk = True #Enable graphic rendering
windowSize = "1280x960+0+0"

if doRenderTk: #Graphic rendering enabled
    root = Tk()
    root.geometry(windowSize)
    root.title("8STT105-TP4")
else: 
    root = None

#Uncomment the model you want to run
#model = wr.Model(root)
#model = wnr.Model(root)
model = wsa.Model(root)

model.run()
if root is not None: 
    root.mainloop()