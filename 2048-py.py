# prompt: Make the 2048 sliding tile number puzzle game using pygame
# conversation link: https://chat.openai.com/share/83818bfd-dec7-41a6-8edc-c65b1bd7a4c9
import pygame
import sys
import random

# Constants
SCREEN_SIZE = 400
TILE_SIZE = 100
TILE_MARGIN = 10

# Colors
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# Initialize the pygame
pygame.init()

def draw_tile(screen, value, x, y):
    color = TILE_COLORS[value]
    rect = (x * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN, y * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, color, rect)

    if value != 0:
        font = pygame.font.Font(None, 40)
        text = font.render(str(value), True, (0, 0, 0))
        text_rect = text.get_rect(center=rect[0:2] + pygame.Vector2(TILE_SIZE // 2, TILE_SIZE // 2))
        screen.blit(text, text_rect)

def move(matrix, direction):
    # 0: up, 1: right, 2: down, 3: left
    rotated_matrix = [row[:] for row in matrix]
    if direction == 0:
        rotated_matrix = list(zip(*reversed(rotated_matrix)))
    elif direction == 1:
        rotated_matrix = [list(reversed(row)) for row in rotated_matrix]
    elif direction == 2:
        rotated_matrix = list(reversed(list(zip(*rotated_matrix))))

    for row in range(4):
        non_zero = [x for x in rotated_matrix[row] if x != 0]
        for i in range(1, len(non_zero)):
            if non_zero[i - 1] == non_zero[i]:
                non_zero[i - 1] *= 2
                non_zero[i] = 0

        non_zero = [x for x in non_zero if x != 0]
        rotated_matrix[row] = non_zero + [0] * (4 - len(non_zero))

    if direction == 0:
        rotated_matrix = list(reversed(list(zip(*rotated_matrix))))
    elif direction == 1:
        rotated_matrix = [list(reversed(row)) for row in rotated_matrix]
    elif direction == 2:
        rotated_matrix = list(zip(*reversed(rotated_matrix)))

    return [list(row) for row in rotated_matrix]

def add_tile(matrix):
    empty_cells = [(x, y) for y in range(4) for x in range(4) if matrix[y][x] == 0]
    if empty_cells:
        x, y = random.choice(empty_cells)
        matrix[y][x] = 2 if random.random() < 0.9 else 4

# Game matrix
matrix = [[0] * 4 for _ in range(4)]
add_tile(matrix)
add_tile(matrix)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("2048")

while True:
    screen.fill(BACKGROUND_COLOR)

    for y in range(4):
        for x in range(4):
            draw_tile(screen, matrix[y][x], x, y)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            old_matrix = [row[:] for row in matrix]
            if event.key == pygame.K_UP:
                matrix = move(matrix, 0)
            elif event.key == pygame.K_RIGHT:
                matrix = move(matrix, 1)
            elif event.key == pygame.K_DOWN:
                matrix = move(matrix, 2)
            elif event.key == pygame.K_LEFT:
                matrix = move(matrix, 3)

            if matrix != old_matrix:
                add_tile(matrix)
