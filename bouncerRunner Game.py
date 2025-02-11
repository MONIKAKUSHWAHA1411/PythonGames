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
BLUE = (0, 0, 255)
BOMB_COLOR = (255, 0, 0)
LEVELS = 10
POWERUP_CHANCE = 0.2  # 20% chance of a power-up appearing on a platform
BOMB_CHANCE = 0.1  # 10% chance of a bomb appearing on a platform

def generate_platforms(level):
    platform_count = max(5, 15 - level)  # Fewer platforms as levels increase
    return [Platform(random.randint(0, WIDTH - PLATFORM_WIDTH), HEIGHT - i * 80, level) for i in range(platform_count)]

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
        self.has_powerup = False

    def move(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        if self.y > HEIGHT:
            self.reset()
    
    def reset(self):
        self.y = HEIGHT - 100
        self.velocity_y = JUMP_STRENGTH
        self.has_powerup = False

    def jump(self):
        self.velocity_y = JUMP_STRENGTH * (1.5 if self.has_powerup else 1)

    def draw(self):
        color = BLUE if self.has_powerup else RED
        pygame.draw.circle(screen, color, (self.x, int(self.y)), self.radius)

# Platform class
class Platform:
    def __init__(self, x, y, level):
        self.x = x
        self.y = y
        self.width = PLATFORM_WIDTH
        self.height = PLATFORM_HEIGHT
        self.has_powerup = random.random() < POWERUP_CHANCE
        self.has_bomb = random.random() < BOMB_CHANCE
        self.moving = level >= 5  # Moving platforms appear in higher levels
        self.direction = random.choice([-1, 1])

    def move(self):
        if self.moving:
            self.x += self.direction * 2
            if self.x <= 0 or self.x + self.width >= WIDTH:
                self.direction *= -1

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
        if self.has_powerup:
            pygame.draw.circle(screen, BLUE, (self.x + self.width // 2, self.y - 10), 5)
        if self.has_bomb:
            pygame.draw.circle(screen, BOMB_COLOR, (self.x + self.width // 2, self.y - 10), 5)

ball = Ball()
current_level = 1
platforms = generate_platforms(current_level)

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
        platform.move()
        if platform.y < ball.y + BALL_RADIUS < platform.y + PLATFORM_HEIGHT and platform.x < ball.x < platform.x + PLATFORM_WIDTH:
            if platform.has_bomb:
                ball.reset()  # Bomb hits the ball, reset position
            else:
                ball.jump()
                if platform.has_powerup:
                    ball.has_powerup = True
                    platform.has_powerup = False
    
    # Level progression
    if ball.y < 50:  # Reaching near top advances level
        current_level += 1
        if current_level > LEVELS:
            print("You Win!")
            running = False
        else:
            platforms = generate_platforms(current_level)
            ball.reset()
    
    # Draw everything
    for platform in platforms:
        platform.draw()
    ball.draw()
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()


