
import pygame.sprite
from preferences import *

SPACE = 60
PAD = 20
PAD2 = PAD * 2


class Cases(pygame.sprite.Sprite):
    KEY = ''
    X = 0
    Y = 700

    def __init__(self, image, game):
        super().__init__()

        self.game = game
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.rect.x = self.X
        self.rect.y = self.Y


class CaseA(Cases):
    KEY = pygame.key.name(KEY_ATTACK_BASE).upper()
    X = PAD

    def __init__(self, game):
        super().__init__('assets/panels/case_a.bmp', game)


class CaseZ(Cases):
    KEY = pygame.key.name(KEY_ATTACK_Z).upper()
    X = SPACE + PAD

    def __init__(self, game):
        super().__init__('assets/panels/case_z.bmp', game)


class CaseE(Cases):
    KEY = pygame.key.name(KEY_ATTACK_E).upper()
    X = SPACE * 2 + PAD

    def __init__(self, game):
        super().__init__('assets/panels/case_e.bmp', game)


class CaseR(Cases):
    KEY = pygame.key.name(KEY_ATTACK_R).upper()
    X = SPACE * 3 + PAD

    def __init__(self, game):
        super().__init__('assets/panels/case_r.bmp', game)


class CaseQ(Cases):
    KEY = pygame.key.name(KEY_BOOST_HEALTH).upper()
    X = SPACE * 4 + PAD2

    def __init__(self, game):
        super().__init__('assets/panels/case_g.bmp', game)


class CaseS(Cases):
    KEY = pygame.key.name(KEY_BOOST_MS).upper()
    X = SPACE * 5 + PAD2

    def __init__(self, game):
        super().__init__('assets/panels/case_g.bmp', game)


class CaseD(Cases):
    KEY = pygame.key.name(KEY_BOOST_ATTACK).upper()
    X = SPACE * 6 + PAD2

    def __init__(self, game):
        super().__init__('assets/panels/case_g.bmp', game)


class CaseF(Cases):
    KEY = pygame.key.name(KEY_BOOST_ATTACK_MS).upper()
    X = SPACE * 7 + PAD2

    def __init__(self, game):
        super().__init__('assets/panels/case_g.bmp', game)
