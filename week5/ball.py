import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# 定义砖块
def draw_brick(x, y, z):
    glBegin(GL_QUADS)
    glVertex3f(x, y, z)
    glVertex3f(x + 1, y, z)
    glVertex3f(x + 1, y + 0.5, z)
    glVertex3f(x, y + 0.5, z)
    glEnd()

# 球的绘制
def draw_ball(x, y, z):
    glTranslatef(x, y, z)
    quadric = gluNewQuadric()
    gluSphere(quadric, 0.2, 32, 32)
    glTranslatef(-x, -y, -z)

# 挡板的绘制
def draw_paddle(x, y, z):
    glBegin(GL_QUADS)
    glVertex3f(x - 1, y, z)
    glVertex3f(x + 1, y, z)
    glVertex3f(x + 1, y + 0.2, z)
    glVertex3f(x - 1, y + 0.2, z)
    glEnd()

# 初始化游戏窗口和OpenGL环境
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -20)

# 游戏变量
paddle_x = 0
ball_pos = np.array([0.0, 0.0, 0.0])  # 使用浮点数
ball_vel = np.array([0.1, 0.1, 0.0])  # 使用浮点数

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle_x -= 1
            elif event.key == pygame.K_RIGHT:
                paddle_x += 1

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    # 绘制砖块
    for x in range(-5, 6, 2):
        for y in range(-2, 3, 1):
            draw_brick(x, y, 0)

    # 更新和绘制球
    ball_pos += ball_vel
    if ball_pos[0] <= -10 or ball_pos[0] >= 10:
        ball_vel[0] = -ball_vel[0]
    if ball_pos[1] <= -10 or ball_pos[1] >= 10:
        ball_vel[1] = -ball_vel[1]

    draw_ball(*ball_pos)

    # 绘制挡板
    draw_paddle(paddle_x, -9, 0)

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
quit()
