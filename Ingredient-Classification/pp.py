#!/usr/bin/python
import sys
import sys
import os
import tkinter as tk

root= tk.Tk()
w = tk.Label(root, text="TELUGU CHARACTER RECOGNITION USING DEEP LEARNING")
w.config(font=("Courier", 30))
w.pack()
w1 = tk.Label(root, text="Please enter the image file name")
w1.config(font=("Times", 10))
w1.pack()
x="python predict.py --image "
canvas1 = tk.Canvas(root, width = 400, height = 300)
canvas1.pack()

entry1 = tk.Entry (root) 
canvas1.create_window(200, 140, window=entry1)

    
def getSquareRoot ():  
    x1 = entry1.get()
    os.system(x+x1)
    print(x+x1)
    
    
button1 = tk.Button(text='run', command=getSquareRoot)
canvas1.create_window(200, 180, window=button1)

root.mainloop()
