import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Circle Sprite Example")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

speed = 200  # Speed in pixels per second

clock = pygame.time.Clock()

# Define states
MENU = 0
GAME = 1
GAME_OVER = 2


# Create a Sprite class
class CircleSprite(pygame.sprite.Sprite):
    def __init__(self, color, radius, x, y):
        super().__init__()
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction_x = 0
        self.direction_y = 0

    def update(self, dt):
        self.rect.x += speed * self.direction_x * dt
        self.rect.y += speed * self.direction_y * dt

class Bullet(pygame.sprite.Sprite):
    def __init__(self, color, radius, x, y):
        super().__init__()
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction_x = 0
        self.direction_y = 0

    def update(self, dt):
        self.rect.x += speed * self.direction_x * dt
        self.rect.y += speed * self.direction_y * dt

class Enemy(pygame.sprite.Sprite):
    def __init__(self, color, radius):
        super().__init__()
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(radius, screen_width - radius),
                            random.randint(radius, screen_height - radius))
        self.radius = radius
        self.speed = 100  # Speed in pixels per second

    def update(self, dt, player_pos):
        # Calculate direction towards player
        player_x, player_y = player_pos
        enemy_x, enemy_y = self.rect.center

        # Calculate distance and direction
        dx = player_x - enemy_x
        dy = player_y - enemy_y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance != 0:
            dx /= distance  # Normalize direction
            dy /= distance  # Normalize direction

        # Update position
        self.rect.x += dx * self.speed * dt
        self.rect.y += dy * self.speed * dt


def display_text(screen, text, font_size, color, x, y):
    font = pygame.font.Font("pixel_font.ttf", font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def handle_sprite_movement(keys, sprite):
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        sprite.direction_x = -1
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        sprite.direction_x = 1
    else:
        sprite.direction_x = 0

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        sprite.direction_y = -1
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        sprite.direction_y = 1
    else:
        sprite.direction_y = 0


# Create sprites
circle_radius = 30
circle_sprite = CircleSprite(RED, circle_radius, screen_width // 2, screen_height // 2)

enemy_radius = 20

# Create sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(circle_sprite)

enemies = pygame.sprite.Group()

# Timing variables
enemy_spawn_event = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_spawn_event, 3000)  # Spawn an enemy every 3 seconds


def reset_game():
    global circle_sprite
    global enemies
    global all_sprites

    # Clear existing sprites
    all_sprites.empty()
    enemies.empty()

    # Reinitialize player sprite
    circle_sprite = CircleSprite(RED, circle_radius, screen_width // 2, screen_height // 2)
    all_sprites.add(circle_sprite)

    # Reinitialize enemies
    enemies.empty()  # Ensures no leftover enemies
    all_sprites.remove(enemies)


# Main game loop
current_state = MENU
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Calculate delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == enemy_spawn_event:
            # Spawn a new enemy
            new_enemy = Enemy((255, 200, 200), enemy_radius)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # Handle state-specific logic
    keys = pygame.key.get_pressed()
    if current_state == MENU:
        if keys[pygame.K_RETURN]:  # Enter key to start the game
            current_state = GAME
    elif current_state == GAME:
        handle_sprite_movement(keys, circle_sprite)

        # Update CircleSprite
        circle_sprite.update(dt)

        # Update enemies with the player's position
        for enemy in enemies:
            enemy.update(dt, circle_sprite.rect.center)

        # Check for collisions
        if pygame.sprite.spritecollide(circle_sprite, enemies, False):
            current_state = GAME_OVER
    elif current_state == GAME_OVER:
        display_text(screen, "Game Over! Press R to Restart", 36, WHITE, screen_width // 2, screen_height // 2)

        # Handle restarting the game
        if keys[pygame.K_r]:  # R key to restart
            reset_game()
            current_state = GAME
        elif keys[pygame.K_ESCAPE]:  # Escape to quit
            running = False

    # Clear screen and draw
    screen.fill(BLACK)

    if current_state == MENU:
        display_text(screen, "Press ENTER to Start", 36, WHITE, screen_width // 2, screen_height // 2)
    elif current_state == GAME:
        all_sprites.draw(screen)
        enemies.draw(screen)
    elif current_state == GAME_OVER:
        padding = 50
        display_text(screen, "Game Over! ", 64, RED, screen_width // 2, screen_height // 2)
        display_text(screen, "Press R to Restart", 36, WHITE, screen_width // 2, (screen_height // 2)+padding)

    pygame.display.flip()

pygame.quit()
sys.exit()
