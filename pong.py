#pylint: disable=no-member, invalid-name
import sys
from random import randint

import pygame

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Game Loop")

PLAYER_RECT_WIDTH = 10
PLAYER_RECT_HEIGHT = 125
PLAYER_RECT_SCREEN_OFFSET = 10

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the game loop
clock = pygame.time.Clock()
RUNNING = True

# Update game logic here
player_rect_x = PLAYER_RECT_SCREEN_OFFSET
player_rect_y = (HEIGHT - PLAYER_RECT_HEIGHT) / 2

enemy_rect_x = WIDTH - PLAYER_RECT_SCREEN_OFFSET - PLAYER_RECT_WIDTH
enemy_rect_y = (HEIGHT - PLAYER_RECT_HEIGHT) / 2

VELOCITY = 10

player_velocity = 0
enemy_velocity = 0

player_score = 0
enemy_score = 0

enemy_rect = pygame.Rect(enemy_rect_x, enemy_rect_y, PLAYER_RECT_WIDTH, PLAYER_RECT_HEIGHT)
player_rect = pygame.Rect(player_rect_x, player_rect_y, PLAYER_RECT_WIDTH, PLAYER_RECT_HEIGHT)

BALL_SIZE = 20
ball_X = (WIDTH - BALL_SIZE) / 2
ball_y = (HEIGHT - BALL_SIZE) / 2

ball_rect = pygame.Rect(ball_X, ball_y, BALL_SIZE, BALL_SIZE)

ball_direction_options = [1 + 1j, 1 - 1j, -1 + 1j, -1 -1j]

def reset_game():
    global ball_velocity
    ball_velocity = VELOCITY / 2 * ball_direction_options[randint(0, 3)]
    ball_rect.x = ball_X
    ball_rect.y = ball_y
    # player_rect.x = player_rect_x
    # player_rect.y = player_rect_y
    # enemy_rect.x = enemy_rect_x
    # enemy_rect.y = enemy_rect_y

reset_game()

# Set up the font
font = pygame.font.Font(None, 72)

while RUNNING:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_UP:
                    enemy_velocity = VELOCITY
                case pygame.K_DOWN:
                    enemy_velocity = -VELOCITY
                case pygame.K_w:
                    player_velocity = VELOCITY
                case pygame.K_s:
                    player_velocity = -VELOCITY

                case pygame.K_SPACE:
                    reset_game()

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                enemy_velocity = 0
            if event.key in (pygame.K_w, pygame.K_s):
                player_velocity = 0

    if ball_rect.colliderect(player_rect) \
       or ball_rect.colliderect(enemy_rect) \
       or ball_rect.top < 0 \
       or ball_rect.bottom > HEIGHT:
        ball_velocity *= 1j

    if ball_rect.left < 0:
        player_score += 1
        print('player scored')
        reset_game()
    if ball_rect.right > WIDTH:
        print('enemy scored')
        enemy_score += 1
        reset_game()

    player_rect.y -= player_velocity
    enemy_rect.y -= enemy_velocity

    if player_rect.top < 0:
        player_rect.top = 0
    if player_rect.bottom > HEIGHT:
        player_rect.bottom = HEIGHT
    if enemy_rect.top < 0:
        enemy_rect.top = 0
    if enemy_rect.bottom > HEIGHT:
        enemy_rect.bottom = HEIGHT
    
    ball_rect.x += ball_velocity.real
    ball_rect.y += ball_velocity.imag

    # Clear the screen
    screen.fill(BLACK)

    pygame.draw.rect(screen, WHITE, player_rect)

    pygame.draw.rect(screen, WHITE, enemy_rect)

    pygame.draw.rect(screen, WHITE, ball_rect)

    scoreboard = font.render(f'{enemy_score} - {player_score}', True, WHITE)
    score_rect = scoreboard.get_rect(center=(WIDTH//2, 50))  # Center text on the screen
    screen.blit(scoreboard, score_rect)


    # Draw objects here

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
