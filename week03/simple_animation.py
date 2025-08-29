import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.transforms as transforms


fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(-1, 1), ax.set_xticks([])
ax.set_ylim(-1, 1), ax.set_yticks([])

# add a circle to the plot
circle1 = plt.Circle((0, 0), 0.1, color='r')
ax.add_patch(circle1)
square = [[-0.5, -0.5], [-0.5, 0.5], [0.5, 0.5], [0.5, -0.5]]

trans = (transforms.Affine2D().rotate_deg(45) + ax.transData)
square = plt.Polygon(square, fill=None, transform=trans)
ax.add_patch(square)

max_loop = 100
full_circle_radius = 1

reverse = False

def update(frame):
    global reverse
    if frame % max_loop == 0:
        reverse = not reverse
    if reverse:
        frame = frame % max_loop
    else:
        frame = max_loop - frame % max_loop

    # normalized frame value (0 to 1)
    # useful to scale things linearly
    norm_frame = frame/max_loop
    
    # set the radius of the circle based on the frame value
    circle1.set_radius(full_circle_radius*norm_frame)

    # set the color of the circle based on the frame value
    circle1.set_color(plt.cm.viridis(norm_frame))

    # create the transformation matrix adding a rotation
    transform = transforms.Affine2D().rotate_deg(90*norm_frame) + ax.transData

    # set the transformation matrix to the square
    square.set_transform(transform)
    
animation = FuncAnimation(fig, update, interval=10)
plt.show()