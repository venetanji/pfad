class Ball:
    def __init__(self, **kwargs):
        self.position = kwargs.get("position", PVector.random2D().mult(width))
        self.velocity = kwargs.get("velocity", PVector.random2D())
        self.color = color(random(360), 70, 70, 70)
        self.size = 20 + random(80)
        
    def update(self, dt):
        step = PVector.mult(self.velocity,dt)
        self.position.add(step)
        self.position.x = self.position.x % width
        self.position.y = self.position.y % height
        fill(self.color)
        stroke(self.color)
        circle(self.position.x, self.position.y, self.size*step.mag())

def setup():
    
    size(768,512)
    colorMode(HSB, 360, 100, 100)

    global balls, n_balls, speed, iteration
    iteration = 1.0
    speed = 2
    balls = []
    n_balls = 10
    for n in range(n_balls):
        ball = Ball()
        balls.append(ball)
    
def draw():
    global iteration
    background(255, 0, 100)
    iteration += 0.005
    current_speed = sin(iteration)*speed
    [ball.update(current_speed) for ball in balls]
    
    if mousePressed:
        balls.append(Ball(position=PVector(mouseX, mouseY)))

    
    
