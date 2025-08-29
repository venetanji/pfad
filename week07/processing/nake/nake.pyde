def setup():
    size(512,512)
    global grid, gsize, side, last_square_empty, border, h_prob
    h_prob = 0.30
    border = 3
    last_square_empty = False
    side = 512
    grid = 64
    gsize = side/grid
    noLoop()
    
def draw():
    background(255)
    stroke(99)
    
    for w in range(grid):
        
        # skip row if we are in the border
        if w < border or w > grid - border - 1: continue    
    
        for h in range(grid):
            
            # skip column if we are in the border
            if h < border or h > grid - border - 1: continue
            
            # set conditions for line to be drawn
            draw_vertical = random(grid) > abs(w-h)
            draw_horizontal = (random(1) < h_prob) and last_square_empty

            # store previous square state (the one above current) for next iteration 
            if draw_vertical or draw_horizontal:
                last_square_empty = False
            else:
                last_square_empty = True
            
            # push matrix will reset the translation at every iteration
            with pushMatrix():
                
                # translate to top left point of each cell
                translate(w * gsize, h * gsize)
                
                # draw the lines with coordinates relative to top left point in the cell
                if draw_vertical: line(0,0,0,gsize) 
                if draw_horizontal: line(0,0,gsize,0) 

            
