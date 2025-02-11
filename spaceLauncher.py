import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FPS = 60

# Spaceship Settings
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50
ASTEROID_WIDTH, ASTEROID_HEIGHT = 40, 40

# Game Variables
level = 1
lives = 3
score = 0

# Create Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Launcher")

# Load Assets
spaceship_img = pygame.image.load("spaceship.jpg")
spaceship_img = pygame.transform.scale(spaceship_img, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

# Spaceship Class
class Spaceship:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 80
        self.vel = 5
    
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vel
        if keys[pygame.K_RIGHT] and self.x < WIDTH - SPACESHIP_WIDTH:
            self.x += self.vel
    
    def draw(self):
        screen.blit(spaceship_img, (self.x, self.y))

# Asteroid Class
class Asteroid:
    def __init__(self, speed):
        self.x = random.randint(0, WIDTH - ASTEROID_WIDTH)
        self.y = -ASTEROID_HEIGHT
        self.speed = speed
    
    def move(self):
        self.y += self.speed
    
    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, ASTEROID_WIDTH, ASTEROID_HEIGHT))

# Main Game Loop
def main():
    global level, lives, score
    run = True
    clock = pygame.time.Clock()
    player = Spaceship()
    asteroids = []
    
    while run:
        clock.tick(FPS)
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()
        
        # Check for Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        # Spawn Asteroids
        if random.randint(1, 50) == 1:
            asteroids.append(Asteroid(level))
        
        # Move and Draw Asteroids
        for asteroid in asteroids[:]:
            asteroid.move()
            asteroid.draw()
            
            # Collision Detection
            if (asteroid.y + ASTEROID_HEIGHT >= player.y and
                player.x < asteroid.x < player.x + SPACESHIP_WIDTH):
                lives -= 1
                asteroids.remove(asteroid)
                if lives == 0:
                    print("Game Over!")
                    run = False
            
            # Remove Off-Screen Asteroids
            if asteroid.y > HEIGHT:
                asteroids.remove(asteroid)
                score += 1
        
        # Level Progression
        if score >= level * 10:
            level += 1
            print(f"Level Up! Now Level {level}")
        
        # Draw Spaceship
        player.move(keys)
        player.draw()
        
        # Display Score and Lives
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))
        
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()
