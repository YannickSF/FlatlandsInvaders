
import pygame.sprite


class Item(pygame.sprite.Sprite):
    NAME = ''
    VELOCITY = 3
    RATIO = 1
    BOOST = 0
    CHARGE = 1

    def __init__(self, image, game):
        super().__init__()

        self.game = game
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.origin_image = self.image

        self.charge = 1
        self.boost = 0

    def remove(self):
        self.game.items.remove(self)

    def pattern(self):
        if self.rect.y >= 650:
            self.remove()
        else:
            self.rect.y += self.VELOCITY

    def context_collides(self, game):
        collides_player = game.check_collides(self, game.all_player)

        if type(self) is ItemPowerZ or type(self) is ItemPowerE or type(self) is ItemPowerR:

            if collides_player:
                if type(self) is ItemPowerZ:
                    if not game.player.power_z_active:
                        game.player.power_z_active = True
                    game.player.power_z_charge += self.CHARGE

                if type(self) is ItemPowerE:
                    if not game.player.power_e_active:
                        game.player.power_e_active = True
                    game.player.power_e_charge += self.CHARGE

                if type(self) is ItemPowerR:
                    if not game.player.power_r_active:
                        game.player.power_r_active = True
                    game.player.power_r_charge += self.CHARGE

                self.remove()
            else:
                self.pattern()

        elif type(self) is ItemBoostAttack \
                or type(self) is ItemBoostAttackMS \
                or type(self) is ItemBoostMS \
                or type(self) is ItemLife:

            if collides_player:
                if type(self) is ItemBoostAttack:
                    if not game.player.boost_attack_active:
                        game.player.boost_attack_active = True
                    game.player.boost_attack_charge += self.CHARGE
                if type(self) is ItemBoostAttackMS:
                    if not game.player.boost_attack_ms_active:
                        game.player.boost_attack_ms_active = True
                    game.player.boost_attack_ms_charge += self.CHARGE
                if type(self) is ItemBoostMS:
                    if not game.player.boost_ms_active:
                        game.player.boost_ms_active = True
                    game.player.boost_ms_charge += self.CHARGE
                if type(self) is ItemLife:
                    if not game.player.power_health_active:
                        game.player.power_health_active = True
                    game.player.power_health_charge += self.CHARGE

                self.remove()
            else:
                self.pattern()

    def move(self, game):
        self.context_collides(game)


class ItemPowerZ(Item):
    NAME = 'ItemPowerZ'
    VELOCITY = 2
    RATIO = 60
    CHARGE = 70

    def __init__(self, game):
        super().__init__('assets/items/item_z.bmp', game)

        self.charge = 70


class ItemPowerE(Item):
    NAME = 'ItemPowerE'
    VELOCITY = 3
    RATIO = 30
    CHARGE = 35

    def __init__(self, game):
        super().__init__('assets/items/item_e.bmp', game)

        self.charge = 35


class ItemPowerR(Item):
    NAME = 'ItemPowerR'
    VELOCITY = 4
    RATIO = 10
    CHARGE = 50

    def __init__(self, game):
        super().__init__('assets/items/item_r.bmp', game)

        self.charge = 50


class ItemBoostAttack(Item):
    NAME = 'ItemBoostAttack'
    VELOCITY = 3
    RATIO = 10
    BOOST = 5

    def __init__(self, game):
        super().__init__('assets/items/item_boost_attack.bmp', game)

        self.boost = 5


class ItemBoostAttackMS(Item):
    NAME = 'ItemBoostAttackMS'
    VELOCITY = 3
    RATIO = 25
    BOOST = 3

    def __init__(self, game):
        super().__init__('assets/items/item_boost_attack_ms.bmp', game)

        self.boost = 3


class ItemBoostMS(Item):
    NAME = 'ItemBoostMS'
    VELOCITY = 3
    RATIO = 40
    BOOST = 2

    def __init__(self, game):
        super().__init__('assets/items/item_boost_ms.bmp', game)

        self.boost = 2


class ItemLife(Item):
    NAME = 'ItemLife'
    VELOCITY = 2
    RATIO = 25
    BOOST = 5

    def __init__(self, game):
        super().__init__('assets/items/item_life.bmp', game)

        self.boost = 5
