import sys
from random import randint
from types import MethodType

import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class GameObject:
    """
    Manages a game object (white rect)
    """
    def __init__(self, init_x, init_y, width, height, velocity) -> None:
        self.init_x = init_x
        self.init_y = init_y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(init_x, init_y, width, height)

        self.velocity = velocity
        self.direction: complex = 0

    def reset(self):
        """
        Reset game object to initial settings
        """
        self.rect.left = self.init_x
        self.rect.top = self.init_y
        self.direction = 0

    def move(self):
        """
        Move the game object
        """
        
        self.rect.x += self.velocity * self.direction.real
        self.rect.y += self.velocity * self.direction.imag

class GameManager:
    """
    Manages the game and implements the game logic
    """

    WIDTH = 800
    HEIGHT = 600

    PLAYER_RECT_WIDTH = 10
    PLAYER_RECT_HEIGHT = 125
    PLAYER_RECT_SCREEN_OFFSET = 10

    PLAYER_VELOCITY = 10

    BALL_SIZE = 20
    BALL_DIRECTION_OPTIONS = [1 + 1j, 1 - 1j, -1 + 1j, -1 -1j]

    BALL_VELOCITY = 5

    GET_BALL_DIRECTION = lambda *args: GameManager.BALL_DIRECTION_OPTIONS[randint(0, 3)] #pylint: disable=unnecessary-lambda-assignment

    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pong over Ping")

        self.clock = pygame.time.Clock()
        self.running = True

        

        self.font = pygame.font.Font(None, 72)

        self.player: GameObject | None = None
        self.enemy: GameObject | None = None
        self.ball: GameObject | None = None

        self.player_score = 0
        self.enemy_score = 0

        self.initialize_game_objects()

        self.game_objects: list[GameObject] = [self.ball, self.player, self.enemy]
        self.exclude_ball_slice = slice(1,None)


    def initialize_game_objects(self):
        """
        Initialize the game objects
        """
        player_rect_x = self.PLAYER_RECT_SCREEN_OFFSET
        player_rect_y = (self.HEIGHT - self.PLAYER_RECT_HEIGHT) / 2
        self.player = GameObject(player_rect_x, player_rect_y, self.PLAYER_RECT_WIDTH, self.PLAYER_RECT_HEIGHT, self.PLAYER_VELOCITY)

        enemy_rect_x = self.WIDTH - self.PLAYER_RECT_SCREEN_OFFSET - self.PLAYER_RECT_WIDTH
        enemy_rect_y = (self.HEIGHT - self.PLAYER_RECT_HEIGHT) / 2
        self.enemy = GameObject(enemy_rect_x, enemy_rect_y, self.PLAYER_RECT_WIDTH, self.PLAYER_RECT_HEIGHT, self.PLAYER_VELOCITY)

        ball_x = (self.WIDTH - self.BALL_SIZE) / 2
        ball_y = (self.HEIGHT - self.BALL_SIZE) / 2
        self.ball = GameObject(ball_x, ball_y, self.BALL_SIZE, self.BALL_SIZE, self.BALL_VELOCITY)

        def ball_reset(self: GameObject):
            self.reset()
            self.direction = GameManager.GET_BALL_DIRECTION()

        self.ball.ball_reset = MethodType(ball_reset, self.ball) # pylint: disable=attribute-defined-outside-init
        self.ball.ball_reset()

    def main_loop(self):
        """
        Handles the logic for the main loop of the game
        """
        #pylint: disable=no-member
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_UP:
                            self.enemy.direction = -1j
                        case pygame.K_DOWN:
                            self.enemy.direction = 1j
                        case pygame.K_w:
                            self.player.direction = -1j
                        case pygame.K_s:
                            self.player.direction = 1j

                        case pygame.K_SPACE:
                            self.ball.ball_reset()
                            # self.ball.reset()
                            # self.ball.direction = self.GET_BALL_DIRECTION()

                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_UP, pygame.K_DOWN):
                        self.enemy.direction = 0
                    if event.key in (pygame.K_w, pygame.K_s):
                        self.player.direction = 0



            for gameobj in self.game_objects:
                gameobj.move()


            if self.ball.rect.colliderect(self.player.rect) \
               or self.ball.rect.colliderect(self.enemy.rect) \
               or self.ball.rect.top < 0 \
               or self.ball.rect.bottom > self.HEIGHT:
                self.ball.direction *= 1j

            for gameobj in self.game_objects[self.exclude_ball_slice]:
                if gameobj.rect.top < 0:
                    gameobj.rect.top = 0
                if gameobj.rect.bottom > self.HEIGHT:
                    gameobj.rect.bottom = self.HEIGHT

            if self.ball.rect.left < 0:
                self.player_score += 1
                self.ball.ball_reset()
            if self.ball.rect.right > self.WIDTH:
                self.enemy_score += 1
                self.ball.ball_reset()

            self.screen.fill(BLACK)

            for gameobj in self.game_objects:
                pygame.draw.rect(self.screen, WHITE, gameobj.rect)

            scoreboard = self.font.render(f'{self.enemy_score} - {self.player_score}', True, WHITE)
            score_rect = scoreboard.get_rect(center=(self.WIDTH//2, 50))  # Center text on the screen
            self.screen.blit(scoreboard, score_rect)

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(60)

    def run(self):
        """
        Run the game and gracegully exit upon exit event
        """
        #pylint: disable=no-member
        self.main_loop()
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    GameManager().run()
