import pygame, math, time

print(pygame)

pygame.init()
WIDTH, HEIGHT = (800, 800)
screen = pygame.display.set_mode((800, 800))
running = True

x = 0
y = 0
xv = 0
yv = 0

# Physics Constants
G = 9.8
F = 0.7
V = 10
JUMP = 7

# Render Constants
BLOCKSIZE = 32

grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

last_time = time.perf_counter()

while running:

    t = time.perf_counter()
    dt = t - last_time
    last_time = t

    try_to_jump = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                try_to_jump = True

    keys = pygame.key.get_pressed()

    # Velocity
    yv += G * dt
    y += yv * dt
    if keys[pygame.K_a]: xv -= V * dt
    if keys[pygame.K_d]: xv += V * dt
    x += xv * dt
    xv *= F ** dt

    # Collisions
    left_x = math.ceil(x - 1)
    right_x = math.floor(x + 1)
    left_x_clearance = math.ceil(x - 0.95)
    right_x_clearance = math.floor(x + 0.95)
    top_y = math.floor(y + 0.9)
    mid_y = math.ceil(y - 0.1)
    bottom_y = math.ceil(y)

    if (grid[mid_y][left_x] != 0 or grid[top_y][left_x] != 0) and xv < 0:
        x = left_x + 1
        xv = 0

    if (grid[mid_y][right_x] != 0 or grid[top_y][right_x] != 0) and xv > 0:
        x = right_x - 1
        xv = 0

    # Floor Collisions
    if (grid[bottom_y][left_x_clearance] != 0 or grid[bottom_y][right_x_clearance] != 0) and yv > 0:
        if try_to_jump: yv = -JUMP
        else: yv = 0
        y = bottom_y - 1

    # Rendering
    screen.fill((255, 255, 255))

    # Draw grid
    for ty, row in enumerate(grid):
        for tx, tile in enumerate(row):
            
            if tile == 0: colour = (135, 206, 235)
            elif tile == 1: colour = (80, 80, 80)
            else: colour = (255, 255, 255)

            effective_x = (tx - x) * BLOCKSIZE + WIDTH / 2 - BLOCKSIZE / 2
            effective_y = (ty - y) * BLOCKSIZE + HEIGHT / 2 - BLOCKSIZE / 2

            pygame.draw.rect(screen, colour, pygame.Rect(effective_x, effective_y, BLOCKSIZE, BLOCKSIZE))

    # Draw player
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(WIDTH // 2 - BLOCKSIZE // 2, HEIGHT // 2 - BLOCKSIZE // 2, BLOCKSIZE, BLOCKSIZE))
    pygame.display.update()
pygame.quit()