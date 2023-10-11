import sys
import pygame
from pygame.locals import *

# Initialize pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

# Set colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Load sound effects
hit_sound = pygame.mixer.Sound('hit.wav')
lose_sound = pygame.mixer.Sound('lose.wav')

# Initialize font
font = pygame.font.Font(None, 36)
score = 0

# Game classes
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((75, 25))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 5

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        pygame.draw.circle(self.image, WHITE, (7, 7), 7)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = [3, 3]

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0:
            self.speed[1] = -self.speed[1]

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 25))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Create game objects
paddle = Paddle()
ball = Ball()
bricks_group = pygame.sprite.Group()

# Create bricks
for i in range(7):
    for j in range(5):
        brick = Brick(i * 55, j * 30)
        bricks_group.add(brick)

all_sprites = pygame.sprite.Group(paddle, ball, bricks_group)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update game objects
    all_sprites.update()

    # Check for collisions
    if pygame.sprite.spritecollide(paddle, pygame.sprite.Group(ball), False):
        rel = ball.rect.centerx - paddle.rect.centerx
        ball.speed[0] = rel * 0.1  # Adjust this factor to control the angle of bounce
        ball.speed[1] = -ball.speed[1]

    collided_bricks = pygame.sprite.spritecollide(ball, bricks_group, True)
    if collided_bricks:
        ball.speed[1] = -ball.speed[1]
        score += len(collided_bricks)
        hit_sound.play()

    if not bricks_group:
        ball.speed[0] += 1
        ball.speed[1] += 1
        # Here you can also re-populate the bricks for the next level or go to the next stage

    if ball.rect.top > SCREEN_HEIGHT:
        lose_sound.play()
        pygame.time.wait(3000)  # wait for a few seconds to let the sound play
        print('Game Over')
        pygame.quit()
        sys.exit()

    # Clear screen
    screen.fill(BLACK)

    # Draw game objects
    all_sprites.draw(screen)

    # Display the score
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (20, SCREEN_HEIGHT - 40))

    # Refresh screen
    pygame.display.flip()

    # Set FPS
    pygame.time.Clock().tick(60)
