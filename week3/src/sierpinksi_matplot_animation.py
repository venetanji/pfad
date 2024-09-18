import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# create a figure
fig = plt.figure(figsize=(7, 7))

# create an axes object that spans the whole figure
ax = fig.add_axes([0, 0, 1, 1], frameon=False)

# give some margin to the plot and remove the visibility of the axes
ax.set_xlim(-0.2, 1.2), ax.set_xticks([])
ax.set_ylim(-0.2, 1.2), ax.set_yticks([])

# some parameters you can change!
max_loop = 100
vertices = [[0.5, np.sqrt(3)/2], [0, 0], [1, 0]]
max_runs = 10
iters = 500 # number of iterations per run

# draw equilateral triangle
triangle = plt.Polygon(vertices, fill=None)

# add it to the axes
ax.add_patch(triangle)

# declare variable to store the points
runs = []

def update(frame):

    global max_loop
    global runs

    frame = frame % max_loop

    pos_x = [0]
    pos_y = [0]
    
    for _ in range(iters):
        # get a random vertex
        vertex = vertices[np.random.randint(0, 3)]

        # from the last position move halfway to the vertex
        pos_x.append(0.5*(pos_x[-1]+vertex[0]))
        pos_y.append(0.5*(pos_y[-1]+vertex[1]))

    # create a color based on the frame value
    triangle_color = plt.cm.viridis(1 - frame/max_loop)

    # set the color of the triangle
    triangle.set_edgecolor(triangle_color)

    # create a color based on the frame value
    run_color = plt.cm.viridis(frame/max_loop)

    # plot the run with a color based on the frame value
    run = ax.scatter(pos_x, pos_y, color=run_color,s=2)

    # add the run to the list of runs
    runs.append(run)
    
    # remove the first run if we have more than max_runs
    if len(runs) > max_runs:
        # remove oldest one from the plot
        runs[0].remove()
        # remove oldest one from the list
        runs.pop(0)

# create the animation
animation = FuncAnimation(fig, update, interval=10, cache_frame_data=False)

# show the plot
plt.show()