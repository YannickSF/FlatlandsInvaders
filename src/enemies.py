
import pygame
import random
from src.variables import GAME_VARIABLES
from src.powers import PowerEnemy, PowerEnemy1, PowerEnemy2, PowerEnemy3


class Enemy(pygame.sprite.Sprite):
    MAX_HEALTH = 20
    VELOCITY = 1
    HIT = 0
    XP = 0

    def __init__(self, image, game, add_speed=GAME_VARIABLES.ENEMY_SPEED):
        super().__init__()

        self.game = game
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.all_attacks = pygame.sprite.Group()

        self.health = 0

        self.VELOCITY += add_speed
        self.add_speed = add_speed

    def remove(self):
        self.game.enemies.remove(self)

    def pattern(self, game):
        if self.rect.y >= 650:
            self.remove()
        else:
            # self.rect.x += self.VELOCITY
            self.rect.y += self.VELOCITY

    def context_collides(self, game):
        collides_player = game.check_collides(self, game.all_player)

        if type(self) in (Alien, Alien1, Alien2, Alien3, Boss1):

            if collides_player:
                game.player.health -= self.HIT
                self.remove()
                game.score += 1
                game.xp += self.XP

                if game.player.health <= 0:
                    game.game_over()

                game.spawn_on_die(self)
            else:
                self.pattern(game)

    def move(self, game):
        self.context_collides(game)

    def hited(self, ext_hits):
        if self.health - ext_hits > 0:
            self.health -= ext_hits
            return False
        else:
            return True

    def lambda_health_position(self):
        return [self.rect.x, self.rect.y - 10, self.health, 5]

    def lambda_max_health_position(self):
        return [self.rect.x, self.rect.y - 10, self.MAX_HEALTH, 5]

    def update_health(self, game):
        back_bar_color = (60, 63, 60)
        bar_color = (111, 210, 46)

        game.screen.blit(game.background, self.lambda_max_health_position(), self.lambda_max_health_position())
        game.screen.blit(game.background, self.lambda_health_position(), self.lambda_health_position())

        pygame.draw.rect(game.screen, back_bar_color, self.lambda_max_health_position())
        pygame.draw.rect(game.screen, bar_color, self.lambda_health_position())


class Alien(Enemy):
    HIT = 5
    XP = 20

    def __init__(self, game, add_speed=None):
        super().__init__('assets/enemies/alien.bmp', game, add_speed)

        self.health = self.MAX_HEALTH


class Alien1(Enemy):
    MAX_HEALTH = 30
    VELOCITY = 1.5
    HIT = 10
    XP = 50

    def __init__(self, game, add_speed=None):
        super().__init__('assets/enemies/alien1.bmp', game, add_speed)

        self.health = self.MAX_HEALTH


class Alien2(Enemy):
    MAX_HEALTH = 50
    VELOCITY = 1
    HIT = 15
    XP = 100

    def __init__(self, game, add_speed=None):
        super().__init__('assets/enemies/alien2.bmp', game, add_speed)

        self.health = self.MAX_HEALTH

        self.move_period = 60
        self.attack_period = 60
        self.move_cycle = 0
        self.attack_cycle = 0
        self.CORD = ['E', 'O']
        self.direction = 'E'
        self.is_block = 0

    def lambda_health_position(self):
        return [self.rect.x - 10, self.rect.y - 10, self.health, 5]

    def lambda_max_health_position(self):
        return [self.rect.x - 10, self.rect.y - 10, self.MAX_HEALTH, 5]

    def pattern(self, game):
        if self.rect.y >= 650:
            self.remove()
        else:
            self.rect.y += self.VELOCITY

            if GAME_VARIABLES.ENEMY_MOBILITY_ACTIVE:
                if self.move_cycle == self.move_period:
                    self.direction = random.choice(self.CORD)
                    self.move_cycle = 0
                else:
                    if self.direction == 'E':
                        if 100 <= self.rect.x < 600:
                            self.rect.x += self.VELOCITY
                        else:
                            self.rect.x -= self.VELOCITY
                            self.direction = random.choice(self.CORD)
                            self.move_cycle = 0

                    if self.direction == 'O':
                        if 100 <= self.rect.x - self.VELOCITY < 600:
                            self.rect.x -= self.VELOCITY
                        else:
                            self.rect.x += self.VELOCITY
                            self.direction = random.choice(self.CORD)
                            self.move_cycle = 0

                    self.move_cycle += 1

            if GAME_VARIABLES.ENEMY_ATTACK_ACTIVE:
                if self.attack_cycle == self.attack_period:
                    self.all_attacks.add(PowerEnemy(self))
                    self.attack_cycle = 0

                self.attack_cycle += 1


class Alien3(Enemy):
    MAX_HEALTH = 70
    VELOCITY = 1.5
    HIT = 30
    XP = 150

    def __init__(self, game, add_speed=None):
        super().__init__('assets/enemies/alien3.bmp', game, add_speed)

        self.health = self.MAX_HEALTH

        self.move_period = 60
        self.attack_period = 60
        self.move_cycle = 0
        self.attack_cycle = 0
        self.CORD = ['E', 'O']
        self.direction = 'E'
        self.is_block = 0

    def lambda_health_position(self):
        return [self.rect.x - 15, self.rect.y - 10, self.health, 5]

    def lambda_max_health_position(self):
        return [self.rect.x - 15, self.rect.y - 10, self.MAX_HEALTH, 5]

    def pattern(self, game):
        if self.rect.y >= 650:
            self.remove()
        else:
            self.rect.y += self.VELOCITY

            if GAME_VARIABLES.ENEMY_MOBILITY_ACTIVE:
                if self.move_cycle == self.move_period:
                    self.direction = random.choice(self.CORD)
                    self.move_cycle = 0
                else:
                    if self.direction == 'E':
                        if 100 <= self.rect.x < 600:
                            self.rect.x += self.VELOCITY
                        else:
                            self.rect.x -= self.VELOCITY
                            self.direction = random.choice(self.CORD)
                            self.move_cycle = 0

                    if self.direction == 'O':
                        if 100 <= self.rect.x - self.VELOCITY < 600:
                            self.rect.x -= self.VELOCITY
                        else:
                            self.rect.x += self.VELOCITY
                            self.direction = random.choice(self.CORD)
                            self.move_cycle = 0

                    self.move_cycle += 1

            if GAME_VARIABLES.ENEMY_ATTACK_ACTIVE:
                if self.attack_cycle == self.attack_period:
                    self.all_attacks.add(PowerEnemy1(self))
                    self.attack_cycle = 0

                self.attack_cycle += 1


class Boss1(Enemy):
    MAX_HEALTH = 120
    VELOCITY = 3
    HIT = 40
    XP = 1000

    def __init__(self, game, add_speed=None):
        super().__init__('assets/enemies/boss1.bmp', game, add_speed)

        self.health = self.MAX_HEALTH

        self.move_period = 40
        self.attack_1_period = 20
        self.attack_2_period = 60
        self.move_cycle = 0
        self.attack_cycle = 0
        self.CORD = ['N', 'S', 'E', 'O']
        self.direction = 'S'
        self.is_block = 0

    def lambda_health_position(self):
        return [self.rect.x - 50, self.rect.y - 15, self.health, 10]

    def lambda_max_health_position(self):
        return [self.rect.x - 50, self.rect.y - 15, self.MAX_HEALTH, 10]

    def pattern(self, game):
        if self.move_cycle == self.move_period:
            self.direction = random.choice(self.CORD)
            self.move_cycle = 0
        else:
            if self.direction == 'N':
                if 60 < self.rect.y < 400:
                    self.rect.y -= self.VELOCITY
                else:
                    self.rect.y += self.VELOCITY
                    self.direction = random.choice(self.CORD)
                    self.move_cycle = 0

            if self.direction == 'S':
                if 60 < self.rect.y < 400:
                    self.rect.y += self.VELOCITY
                else:
                    self.rect.y -= self.VELOCITY
                    self.direction = random.choice(self.CORD)
                    self.move_cycle = 0

            if self.direction == 'E':
                if 100 <= self.rect.x < 600:
                    self.rect.x += self.VELOCITY
                else:
                    self.rect.x -= self.VELOCITY
                    self.direction = random.choice(self.CORD)
                    self.move_cycle = 0

            if self.direction == 'O':
                if 100 <= self.rect.x - self.VELOCITY < 600:
                    self.rect.x -= self.VELOCITY
                else:
                    self.rect.x += self.VELOCITY
                    self.direction = random.choice(self.CORD)
                    self.move_cycle = 0

            self.move_cycle += 1

        # attack cycle
        if self.attack_cycle % self.attack_1_period == 0:
            self.all_attacks.add(PowerEnemy2(self))

        if self.attack_cycle == self.attack_2_period:
            self.all_attacks.add(PowerEnemy3(self))
            self.attack_cycle = 0

        self.attack_cycle += 1
