
def context_collides(self, sprite):
    """variables de collisions"""
    collides_player = self.check_collides(sprite, self.all_player)
    collides_attacks = self.check_collides(sprite, self.player.all_attacks)
    collides_enemies = self.check_collides(sprite, self.enemies)
    collides_items = self.check_collides(sprite, self.items)


BORDER_TOP = 50
BORDER_BOT = 650

INIT_LVL_N = 0
INIT_LVL_N1 = 1000

PERIOD_1 = 2160
PERIOD_2 = 6480
PERIOD_3 = 19940

PERIOD_ALIEN = 180
PERIOD_POWER_Z = PERIOD_1
PERIOD_POWER_E = PERIOD_1
PERIOD_POWER_R = PERIOD_2
