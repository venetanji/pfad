import pygame
import sys

# 初始化pygame
pygame.init()

# 设置屏幕大小
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 颜色定义
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# 砖块参数
brick_width = 60
brick_height = 20
brick_color = blue
num_bricks_x = screen_width // (brick_width + 10)
num_bricks_y = 5

# 球参数
ball_size = 10
ball_color = white
ball_rect = pygame.Rect(screen_width // 2, screen_height // 2, ball_size, ball_size)
ball_speed_x = 4
ball_speed_y = -4

# 挡板参数
paddle_width = 100
paddle_height = 20
paddle_color = red
paddle_rect = pygame.Rect(screen_width // 2 - paddle_width // 2, screen_height - 40, paddle_width, paddle_height)
paddle_speed = 0
paddle_move_speed = 6

# 创建砖块
bricks = []
for y in range(num_bricks_y):
    for x in range(num_bricks_x):
        brick = pygame.Rect(x * (brick_width + 10) + 5, y * (brick_height + 5) + 50, brick_width, brick_height)
        bricks.append(brick)

# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle_speed = -paddle_move_speed
            elif event.key == pygame.K_RIGHT:
                paddle_speed = paddle_move_speed
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                paddle_speed = 0

    # 更新挡板位置
    paddle_rect.x += paddle_speed
    paddle_rect.x = max(paddle_rect.x, 0)
    paddle_rect.x = min(paddle_rect.x, screen_width - paddle_width)

    # 更新球位置
    ball_rect.x += ball_speed_x
    ball_rect.y += ball_speed_y

    # 球碰撞边界处理
    if ball_rect.left <= 0 or ball_rect.right >= screen_width:
        ball_speed_x = -ball_speed_x
    if ball_rect.top <= 0:
        ball_speed_y = -ball_speed_y
    if ball_rect.bottom >= screen_height:
        running = False  # 游戏结束

    # 球碰撞挡板处理
    if ball_rect.colliderect(paddle_rect):
        ball_speed_y = -ball_speed_y

    # 球碰撞砖块处理
    for brick in bricks[:]:
        if ball_rect.colliderect(brick):
            ball_speed_y = -ball_speed_y
            bricks.remove(brick)

    # 渲染
    screen.fill(black)
    for brick in bricks:
        pygame.draw.rect(screen, brick_color, brick)
    pygame.draw.ellipse(screen, ball_color, ball_rect)
    pygame.draw.rect(screen, paddle_color, paddle_rect)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
