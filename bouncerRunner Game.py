import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 800
BALL_RADIUS = 20
GRAVITY = 0.5
JUMP_STRENGTH = -10
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bounce Runner")
clock = pygame.time.Clock()

# Ball class
class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.radius = BALL_RADIUS
        self.velocity_y = 0

    def move(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        if self.y > HEIGHT:
            self.reset()
    
    def reset(self):
        self.y = HEIGHT - 100
        self.velocity_y = JUMP_STRENGTH

    def jump(self):
        self.velocity_y = JUMP_STRENGTH

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x, int(self.y)), self.radius)

# Platform class
class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLATFORM_WIDTH
        self.height = PLATFORM_HEIGHT

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

# Generate platforms
platforms = [Platform(random.randint(0, WIDTH - PLATFORM_WIDTH), HEIGHT - i * 80) for i in range(10)]
ball = Ball()

# Game loop
running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball.jump()
    
    # Move ball
    ball.move()
    
    # Check for collision with platforms
    for platform in platforms:
        if platform.y < ball.y + BALL_RADIUS < platform.y + PLATFORM_HEIGHT and platform.x < ball.x < platform.x + PLATFORM_WIDTH:
            ball.jump()
    
    # Draw everything
    for platform in platforms:
        platform.draw()
    ball.draw()
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
