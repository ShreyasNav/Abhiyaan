import pygame
import random
import math

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
NUM_ROBOTS = 10
ROBOT_SIZE = 20
TARGET_SIZE = 20
ROBOT_SPEED = 2
GAP_DISTANCE = 50

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Robot class
class Robot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((ROBOT_SIZE, ROBOT_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = ROBOT_SPEED

    def update(self, target_pos, robots):
        # Move towards target
        angle = math.atan2(target_pos[1] - self.rect.centery, target_pos[0] - self.rect.centerx)
        dx = self.speed * math.cos(angle)
        dy = self.speed * math.sin(angle)
        self.rect.x += dx
        self.rect.y += dy

        # Avoid collisions with other robots
        for robot in robots:
            if robot != self:
                ##if pygame.sprite.collide_rect(self, robot):
                dist = math.hypot(self.rect.centerx - robot.rect.centerx, self.rect.centery - robot.rect.centery)
                if dist < GAP_DISTANCE:
                    self.rect.x -= dx
                    self.rect.y -= dy
                    break

# Target class
class Target(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TARGET_SIZE, TARGET_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Create sprites
all_sprites = pygame.sprite.Group()
robots = pygame.sprite.Group()
for _ in range(NUM_ROBOTS):
    robot = Robot(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
    robots.add(robot)
    all_sprites.add(robot)

target = Target(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
all_sprites.add(target)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update robots
    for robot in robots:
        robot.update(target.rect.center, robots)

    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


