# a rendering of the sierpinsky fractal using tkinter canvas
import random
import tkinter as tk
import numpy as np
width = 800
height = 600
root = tk.Tk()
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()
canvas.create_rectangle(0, 0, width, height, fill='white')


def draw_point(pos):
    x, y = pos  + np.array([(random.random() - 0.5)*500 for _ in range(2)])
    canvas.create_oval(x-1, y-1, x + 1, y + 1, fill='black')
    canvas.after(10, draw_point, pos)

draw_point(np.array([width/2, height/2]))

root.mainloop()