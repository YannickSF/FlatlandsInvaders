
import pygame


class Power(pygame.sprite.Sprite):
    HIT = 0
    VELOCITY = 1

    def __init__(self, character):
        super().__init__()
        self.character = character

        self.image = None
        self.rect = None
        self.origin_image = None
        self.angle = 0

        self.charge = 0

    def remove(self):
        self.character.all_attacks.remove(self)

    def pattern(self):
        self.rect.y -= self.VELOCITY

    def context_collides(self, game):
        collides_enemies = game.check_collides(self, game.enemies)

        if type(self) is PowerA or type(self) is PowerZ or type(self) is PowerE or type(self) is PowerR:

            if self.rect.y > 650 or self.rect.y < 50:
                self.remove()
            else:
                if collides_enemies:
                    game.player.all_attacks.remove(self)
                    if collides_enemies[0].hited(self.HIT):
                        game.screen.blit(game.background, collides_enemies[0].rect, collides_enemies[0].rect)
                        game.screen.blit(game.background,
                                         collides_enemies[0].lambda_max_health_position(),
                                         collides_enemies[0].lambda_max_health_position()
                                         )

                        game.screen.blit(game.background,
                                         collides_enemies[0].lambda_health_position(),
                                         collides_enemies[0].lambda_health_position()
                                         )
                        game.enemies.remove(collides_enemies[0])
                        game.score += 1
                        game.xp += collides_enemies[0].XP
                        game.spawn_on_die(collides_enemies[0])

                    self.remove()
                else:
                    self.pattern()

    def move(self, game):
        self.context_collides(game)
        # self.angle += 7
        # self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        # self.rect = self.image.get_rect(center=self.rect.center)


class PowerA(Power):
    HIT = 5
    VELOCITY = 5

    def __init__(self, character):
        super().__init__(character)

        self.image = pygame.image.load('assets/items/power_a.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.character.rect.x + self.character.rect.width / 2 - 5
        self.rect.y = self.character.rect.y - self.character.rect.height
        self.origin_image = self.image

        self.VELOCITY += self.character.boost_attack_ms
        self.HIT += self.character.boost_attack


class PowerZ(Power):
    HIT = 10
    VELOCITY = 10

    def __init__(self, character):
        super().__init__(character)

        self.image = pygame.image.load('assets/items/power_z.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.character.rect.x + self.character.rect.width / 2 - 5
        self.rect.y = self.character.rect.y - self.character.rect.height
        self.origin_image = self.image

        self.VELOCITY += self.character.boost_attack_ms
        self.HIT += self.character.boost_attack

        self.charge = 70


class PowerE(Power):
    HIT = 12
    VELOCITY = 12

    def __init__(self, character, direction):
        super().__init__(character)
        self.image = pygame.image.load('assets/items/power_e.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.character.rect.x + self.character.rect.width / 2 - 5
        self.rect.y = self.character.rect.y - self.character.rect.height
        self.origin_image = self.image

        self.VELOCITY += self.character.boost_attack_ms
        self.HIT += self.character.boost_attack

        self.direction = direction
        self.charge = 40

    def pattern(self):
        if self.direction == 'N':
            self.rect.y -= self.VELOCITY

        elif self.direction == 'E':
            self.rect.y -= self.VELOCITY
            self.rect.x += 5

        elif self.direction == 'O':
            self.rect.y -= self.VELOCITY
            self.rect.x -= 5


class PowerR(Power):
    HIT = 20
    VELOCITY = 15

    def __init__(self, character):
        super().__init__(character)
        self.image = pygame.image.load('assets/items/power_r.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.character.rect.x - self.rect.width / 2 + 10
        self.rect.y = self.character.rect.y - self.character.rect.height
        self.origin_image = self.image

        self.VELOCITY += self.character.boost_attack_ms
        self.HIT += self.character.boost_attack

        self.charge = 50


class PowerEnemy(Power):
    HIT = 2
    VELOCITY = 3

    def __init__(self, character):
        super().__init__(character)
        self.image = pygame.image.load('assets/items/power_enemy.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.character.rect.x - self.rect.width / 2 + 10
        self.rect.y = self.character.rect.y
        self.origin_image = self.image

        self.charge = 50

        self.VELOCITY += character.add_speed

    def pattern(self):
        self.rect.y += self.VELOCITY

    def context_collides(self, game):
        collides_player = game.check_collides(self, game.all_player)

        if self.rect.y > 650 or self.rect.y < 50:
            self.remove()
        else:
            if collides_player:
                game.player.health -= self.HIT
                self.remove()

                if game.player.health <= 0:
                    game.game_over()
            else:
                self.pattern()


class PowerEnemy1(Power):
    HIT = 3
    VELOCITY = 3

    def __init__(self, character):
        super().__init__(character)
        self.image = pygame.image.load('assets/items/power_enemy_1.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.character.rect.x - self.rect.width / 2 + 10
        self.rect.y = self.character.rect.y
        self.origin_image = self.image

        self.charge = 50
        self.VELOCITY += character.add_speed

    def pattern(self):
        self.rect.y += self.VELOCITY

    def context_collides(self, game):
        collides_player = game.check_collides(self, game.all_player)

        if self.rect.y > 650 or self.rect.y < 50:
            self.remove()
        else:
            if collides_player:
                game.player.health -= self.HIT
                self.remove()

                if game.player.health <= 0:
                    game.game_over()
            else:
                self.pattern()


class PowerEnemy2(Power):
    HIT = 5
    VELOCITY = 4

    def __init__(self, character):
        super().__init__(character)
        self.image = pygame.image.load('assets/items/power_enemy_2.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.character.rect.x - self.rect.width / 2 + 10
        self.rect.y = self.character.rect.y
        self.origin_image = self.image

        self.charge = 50
        self.VELOCITY += character.add_speed

    def pattern(self):
        self.rect.y += self.VELOCITY

    def context_collides(self, game):
        collides_player = game.check_collides(self, game.all_player)

        if self.rect.y > 650 or self.rect.y < 50:
            self.remove()
        else:
            if collides_player:
                game.player.health -= self.HIT
                self.remove()

                if game.player.health <= 0:
                    game.game_over()
            else:
                self.pattern()


class PowerEnemy3(Power):
    HIT = 10
    VELOCITY = 4

    def __init__(self, character):
        super().__init__(character)
        self.image = pygame.image.load('assets/items/power_enemy_3.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.character.rect.x - self.rect.width / 2 + 10
        self.rect.y = self.character.rect.y
        self.origin_image = self.image

        self.charge = 50
        self.VELOCITY += character.add_speed

    def pattern(self):
        self.rect.y += self.VELOCITY

    def context_collides(self, game):
        collides_player = game.check_collides(self, game.all_player)

        if self.rect.y > 650 or self.rect.y < 50:
            self.remove()
        else:
            if collides_player:
                game.player.health -= self.HIT
                self.remove()

                if game.player.health <= 0:
                    game.game_over()
            else:
                self.pattern()
