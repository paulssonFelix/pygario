import logging
import pygame
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Konstanter
FPS = 60
SCREEN_SIZE = (800, 600)
CAPTION = "Pygame Example"

# Game states
STATE_PREGAME = 1
STATE_RUNNING = 2

class Controller():
    """Game controller."""

    def __init__(self):
        """Initialize game controller."""
        self.fps = FPS

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()

        self.player = Player(self.screen)

        # Initialize game state
        self.game_state = STATE_PREGAME

    def run(self):
        """Main game loop."""
        while True:
            # Hantera event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # ALT + F4 or icon in upper right corner.
                    self.quit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # Escape key pressed.
                    self.quit()

                if self.game_state == STATE_PREGAME:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.game_state = STATE_RUNNING

                if self.game_state == STATE_RUNNING:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                        self.player.engine_on()

                    if event.type == pygame.KEYUP and event.key == pygame.K_w:
                        self.player.engine_off()

            # Hantera speltillstånd
            if self.game_state == STATE_PREGAME:
                pass

            if self.game_state == STATE_RUNNING:
                self.player.tick()
                self.screen.fill(pygame.Color('#000000'))
                self.player.draw()

            pygame.display.flip()

            self.clock.tick(self.fps)

    def quit(self):
        logging.info('Quitting... good bye!')
        pygame.quit()
        sys.exit()


class Player():
    def __init__(self, screen):
        self.x = SCREEN_SIZE[0] / 2
        self.y = SCREEN_SIZE[1] / 2
        self.screen = screen
        self.engine = False

    def draw(self):
        surface = pygame.Surface((20, 20))
        color = pygame.Color('#FF0000')
        pygame.draw.line(surface, color, (10, 0), (15, 20))
        pygame.draw.line(surface, color, (10, 0), (5, 20))

        self.screen.blit(surface, (self.x - 10, self.y - 10))

    def tick(self):
        if self.engine:
            self.y -= 1

        self.y += 0.5

    def engine_on(self):
        self.engine = True

    def engine_off(self):
        self.engine = False

if __name__ == "__main__":
    logger.info('Starting...')
    c = Controller()
    c.run()
