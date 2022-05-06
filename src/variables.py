
def context_collides(self, sprite):
    """variables de collisions"""
    collides_player = self.check_collides(sprite, self.all_player)
    collides_attacks = self.check_collides(sprite, self.player.all_attacks)
    collides_enemies = self.check_collides(sprite, self.enemies)
    collides_items = self.check_collides(sprite, self.items)


class GameVariables:

    BORDER_TOP = 50
    BORDER_BOT = 650

    LVL_GAP = 2000
    ADDITIONAL_LVL_GAP = 1000
    INIT_LVL_N1 = 1000

    PERIOD_1 = 2160
    PERIOD_2 = 6480
    PERIOD_3 = 19940

    PERIOD_POWER_Z = PERIOD_1
    PERIOD_POWER_E = PERIOD_1
    PERIOD_POWER_R = PERIOD_2

    STOP_PERIOD = 1000
    ENEMY_SPAWN_PERIOD = 150
    ENEMY_SPAWN_PERIOD1 = 200
    ENEMY_SPAWN_PERIOD2 = 400

    SPAWN_MINIMAL = 400
    SPAWN_MAXIMAL = 600

    ENEMY_SPEED = 0

    ENEMY_SPAWN_NUMBER = 3
    ENEMY_SPAWN_NUMBER_1 = 1

    SPAWN_CHANCE_MINIMAL = 1
    SPAWN_CHANCE_MAXIMAL = 10

    def __init__(self):
        self.lvl_evolve = 0
        self.enemy_zone_evolve = 0
        self.enemy_number_evolve = 0

    def evolve_lvl_gap(self):
        self.LVL_GAP += self.ADDITIONAL_LVL_GAP

    def evolve_enemy_speed(self, lvl):
        if lvl != self.lvl_evolve:
            self.ENEMY_SPEED += 1
            self.lvl_evolve = lvl

    def evolve_enemy_spawn_zone(self, lvl):
        if lvl != self.enemy_zone_evolve:
            self.SPAWN_MINIMAL -= 100
            self.SPAWN_MAXIMAL += 100
            self.enemy_zone_evolve = lvl

    def evolve_enemy_spawn_number(self, lvl):
        if lvl != self.enemy_number_evolve:
            self.ENEMY_SPAWN_NUMBER += 1
            self.ENEMY_SPAWN_NUMBER_1 += 1
            self.enemy_number_evolve = lvl


GAME_VARIABLES = GameVariables()
