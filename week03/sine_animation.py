import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(-1, 1), ax.set_xticks([])
ax.set_ylim(-1, 1), ax.set_yticks([])

# add a circle to the plot
circle1 = plt.Circle((0, 0), 0.1, color='r')
ax.add_patch(circle1)

# some variables you can change
max_loop = 100
full_circle_radius = 1
number_of_lines = 200
scale = 30

reverse = False
def update(frame):
    global reverse
    # reverse the animation when reaching the end
    if frame % max_loop == 0:
        reverse = not reverse
        
    # if animation is in reverse
    if reverse:
        # loop the frame value using the modulo operator %
        frame = frame % max_loop
    else:
        # invert the frame value
        frame = max_loop - frame % max_loop
    
    # normalized frame value (0 to 1)
    norm_frame = frame/max_loop
    
    # animate the circle radius and color
    circle1.set_radius(full_circle_radius*norm_frame)
    circle1.set_color(plt.cm.viridis(norm_frame))

    # create the X values
    # the third argument is the number of steps
    # higher values will make the curves smoother
    x = np.linspace(-1, 1, int(norm_frame*max_loop))
    
    # SET THE FUNCTION HERE
    y = np.cos(x*frame/scale)
    z = np.sin(x*frame/scale)
    #z = np.exp(x*np.pi*1j)
    #z = np.sin(x * np.exp(frame * 1j))
    
    # flip the value upside down when going in reverse
    if reverse:
        y = -y
        z = -z

    # plot two lines with oppsite colors
    ax.plot(x,y, color=plt.cm.viridis(norm_frame),alpha=0.5)
    ax.plot(x,z, color=plt.cm.viridis(-norm_frame), alpha=0.5)
    # try inverting the axis
    # ax.plot(z,x, color=plt.cm.viridis(-frame/100))

    # while the number of lines is greater than the number of lines we want
    while len(ax.lines) > number_of_lines*norm_frame:
        # remove the oldest line
        ax.lines[0].remove()

animation = FuncAnimation(fig, update, interval=10)
plt.show()