import logging
import pygame
import sys
import random
from math import sqrt, pi

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Konstanter
FPS = 30
SCREEN_SIZE = (1500, 1000)
CAPTION = "Pygame Example"
N_ENEMIES = 10
N_FOODS = 250
COLORS = {'player': pygame.Color('#00FF00'),
          'small_enemy': pygame.Color('#3333FF'),
          'big_enemy': pygame.Color('#FF0000'),
          'food': pygame.Color('#FFFFFF'),
          'text': pygame.Color('#FFFFFF')}

# Game states
STATE_PREGAME = 1
STATE_RUNNING = 2
STATE_GAMEOVER = 3

class Controller():
    """Spelkontrollern"""

    def __init__(self):
        """Initialisera spelkontrollern"""
        self.fps = FPS

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont('Arial', 100)
        self.font2 = pygame.font.SysFont('Arial', 50)
        self.enemies = []
        self.foods = []
        self.player = Player(self)
        for _ in range(N_ENEMIES):
            self.enemies.append(Enemy(self))
        for _ in range(N_FOODS):
            self.foods.append(Food(self.screen))

        # Initialisera speltillstånd
        self.game_state = STATE_PREGAME

    def run(self):
        """Spelets huvudloop"""
        while True:
            # Hantera event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # ALT + F4 eller ikonen i övre högra hörnet.
                    self.quit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # Escape knapp nedtryckt.
                    self.quit()

                if self.game_state == STATE_PREGAME:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.game_state = STATE_RUNNING

                if self.game_state == STATE_RUNNING:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                        self.player.up_on()

                    if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                        self.player.up_off()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                        self.player.down_on()

                    if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                        self.player.down_off()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                        self.player.left_on()

                    if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                        self.player.left_off()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                        self.player.right_on()

                    if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                        self.player.right_off()

                if self.game_state == STATE_GAMEOVER:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.game_state = STATE_RUNNING

            # Hantera speltillstånd
            if self.game_state == STATE_PREGAME:
                # Presentation av startskärmen
                surface = self.font.render('AGAR.IO', False, COLORS['text'])
                x = SCREEN_SIZE[0] / 2 - surface.get_width() / 2
                y = SCREEN_SIZE[1] / 2.3 - surface.get_height() / 2
                self.screen.fill(pygame.Color('#000000'))
                self.screen.blit(surface, (x, y))

                surface2 = self.font2.render('Press SPACE to start', False, COLORS['text'])
                x2 = SCREEN_SIZE[0] / 2 - surface2.get_width() / 2
                y2 = SCREEN_SIZE[1] / 1.8 - surface2.get_height() / 2
                self.screen.blit(surface2, (x2, y2))

            if self.game_state == STATE_RUNNING:
                self.screen.fill(pygame.Color('#000000'))

                self.player.tick()

                for e in self.enemies:
                    e.tick()

                for f in self.foods:
                    f.draw()

                self.player.draw()

                for e in self.enemies:
                    e.draw()

            # Omstart av spelets element
            if self.game_state == STATE_GAMEOVER:
                self.enemies.clear()
                for _ in range(N_ENEMIES):
                    self.enemies.append(Enemy(self))

                self.foods.clear()
                for _ in range(N_FOODS):
                    self.foods.append(Food(self.screen))

                self.player.x = SCREEN_SIZE[0] / 2
                self.player.y = SCREEN_SIZE[1] / 2
                self.player.radius = 20
                self.player.x_speed = 0
                self.player.y_speed = 0
                self.player.up = False
                self.player.down = False
                self.player.left = False
                self.player.right = False

                # Presentation av "GAME OVER"-skärmen
                surface = self.font.render('GAME OVER', False, COLORS['text'])
                x = SCREEN_SIZE[0] / 2 - surface.get_width() / 2
                y = SCREEN_SIZE[1] / 2.3 - surface.get_height() / 2
                self.screen.fill(pygame.Color('#000000'))
                self.screen.blit(surface, (x, y))

                surface2 = self.font2.render('Press SPACE to restart', False, COLORS['text'])
                x2 = SCREEN_SIZE[0] / 2 - surface2.get_width() / 2
                y2 = SCREEN_SIZE[1] / 1.8 - surface2.get_height() / 2
                self.screen.blit(surface2, (x2, y2))

            pygame.display.flip()

            self.clock.tick(self.fps)


    def quit(self):
        logging.info('Quitting... good bye!')
        pygame.quit()
        sys.exit()

    def add_food(self):
        self.foods.append(Food(self.screen))

    def remove_food(self, food):
        self.foods.remove(food)

    def add_enemy(self):
        self.enemies.append(Enemy(self))

    def remove_enemy(self, enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)



class Food():
    def __init__(self, screen):
        self.radius = 5
        self.x = random.randint(self.radius, SCREEN_SIZE[0] - self.radius)
        self.y = random.randint(self.radius, SCREEN_SIZE[1] - self.radius)
        self.screen = screen

    def draw(self):
        surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, COLORS['food'], (self.radius, self.radius), (self.radius))

        self.screen.blit(surface, (self.x - self.radius, self.y - self.radius))


class Player():
    def __init__(self, controller):
        self.x = SCREEN_SIZE[0] / 2
        self.y = SCREEN_SIZE[1] / 2
        self.radius = 20
        self.x_speed = 0
        self.y_speed = 0
        self.acceleration = 0.2
        self.controller = controller
        self.enemies = controller.enemies
        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def draw(self):
        surface = pygame.Surface((int(self.radius) * 2, int(self.radius) * 2), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, COLORS['player'], (int(self.radius), int(self.radius)), (int(self.radius)))

        self.controller.screen.blit(surface, (self.x - int(self.radius), self.y - int(self.radius)))

    def tick(self):
        # Kontrollera om spelaren är uppäten
        for enemy in self.enemies:
            if (enemy.radius > self.radius * 1.1) and sqrt(((self.x - enemy.x) ** 2) + ((self.y - enemy.y) ** 2)) <= enemy.radius - (self.radius / 2):
                self.controller.game_state = STATE_GAMEOVER

        # Kontrollera ätandet av födan
        for food in self.controller.foods:
            if sqrt(((food.x - self.x) ** 2) + ((food.y - self.y) ** 2)) <= self.radius - (food.radius / 2):
                self.controller.remove_food(food)
                self.controller.add_food()
                self.radius = sqrt(((pi * (self.radius ** 2)) + (pi * (food.radius ** 2))) / pi)

        # Kontrollera ätandet av fiender
        for enemy in self.controller.enemies:
            if sqrt(((enemy.x - self.x) ** 2) + ((enemy.y - self.y) ** 2)) <= self.radius - (enemy.radius / 2):
                self.controller.remove_enemy(enemy)
                self.controller.add_enemy()
                self.radius = sqrt(((pi * (self.radius ** 2)) + (pi * (enemy.radius ** 2))) / pi)

        # Vid kollision i vänstra sidan
        if self.x <= self.radius:
            self.x = self.radius
            self.x_speed = 0

        # Vid kollision i högra sidan
        if self.x >= SCREEN_SIZE[0] - self.radius:
            self.x = SCREEN_SIZE[0] - self.radius
            self.x_speed = 0

        # Vid kollision i övre sidan
        if self.y <= self.radius:
            self.y = self.radius
            self.y_speed = 0

        # Vid kollision i nedre sidan
        if self.y >= SCREEN_SIZE[1] - self.radius:
            self.y = SCREEN_SIZE[1] - self.radius
            self.y_speed = 0

        if self.up:
            self.y_speed -= self.acceleration

        if self.down:
            self.y_speed += self.acceleration

        if self.left:
            self.x_speed -= self.acceleration

        if self.right:
            self.x_speed += self.acceleration

        # Beräkna ny position
        self.x = self.x + self.x_speed
        self.y = self.y + self.y_speed

        # Deacceleration
        self.x_speed = self.x_speed * 0.96
        self.y_speed = self.y_speed * 0.96

    def up_on(self):
        self.up = True

    def up_off(self):
        self.up = False

    def down_on(self):
        self.down = True

    def down_off(self):
        self.down = False

    def left_on(self):
        self.left = True

    def left_off(self):
        self.left = False

    def right_on(self):
        self.right = True

    def right_off(self):
        self.right = False


class Enemy():
    def __init__(self, controller):
        self.radius = 20
        self.x = random.randint(self.radius, SCREEN_SIZE[0] - self.radius)
        self.y = random.randint(self.radius, SCREEN_SIZE[1] - self.radius)
        self.x_speed = 0
        self.y_speed = 0
        self.acceleration = 0.2
        self.controller = controller
        self.player = controller.player

    def draw(self):
        color = COLORS['small_enemy']
        surface = pygame.Surface((int(self.radius) * 2, int(self.radius) * 2), pygame.SRCALPHA, 32)

        if self.radius >= self.player.radius * 1.1:
            color = COLORS['big_enemy']
        else:
            color = COLORS['small_enemy']

        pygame.draw.circle(surface, color, (int(self.radius), int(self.radius)), (int(self.radius)))
        self.controller.screen.blit(surface, (self.x - self.radius, self.y - int(self.radius)))

    def tick(self):
        enemies = [enemy for enemy in self.controller.enemies if not enemy is self]
        if self.player not in enemies:
            enemies.append(self.player)
        # logger.debug('enemies: {}'.format(enemies))

        closest_food = []
        closest_enemy = []

        for enemy in enemies:
            if (not closest_enemy) or (sqrt(((enemy.x - self.x) ** 2) + ((enemy.y - self.y) ** 2)) < sqrt(((closest_enemy[0].x - self.x) ** 2) + ((closest_enemy[0].y - self.y) ** 2))):
                closest_enemy.clear()
                closest_enemy.append(enemy)

        # Kontrollera ätandet av födan
        for food in self.controller.foods:
            if sqrt(((food.x - self.x) ** 2) + ((food.y - self.y) ** 2)) <= self.radius - (food.radius / 2):
                self.controller.remove_food(food)
                self.controller.add_food()
                self.radius = sqrt(((pi * (self.radius ** 2)) + (pi * (food.radius ** 2))) / pi)

        for enemy in enemies:
            if (self.radius >= closest_enemy[0].radius * 1.1) and sqrt(((enemy.x - self.x) ** 2) + ((enemy.y - self.y) ** 2)) <= self.radius - (enemy.radius / 2):
                self.controller.remove_enemy(enemy)
                self.controller.add_enemy()
                self.radius = sqrt(((pi * (self.radius ** 2)) + (pi * (enemy.radius ** 2))) / pi)

        # Vid kollision i vänstra sidan
        if self.x <= self.radius:
            self.x = self.radius
            self.x_speed = 0

        # Vid kollision i högra sidan
        if self.x >= SCREEN_SIZE[0] - self.radius:
            self.x = SCREEN_SIZE[0] - self.radius
            self.x_speed = 0

        # Vid kollision i övre sidan
        if self.y <= self.radius:
            self.y = self.radius
            self.y_speed = 0

        # Vid kollision i nedre sidan
        if self.y >= SCREEN_SIZE[1] - self.radius:
            self.y = SCREEN_SIZE[1] - self.radius
            self.y_speed = 0

        if (self.radius < closest_enemy[0].radius * 1.1):
            # Håll avstånd från spelaren
            if (sqrt(((self.x - closest_enemy[0].x) ** 2) + ((self.y - closest_enemy[0].y) ** 2)) <= (self.radius + closest_enemy[0].radius) * 1.2):
                if self.y > closest_enemy[0].y and not self.y > SCREEN_SIZE[1] - 100:
                    self.y_speed += self.acceleration

                if self.y < closest_enemy[0].y and not self.y < 100:
                    self.y_speed -= self.acceleration

                if self.x > closest_enemy[0].x and not self.x > SCREEN_SIZE[0] - 100:
                    self.x_speed += self.acceleration

                if self.x < closest_enemy[0].x and not self.x < 100:
                    self.x_speed -= self.acceleration

            else:
                # Hitta närmaste föda och åk över den
                for food in self.controller.foods:
                    if (not closest_food) or (sqrt(((food.x - self.x) ** 2) + ((food.y - self.y) ** 2)) < sqrt(((closest_food[0].x - self.x) ** 2) + ((closest_food[0].y - self.y) ** 2))):
                        closest_food.clear()
                        closest_food.append(food)

                if self.y > closest_food[0].y:
                    self.y_speed -= self.acceleration

                if self.y < closest_food[0].y:
                    self.y_speed += self.acceleration

                if self.x > closest_food[0].x:
                    self.x_speed -= self.acceleration

                if self.x < closest_food[0].x:
                    self.x_speed += self.acceleration

        else:
            # Åk över spelaren
            if self.y > closest_enemy[0].y:
                self.y_speed -= self.acceleration

            if self.y < closest_enemy[0].y:
                self.y_speed += self.acceleration

            if self.x > closest_enemy[0].x:
                self.x_speed -= self.acceleration

            if self.x < closest_enemy[0].x:
                self.x_speed += self.acceleration

        # Beräkna ny position
        self.x = self.x + self.x_speed
        self.y = self.y + self.y_speed

        # Deacceleration
        self.x_speed = self.x_speed * 0.96
        self.y_speed = self.y_speed * 0.96

if __name__ == "__main__":
    logger.info('Starting...')
    c = Controller()
    c.run()
