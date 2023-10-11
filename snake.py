import sys
import pygame
import random

# Initialize pygame
pygame.init()

# Set screen dimensions
WIDTH, HEIGHT = 640, 480
BACKGROUND_COLOR = (0,0,0)
SNAKE_COLOR = (0,255,0)
FOOD_COLOR = (255,0,0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

class Snake:
    def __init__(self):
        self.position = [100, 50]
        self.body = [[100,50], [90,50], [80,50]]
        self.direction = 'RIGHT'

    def change_direction(self, new_direction):
        if new_direction == 'RIGHT' and not self.direction == 'LEFT':
            self.direction = 'RIGHT'
        if new_direction == 'LEFT' and not self.direction == 'RIGHT':
            self.direction = 'LEFT'
        if new_direction == 'UP' and not self.direction == 'DOWN':
            self.direction = 'UP'
        if new_direction == 'DOWN' and not self.direction == 'UP':
            self.direction = 'DOWN'

    def move(self, food_position):
        if self.direction == 'RIGHT':
            self.position[0] += 10
        if self.direction == 'LEFT':
            self.position[0] -= 10
        if self.direction == 'UP':
            self.position[1] -= 10
        if self.direction == 'DOWN':
            self.position[1] += 10

        self.body.insert(0, list(self.position))

        if self.position == food_position:
            return True
        else:
            self.body.pop()
            return False

    def check_collision(self):
        if self.position[0] < 0 or \
            self.position[0] > WIDTH-10 or \
            self.position[1] < 0 or \
            self.position[1] > HEIGHT-10 :
            return True
        for segment in self.body[1:]:
            if segment == self.position:
                return True
        return False

    def get_head_position(self):
        return self.position

    def get_body(self):
        return self.body

class Food:
    def __init__(self):
        self.position = [random.randrange(1, WIDTH/10) * 10, random.randrange(1, HEIGHT/10) * 10]
        self.is_food_on_screen = True

    def spawn_food(self):
        if not self.is_food_on_screen:
            self.position = [random.randrange(1, WIDTH/10) * 10, random.randrange(1, HEIGHT/10) * 10]
            self.is_food_on_screen = True
        return self.position

    def set_food_on_screen(self, choice):
        self.is_food_on_screen = choice


# Initialize snake and food
snake = Snake()
food = Food()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction('UP')
            if event.key == pygame.K_DOWN:
                snake.change_direction('DOWN')
            if event.key == pygame.K_LEFT:
                snake.change_direction('LEFT')
            if event.key == pygame.K_RIGHT:
                snake.change_direction('RIGHT')

    food_position = food.spawn_food()
    if snake.move(food_position):
        food.set_food_on_screen(False)

    if snake.check_collision():
        break

    screen.fill(BACKGROUND_COLOR)
    for position in snake.get_body():
        pygame.draw.rect(screen, SNAKE_COLOR, pygame.Rect(position[0], position[1], 10, 10))

    pygame.draw.rect(screen, FOOD_COLOR, pygame.Rect(food_position[0], food_position[1], 10, 10))
    pygame.display.flip()

    pygame.time.Clock().tick(10)
