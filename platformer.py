import pygame

pygame.init()
BS = 32
W = H = 800
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

# Physics constants
G = 2000
SPEED = 400
JUMP = 800
FRICTION = 0.8

grid = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,1],
    [0,0,0,0,0,0,0,0,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,0,0,0,1,1,1],
    [1,1,1,1,0,0,0,1,1,1],
    [1,1,1,1,1,1,1,1,1,1]
]

player = pygame.Rect(64, 0, BS, BS)
vx = vy = 0.0
on_ground = False
running = True

def solid_tiles(rect):
    x0 = rect.left // BS
    x1 = rect.right // BS
    y0 = rect.top // BS
    y1 = rect.bottom // BS

    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if grid[y][x]:
                yield pygame.Rect(x*BS, y*BS, BS, BS)

while running:
    dt = clock.tick(60) / 1000

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Input
    if keys[pygame.K_a]: vx = -SPEED
    elif keys[pygame.K_d]: vx = SPEED
    else: vx *= FRICTION
    if keys[pygame.K_SPACE] and on_ground: vy = -JUMP

    # Gravity
    vy += G * dt

    # Horizontal movement
    player.x += vx * dt
    for tile in solid_tiles(player):
        if player.colliderect(tile):
            if vx > 0:
                player.right = tile.left
            elif vx < 0:
                player.left = tile.right
            vx = 0

    # Vertical movement
    player.y += vy * dt
    on_ground = False
    for tile in solid_tiles(player):
        if player.colliderect(tile):
            if vy > 0:
                player.bottom = tile.top
                on_ground = True
            elif vy < 0:
                player.top = tile.bottom
            vy = 0

    # Render
    screen.fill((135,206,235))
    for y, row in enumerate(grid):
        for x, t in enumerate(row):
            if t:
                dx = x * BS - player.x + W // 2 - BS // 2
                dy = y * BS - player.y + H // 2 - BS // 2
                pygame.draw.rect(screen, (80,80,80),(dx, dy, BS, BS))

    pygame.draw.rect(screen, (255,0,0), pygame.Rect(W // 2 - BS // 2, H // 2 - BS // 2, BS, BS))
    pygame.display.flip()

pygame.quit()