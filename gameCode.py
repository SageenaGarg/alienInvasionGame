import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)

# Player settings
player_speed = 5
bullet_speed = 7

# Alien settings
alien_size = 50
alien_speed = 3
alien_spawn_rate = 25

# Bullet settings
bullet_size = 5
bullets = []
hit_bullets = []

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Invasion")
clock = pygame.time.Clock()

# Load images
original_player_image = pygame.image.load("ship.jpeg").convert_alpha()
ufo_image = pygame.image.load("ufo.jpg").convert_alpha()

# Scale the player image to match the alien size
scaled_player_image = pygame.transform.scale(original_player_image, (alien_size, alien_size))
scaled_ufo_image = pygame.transform.scale(ufo_image, (alien_size, alien_size))

# Get the rect of the scaled player image for positioning
player_rect = scaled_player_image.get_rect()

# Initial player position
player_rect.centerx = WIDTH // 2
player_rect.bottom = HEIGHT - 10

# Initialize the 'aliens' list
aliens = []


# Function to draw the player
def draw_player():
    screen.blit(scaled_player_image, player_rect)

# Function to draw aliens
def draw_aliens():
    for alien in aliens:
        screen.blit(scaled_ufo_image, (alien[0], alien[1]))

# Function to draw bullets
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, BLUE, (bullet[0], bullet[1], bullet_size, bullet_size))

# Function to draw text on the screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Create a font object
font = pygame.font.Font(None, 36)

# Initialize points
points = 0

# ... (previous code remains unchanged)

# Game state
start_screen = True
playing_game = False
game_over = False  # Add a new game over state

# Main game loop
while not playing_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing_game = True  # Exit the game loop
        elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
            start_screen = False
            playing_game = True

    screen.fill((0, 0, 0))
    draw_text("Press Space to Play", font, WHITE, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    clock.tick(FPS)

# Main game loop
while playing_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing_game = False  # Exit the game loop
        # Handle shooting
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append([player_rect.centerx - bullet_size // 2, player_rect.top])

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed

    # Move bullets upward
    for bullet in bullets:
        bullet[1] -= bullet_speed

    # Remove bullets that go off-screen
    bullets = [bullet for bullet in bullets if bullet[1] > 0]

    # Spawn aliens randomly
    if random.randint(1, alien_spawn_rate) == 1:
        alien_x = random.randint(0, WIDTH - alien_size)
        alien_y = random.randint(-alien_size, 0)
        aliens.append([alien_x, alien_y])

    # Move aliens downward
    for alien in aliens:
        alien[1] += alien_speed

    # Remove aliens that go off-screen and update points
    aliens = [alien for alien in aliens if alien[1] < HEIGHT]

    # Check for collisions between bullets and aliens
    for bullet in bullets:
        for alien in aliens:
            if (
                bullet[0] < alien[0] + alien_size
                and bullet[0] + bullet_size > alien[0]
                and bullet[1] < alien[1] + alien_size
                and bullet[1] + bullet_size > alien[1]
            ):
                bullets.remove(bullet)
                hit_bullets.append(bullet)
                aliens.remove(alien)
                points += 1

    # Check for collisions between player and aliens
    for alien in aliens:
        if player_rect.colliderect(pygame.Rect(alien[0], alien[1], alien_size, alien_size)):
            print("Game Over!")
            game_over = True  # Set game over state
            playing_game = False  # Exit the game loop

    # Clear the screen
    screen.fill((212, 241, 244))

    # Draw the player, aliens, and bullets
    draw_player()
    draw_aliens()
    draw_bullets()

    # Draw the text on the screen
    draw_text(f"Points: {points}", font, BLACK, WIDTH - 100, 30)

    # Update the display
    pygame.display.flip()

    # Set the frames per second
    clock.tick(FPS)

# Game over loop
while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False  # Exit the game over loop

    screen.fill((0, 0, 0))
    draw_text("Game Over! Press Q to Quit", font, WHITE, WIDTH // 2, HEIGHT // 2)

    pygame.display.flip()
    clock.tick(FPS)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        game_over = False  # Exit the game over loop
