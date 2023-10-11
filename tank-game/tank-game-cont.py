# Additional imports
from pygame import mixer

import pygame
import sys
import math
import random

# Initialize pygame
pygame.init()

# Screen configuration
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0,0,0)

# Tank configuration
TANK_COLOR_1 = (0, 255, 0)
TANK_COLOR_2 = (255, 0, 0)
TANK_RADIUS = 20
BULLET_COLOR = (255, 255, 0)
BULLET_RADIUS = 5

# Sound effects
BULLET_SOUND = 'bullet.wav'  # Add the path to your bullet sound file
EXPLOSION_SOUND = 'explosion.wav'  # Add the path to your explosion sound file
# Load sound effects
mixer.init()
bullet_sound = mixer.Sound(BULLET_SOUND)
explosion_sound = mixer.Sound(EXPLOSION_SOUND)
# Load tank sprite
TANK_SPRITE = pygame.image.load('tank.png')  # Change to the path of your tank sprite


# Text configuration
FONT = pygame.font.Font(None, 36)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tank Battle')

def game_over(winner):
    screen.fill(BACKGROUND_COLOR)
    game_over_text = FONT.render('GAME OVER', True, (255, 255, 255))
    winner_text = FONT.render(f'{winner} WINS!', True, (255, 255, 255))
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - game_over_text.get_height()//2))
    screen.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2 + game_over_text.get_height()))
    pygame.display.flip()
    pygame.time.wait(3000)

class Bullet:
    def __init__(self, x, y, angle, color):
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color
        self.speed = 5

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), BULLET_RADIUS)

    def move(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

class Tank:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.angle = 0
        self.bullets = []
        self.score = 0

    """
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), TANK_RADIUS)
        gun_x = self.x + math.cos(math.radians(self.angle)) * TANK_RADIUS
        gun_y = self.y + math.sin(math.radians(self.angle)) * TANK_RADIUS
        pygame.draw.line(screen, self.color, (self.x, self.y), (gun_x, gun_y), 5)
        for bullet in self.bullets:
            bullet.draw()

        score_text = FONT.render(str(self.score), True, self.color)
        screen.blit(score_text, (self.x - TANK_RADIUS, self.y - TANK_RADIUS - 20))
    """

    def draw(self):
        rotated_tank = pygame.transform.rotate(TANK_SPRITE, self.angle)
        rect = rotated_tank.get_rect(center=(self.x, self.y))
        screen.blit(rotated_tank, rect.topleft)
        
        for bullet in self.bullets:
            bullet.draw()

    def move(self, x, y):
        self.x = max(min(self.x + x, WIDTH - TANK_RADIUS), TANK_RADIUS)
        self.y = max(min(self.y + y, HEIGHT - TANK_RADIUS), TANK_RADIUS)

    def rotate(self, angle):
        self.angle += angle

    def shoot(self):
        bullet_x = self.x + math.cos(math.radians(self.angle)) * (TANK_RADIUS + BULLET_RADIUS)
        bullet_y = self.y + math.sin(math.radians(self.angle)) * (TANK_RADIUS + BULLET_RADIUS)
        bullet = Bullet(bullet_x, bullet_y, self.angle, BULLET_COLOR)
        self.bullets.append(bullet)

# Instantiate two tanks
tank1 = Tank(100, HEIGHT//2, TANK_COLOR_1)
tank2 = Tank(WIDTH-100, HEIGHT//2, TANK_COLOR_2)

while True:
    screen.fill(BACKGROUND_COLOR)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tank1.shoot()
                bullet_sound.play()
            if event.key == pygame.K_RETURN:
                tank2.shoot()
                bullet_sound.play()
            if event.key == pygame.K_r:
                tank1 = Tank(100, HEIGHT//2, TANK_COLOR_1)
                tank2 = Tank(WIDTH-100, HEIGHT//2, TANK_COLOR_2)

    keys = pygame.key.get_pressed()
    
    # ... (The previous tank control code remains unchanged)
    # MANUALLY PASTE START moving code
    # Tank1 controls
    if keys[pygame.K_w]:
        tank1.move(0, -2)
    if keys[pygame.K_s]:
        tank1.move(0, 2)
    if keys[pygame.K_a]:
        tank1.move(-2, 0)
    if keys[pygame.K_d]:
        tank1.move(2, 0)
    if keys[pygame.K_q]:
        tank1.rotate(-2)
    if keys[pygame.K_e]:
        tank1.rotate(2)

    # Tank2 controls
    if keys[pygame.K_UP]:
        tank2.move(0, -2)
    if keys[pygame.K_DOWN]:
        tank2.move(0, 2)
    if keys[pygame.K_LEFT]:
        tank2.move(-2, 0)
    if keys[pygame.K_RIGHT]:
        tank2.move(2, 0)
    if keys[pygame.K_m]:
        tank2.rotate(-2)
    if keys[pygame.K_n]:
        tank2.rotate(2)
    # MANUALLY PASTE END moving code


    # Move and check bullet collisions
    for tank in [tank1, tank2]:
        for bullet in tank.bullets:
            bullet.move()
            if TANK_RADIUS + BULLET_RADIUS > math.hypot(tank1.x - bullet.x, tank1.y - bullet.y):
                tank2.score += 1
                tank.bullets.remove(bullet)
            elif TANK_RADIUS + BULLET_RADIUS > math.hypot(tank2.x - bullet.x, tank2.y - bullet.y):
                tank1.score += 1
                tank.bullets.remove(bullet)


    if tank1.score == 5:
        explosion_sound.play()
        game_over("TANK 1")
        tank1 = Tank(100, HEIGHT//2, TANK_COLOR_1)
        tank2 = Tank(WIDTH-100, HEIGHT//2, TANK_COLOR_2)
    elif tank2.score == 5:
        explosion_sound.play()
        game_over("TANK 2")
        tank1 = Tank(100, HEIGHT//2, TANK_COLOR_1)
        tank2 = Tank(WIDTH-100, HEIGHT//2, TANK_COLOR_2)

    tank1.draw()
    tank2.draw()

    pygame.display.flip()
    pygame.time.Clock().tick(60)
