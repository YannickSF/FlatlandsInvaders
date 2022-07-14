
from src.powers import *
from src.items import *
from src.variables import GAME_VARIABLES


class Player(pygame.sprite.Sprite):
    MAX_HEALTH = 100
    VELOCITY = 2

    def __init__(self, image):
        super().__init__()

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.all_attacks = pygame.sprite.Group()

        self.power_a_active = True
        self.power_a_charge = 'x'

        self.power_z_active = False
        self.power_z_charge = 0

        self.power_e_active = False
        self.power_e_charge = 0

        self.power_r_active = False
        self.power_r_charge = 0

        self.health = 20
        self.power_health_active = 0
        self.power_health_charge = 0

        self.boost_ms = 0
        self.boost_ms_active = False
        self.boost_ms_charge = 0
        self.boost_attack = 0
        self.boost_attack_charge = 0
        self.boost_attack_active = 0
        self.boost_attack_ms = 0
        self.boost_attack_ms_active = 0
        self.boost_attack_ms_charge = 0

    def velocity(self):
        return self.VELOCITY + self.boost_ms

    def lambda_health_position(self):
        return [540, 15, self.health, 20]

    def lambda_max_health_position(self):
        return [540, 15, self.MAX_HEALTH, 20]

    def update_health(self, game):
        back_bar_color = (60, 63, 60)
        bar_color = (111, 210, 46)

        game.screen.blit(game.background, self.lambda_max_health_position(), self.lambda_max_health_position())
        game.screen.blit(game.background, self.lambda_health_position(), self.lambda_health_position())

        pygame.draw.rect(game.screen, back_bar_color, self.lambda_max_health_position())
        pygame.draw.rect(game.screen, bar_color, self.lambda_health_position())

    def power_a(self):
        pass

    def power_z(self):
        pass

    def power_e(self):
        pass

    def power_r(self):
        pass

    def item_q(self):
        if self.power_health_charge > 0:
            if self.health + ItemLife.BOOST < GAME_VARIABLES.MAX_HEALTH:
                self.health += ItemLife.BOOST
                self.power_health_charge -= 1

    def item_s(self):
        if self.boost_ms_charge > 0:
            if self.VELOCITY + self.boost_ms + ItemLife.BOOST < GAME_VARIABLES.MAX_MS:
                self.boost_ms += ItemBoostMS.BOOST
                self.boost_ms_charge -= 1

    def item_d(self):
        if self.boost_attack_charge > 0:
            if self.boost_attack + ItemBoostAttack.BOOST < GAME_VARIABLES.MAX_ATTACK:
                self.boost_attack += ItemBoostAttack.BOOST
                self.boost_attack_charge -= 1

    def item_f(self):
        if self.boost_attack_ms_charge > 0:
            if self.boost_attack_ms + ItemBoostAttackMS.BOOST < GAME_VARIABLES.MAX_ATTACK_MS:
                self.boost_attack_ms += ItemBoostAttackMS.BOOST
                self.boost_attack_ms_charge -= 1


class Red(Player):
    NAME = 'Red'

    def __init__(self):
        super(Red, self).__init__('assets/players/red.bmp')
        self.rect.x = 500
        self.rect.y = 575

    def power_a(self):
        if self.power_a_active:
            self.all_attacks.add(PowerA(self))

    def power_z(self):
        if self.power_z_active:
            if self.power_z_charge > 0:
                self.all_attacks.add(PowerZ(self))
                self.power_z_charge -= 1

    def power_e(self):
        if self.power_e_active:
            if self.power_e_charge > 0:
                self.all_attacks.add(PowerE(self, 'N'))
                self.all_attacks.add(PowerE(self, 'E'))
                self.all_attacks.add(PowerE(self, 'O'))
                self.power_e_charge -= 1

    def power_r(self):
        if self.power_r_active:
            if self.power_r_charge > 0:
                self.all_attacks.add(PowerR(self))
                self.power_r_charge -= 1
