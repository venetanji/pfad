import random
import time
vert = "|"
hor = "\u23b4"
size = 30
h_prob = 0.20

grid = []

last_square_empty = False
for w in range(size):
    grid.append([])
    for h in range(size):
        draw_vertical = random.randint(0, size-2) >= abs(w-h)
        draw_horizontal = (random.randint(0, size) > h_prob*size) and last_square_empty
        grid[w].append((draw_vertical, draw_horizontal))
        if draw_vertical or draw_horizontal:
            last_square_empty = False
        else:
            last_square_empty = True

for h in range(size):
    for w in range(size):
        print(vert if grid[w][h][0] else " ", end="")
        print(hor if grid[w][h][1] else " ", end="")
    print()
