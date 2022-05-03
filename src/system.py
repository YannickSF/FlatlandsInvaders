
from pygame.locals import *
from src.variables import *
from src.characters import Red
from src.powers import *
from src.enemies import *
from src.items import *
from src.panels import *


class Game:
    def __init__(self, screen):
        self.screen = screen if screen is not None else 'Error'
        self.is_playing = False
        self.play_button = pygame.image.load('assets/play.bmp')
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.x = 330
        self.play_button_rect.y = 350

        self.pause_button = pygame.image.load('assets/pause.bmp')
        self.pause_button_rect = self.pause_button.get_rect()
        self.pause_button_rect.x = 400
        self.pause_button_rect.y = 350

        self._open_window = True
        self._pause = False
        self._game_over = False

        # Fill background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = pygame.image.load('assets/background.bmp').convert()

        self.pressed = {}
        self.fetch_stats = False

        self.player = None
        self.all_player = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

        self.current_lvl = 0
        self.lvl_N = INIT_LVL_N
        self.lvl_N1 = INIT_LVL_N1
        self.score = 0
        self.xp = 0

        self.cycle_alien = 0
        self.cycle_power_z = 0
        self.cycle_power_e = 0
        self.cycle_power_r = 0

        # panels
        self.ca = CaseA(self)
        self.cz = CaseZ(self)
        self.ce = CaseE(self)
        self.cr = CaseR(self)
        self.cq = CaseQ(self)
        self.cs = CaseS(self)
        self.cd = CaseD(self)
        self.cf = CaseF(self)

    def exit(self, event):
        if event.type == QUIT:
            self._open_window = False

    def display_case(self, key, charge, active, sprite):
        self.screen.blit(self.background, sprite.rect, sprite.rect)
        if active:
            self.screen.blit(sprite.image, sprite.rect)

            fetch_line = pygame.font.SysFont("monospace", 15)
            fetch_text = fetch_line.render(
                "{0}".format('{0}|{1:02d}'.format(key, charge) if type(charge) == int else '{0}|{1}'.format(key, charge)),
                1, (255, 255, 255))

            fetch_pos = fetch_text.get_rect()
            fetch_pos.x = sprite.X + 5
            fetch_pos.y = sprite.Y + 17
            self.screen.blit(self.background, fetch_pos, fetch_pos)
            self.screen.blit(fetch_text, fetch_pos)

    def display_panels_top(self):
        # fetch stats TOP
        fetch_line1 = pygame.font.SysFont("monospace", 25)
        fetch_text1 = fetch_line1.render(
            "|Score:{0:05d} |XP:{1:07d}   |{2}"
                .format(self.score,
                        self.xp,
                        self.player.NAME,
                        ),
            1, (255, 255, 255))

        fetch_pos1 = fetch_text1.get_rect()
        fetch_pos1.x = 10
        fetch_pos1.y = 12
        self.screen.blit(self.background, fetch_pos1, fetch_pos1)
        self.screen.blit(fetch_text1, fetch_pos1)
        pygame.time.delay(2)

    def display_panels_bottom(self):
        # A
        self.display_case(self.ca.KEY, self.player.power_a_charge, self.player.power_a_active, self.ca)
        # Z
        self.display_case(self.cz.KEY, self.player.power_z_charge, self.player.power_z_active, self.cz)
        # E
        self.display_case(self.ce.KEY, self.player.power_e_charge, self.player.power_e_active, self.ce)
        # Q
        self.display_case(self.cr.KEY, self.player.power_r_charge, self.player.power_r_active, self.cr)
        # S
        self.display_case(self.cq.KEY, self.player.power_health_charge, self.player.power_health_active, self.cq)
        # D
        self.display_case(self.cs.KEY, self.player.boost_ms_charge, self.player.boost_ms_active, self.cs)
        # R
        self.display_case(self.cd.KEY, self.player.boost_attack_charge, self.player.boost_attack_active, self.cd)
        # F
        self.display_case(self.cf.KEY, self.player.boost_attack_ms_charge, self.player.boost_attack_ms_active, self.cf)

    def display_stats(self, fetch):
        # fetch stats TOP
        fetch_line1 = pygame.font.SysFont("monospace", 16)
        #
        fetch_text1 = fetch_line1.render(
            "|{0}[{1}] |H[{2:02d}/{3}] |Ms[{4}] |N:{5} |N1:{6}"
                .format(self.player.NAME,
                        self.current_lvl,
                        self.player.health,
                        self.player.MAX_HEALTH,
                        self.player.VELOCITY + self.player.boost_ms,
                        self.lvl_N, self.lvl_N1
                        ),
            1, (255, 255, 255))

        fetch_pos1 = fetch_text1.get_rect()
        fetch_pos1.x = 15
        fetch_pos1.y = 800

        # Fetch stats BOT
        fetch_line2 = pygame.font.SysFont("monospace", 16)
        fetch_text2 = fetch_line2.render(
            "|{0} |{1} |{2} |{3}"
                .format('{0}[{1:03d}/{2:03d}:{3}]'.format(pygame.key.name(KEY_ATTACK_BASE).upper(),
                                                          PowerA.HIT + self.player.boost_attack,
                                                          PowerA.VELOCITY + self.player.boost_attack_ms,
                                                          self.player.power_a_charge)
                        if self.player.power_a_active else '',
                        '{0}[{1:03d}/{2:03d}:{3:03d}]'.format(pygame.key.name(KEY_ATTACK_BASE).upper(),
                                                              PowerZ.HIT + self.player.boost_attack,
                                                              PowerZ.VELOCITY + self.player.boost_attack_ms,
                                                              self.player.power_z_charge)
                        if self.player.power_z_active else '',
                        '{0}[{1:03d}/{2:03d}:{3:03d}]'.format(pygame.key.name(KEY_ATTACK_BASE).upper(),
                                                              PowerE.HIT + self.player.boost_attack,
                                                              PowerE.VELOCITY + self.player.boost_attack_ms,
                                                              self.player.power_e_charge)
                        if self.player.power_e_active else '',
                        '{0}[{1:03d}/{2:03d}:{3:03d}]'.format(pygame.key.name(KEY_ATTACK_BASE).upper(),
                                                              PowerR.HIT + self.player.boost_attack,
                                                              PowerR.VELOCITY + self.player.boost_attack_ms,
                                                              self.player.power_r_charge)
                        if self.player.power_r_active else ''
                        ),
            1, (255, 255, 255))

        fetch_pos2 = fetch_text2.get_rect()
        fetch_pos2.x = 15
        fetch_pos2.y = 820

        fetch_line3 = pygame.font.SysFont("monospace", 16)
        fetch_text3 = fetch_line3.render(
            "|Q[H]:{0:02d} |S[Ms]:{1:02d} |D[A*]:{2:02d} |F[AMs]:{3:02d}"
                .format(self.player.power_health_charge,
                        self.player.boost_ms_charge,
                        self.player.boost_attack_charge,
                        self.player.boost_attack_ms_charge,
                        ),
            1, (255, 255, 255))

        fetch_pos3 = fetch_text3.get_rect()
        fetch_pos3.x = 15
        fetch_pos3.y = 840

        if fetch:
            self.screen.blit(self.background, fetch_pos1, fetch_pos1)
            self.screen.blit(fetch_text1, fetch_pos1)
            self.screen.blit(self.background, fetch_pos2, fetch_pos2)
            self.screen.blit(fetch_text2, fetch_pos2)
            self.screen.blit(self.background, fetch_pos3, fetch_pos3)
            self.screen.blit(fetch_text3, fetch_pos3)
            pygame.time.delay(2)
        else:
            self.screen.blit(self.background, fetch_pos1, fetch_pos1)
            self.screen.blit(self.background, fetch_pos2, fetch_pos2)
            self.screen.blit(self.background, fetch_pos3, fetch_pos3)

    def movements_play(self):
        # Movements
        if self.pressed.get(KEY_UP) and self.player.rect.y > 40:
            self.player.rect = self.player.rect.move(0, -(self.player.VELOCITY + self.player.boost_ms))  # move players
        if self.pressed.get(KEY_DOWN) and \
                self.player.rect.y + self.player.rect.height + self.player.VELOCITY < 680:
            self.player.rect = self.player.rect.move(0, self.player.VELOCITY + self.player.boost_ms)  # move players
        if self.pressed.get(KEY_RIGHT) and \
                self.player.rect.x + self.player.rect.width < self.screen.get_width():
            self.player.rect = self.player.rect.move(self.player.VELOCITY + self.player.boost_ms, 0)  # move players
        if self.pressed.get(KEY_LEFT) and self.player.rect.x > 0:
            self.player.rect = self.player.rect.move(-(self.player.VELOCITY + self.player.boost_ms), 0)  # move players

        # Attack
        if self.pressed.get(pygame.K_r):
            self.player.power_r()

    def skills_play(self, key):
        # Attacks
        if key == KEY_ATTACK_BASE:
            self.player.power_a()
        if key == KEY_ATTACK_Z:
            self.player.power_z()
        if key == KEY_ATTACK_E:
            self.player.power_e()

        # Boost
        if key == KEY_BOOST_HEALTH:
            self.player.item_q()
        if key == KEY_BOOST_MS:
            self.player.item_s()
        if key == KEY_BOOST_ATTACK:
            self.player.item_d()
        if key == KEY_BOOST_ATTACK_MS:
            self.player.item_f()

        # Parameters
        if key == KEY_STATS:
            self.fetch_stats = not self.fetch_stats

    @staticmethod
    def check_collides(sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    @staticmethod
    def spawn_chance(chance, max_chance):
        return True if random.randint(0, max_chance) < chance else False

    def game_over(self):
        self.is_playing = False
        self._game_over = True

    def _init_level(self):
        self.current_lvl = 0
        self.lvl_N = INIT_LVL_N
        self.lvl_N1 = INIT_LVL_N1

    def update_level(self):
        if self.lvl_N <= self.lvl_N1 < self.xp:
            self.current_lvl += 1
            tmp = self.lvl_N1
            self.lvl_N1 += self.lvl_N
            self.lvl_N = tmp

    def spawn_items(self, item_type, sprite=None):

        if item_type == ItemPowerZ.NAME or item_type == ItemPowerE.NAME or item_type == ItemPowerR.NAME:
            itm = None

            if item_type == ItemPowerZ.NAME and self.spawn_chance(1, 2):
                itm = ItemPowerZ(self)
            if item_type == ItemPowerE.NAME and self.spawn_chance(1, 3):
                itm = ItemPowerE(self)
            if item_type == ItemPowerR.NAME and self.spawn_chance(1, 5):
                itm = ItemPowerR(self)

            if itm is not None:
                itm.rect.y = 50
                itm.rect.x = random.randint(20, 980)
                self.items.add(itm)

        if item_type == ItemBoostAttack.NAME or \
                item_type == ItemBoostAttackMS.NAME or \
                item_type == ItemBoostMS.NAME or \
                item_type == ItemLife.NAME:
            itm = None

            if item_type == ItemBoostAttack.NAME:
                itm = ItemBoostAttack(self)
            if item_type == ItemBoostAttackMS.NAME:
                itm = ItemBoostAttackMS(self)
            if item_type == ItemBoostMS.NAME:
                itm = ItemBoostMS(self)
            if item_type == ItemLife.NAME:
                itm = ItemLife(self)

            if itm is not None:
                itm.rect.y = sprite.rect.y
                itm.rect.x = sprite.rect.x
                self.items.add(itm)

    def spawn_enemies(self):

        if self.cycle_alien == PERIOD_ALIEN:
            if self.current_lvl == 0:
                for i in range(random.randint(1, 3)):
                    aln = Alien(self)
                    aln.rect.y = 50
                    aln.rect.x = random.randint(20, 980)
                    self.enemies.add(aln)

                # Lvl Boss
            if self.current_lvl == 1:

                for i in range(random.randint(1, 4)):
                    aln = Alien(self)
                    aln.rect.y = 50
                    aln.rect.x = random.randint(20, 980)
                    self.enemies.add(aln)

            if self.current_lvl == 2:
                for i in range(random.randint(1, 5)):
                    aln = Alien(self)
                    aln.rect.y = 50
                    aln.rect.x = random.randint(20, 980)
                    self.enemies.add(aln)

                if self.spawn_chance(1, 3):
                    for i in range(random.randint(0, 2)):
                        aln1 = Alien1(self)
                        aln1.rect.y = 50
                        aln1.rect.x = random.randint(20, 980)
                        self.enemies.add(aln1)

            if self.current_lvl == 3:
                for i in range(random.randint(1, 5)):
                    aln = Alien(self)
                    aln.rect.y = 50
                    aln.rect.x = random.randint(20, 980)
                    self.enemies.add(aln)

                if self.spawn_chance(1, 3):
                    for i in range(random.randint(0, 4)):
                        aln1 = Alien1(self)
                        aln1.rect.y = 50
                        aln1.rect.x = random.randint(20, 980)
                        self.enemies.add(aln1)

            if self.current_lvl == 4:
                for i in range(random.randint(1, 5)):
                    aln = Alien(self)
                    aln.rect.y = 50
                    aln.rect.x = random.randint(20, 980)
                    self.enemies.add(aln)

                for i in range(random.randint(0, 3)):
                    aln1 = Alien1(self)
                    aln1.rect.y = 50
                    aln1.rect.x = random.randint(20, 980)
                    self.enemies.add(aln1)

                if self.spawn_chance(1, 4):
                    for i in range(random.randint(0, 1)):
                        aln2 = Alien2(self)
                        aln2.rect.y = 50
                        aln2.rect.x = random.randint(20, 980)
                        self.enemies.add(aln2)

            if self.current_lvl == 5:
                for i in range(random.randint(1, 5)):
                    aln = Alien(self)
                    aln.rect.y = 50
                    aln.rect.x = random.randint(20, 980)
                    self.enemies.add(aln)

                for i in range(random.randint(0, 3)):
                    aln1 = Alien1(self)
                    aln1.rect.y = 50
                    aln1.rect.x = random.randint(20, 980)
                    self.enemies.add(aln1)

                if self.spawn_chance(1, 4):
                    for i in range(random.randint(0, 3)):
                        aln2 = Alien2(self)
                        aln2.rect.y = 50
                        aln2.rect.x = random.randint(20, 980)
                        self.enemies.add(aln2)

            if self.current_lvl == 6:

                for i in range(random.randint(1, 5)):
                    aln = Alien(self)
                    aln.rect.y = 50
                    aln.rect.x = random.randint(20, 980)
                    self.enemies.add(aln)

                for i in range(random.randint(0, 5)):
                    aln1 = Alien1(self)
                    aln1.rect.y = 50
                    aln1.rect.x = random.randint(20, 980)
                    self.enemies.add(aln1)

                if self.spawn_chance(1, 4):
                    for i in range(random.randint(0, 3)):
                        aln2 = Alien2(self)
                        aln2.rect.y = 50
                        aln2.rect.x = random.randint(20, 980)
                        self.enemies.add(aln2)

            if self.current_lvl == 7:
                for i in range(random.randint(1, 5)):
                    aln = Alien(self)
                    aln.rect.y = 50
                    aln.rect.x = random.randint(20, 980)
                    self.enemies.add(aln)

                for i in range(random.randint(1, 5)):
                    aln1 = Alien1(self)
                    aln1.rect.y = 50
                    aln1.rect.x = random.randint(20, 980)
                    self.enemies.add(aln1)

                for i in range(random.randint(0, 2)):
                    aln2 = Alien2(self)
                    aln2.rect.y = 50
                    aln2.rect.x = random.randint(20, 980)
                    self.enemies.add(aln2)

            if self.current_lvl == 8:
                for i in range(random.randint(1, 5)):
                    aln = Alien(self)
                    aln.rect.y = 50
                    aln.rect.x = random.randint(20, 980)
                    self.enemies.add(aln)

                for i in range(random.randint(1, 5)):
                    aln1 = Alien1(self)
                    aln1.rect.y = 50
                    aln1.rect.x = random.randint(20, 980)
                    self.enemies.add(aln1)

                for i in range(random.randint(0, 4)):
                    aln2 = Alien2(self)
                    aln2.rect.y = 50
                    aln2.rect.x = random.randint(20, 980)
                    self.enemies.add(aln2)

                if self.spawn_chance(1, 4):
                    for i in range(random.randint(0, 1)):
                        aln3 = Alien3(self)
                        aln3.rect.y = 50
                        aln3.rect.x = random.randint(20, 980)
                        self.enemies.add(aln3)

            if self.current_lvl == 9:
                for i in range(random.randint(1, 5)):
                    aln = Alien(self)
                    aln.rect.y = 50
                    aln.rect.x = random.randint(20, 980)
                    self.enemies.add(aln)

                for i in range(random.randint(1, 5)):
                    aln1 = Alien1(self)
                    aln1.rect.y = 50
                    aln1.rect.x = random.randint(20, 980)
                    self.enemies.add(aln1)

                for i in range(random.randint(1, 4)):
                    aln2 = Alien2(self)
                    aln2.rect.y = 50
                    aln2.rect.x = random.randint(20, 980)
                    self.enemies.add(aln2)

                for i in range(random.randint(0, 3)):
                    aln3 = Alien3(self)
                    aln3.rect.y = 50
                    aln3.rect.x = random.randint(20, 980)
                    self.enemies.add(aln3)

            if self.current_lvl == 10:
                exist = False
                for e in self.enemies:
                    if type(e) == Boss1:
                        exist = True
                if not exist:
                    boss = Boss1(self)
                    boss.rect.y = 70
                    boss.rect.x = 460
                    self.enemies.add(boss)

            # manage period here
            return True

        return False

    def spawn_on_die(self, sprite=None):
        items = []

        if self.spawn_chance(1, 5):
            items += [ItemBoostMS.NAME for i in range(ItemBoostMS.RATIO)]
            items += [ItemBoostAttack.NAME for i in range(ItemBoostAttackMS.RATIO)]
            items += [ItemBoostAttackMS.NAME for i in range(ItemBoostAttack.RATIO)]
            items += [ItemLife.NAME for i in range(ItemLife.RATIO)]

            return self.spawn_items(random.choice(items), sprite)

    def spawn_player(self, color=Red.NAME):

        if color == Red.NAME:
            self.player = Red()
            self.all_player.add(self.player)
            self.screen.blit(self.player.image, self.player.rect)

    def start(self):
        if self._game_over:
            self.clean_display()
            self._game_over = False

        self.pressed = {}
        self.fetch_stats = False

        self.player = None
        self.all_player = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

        self.current_lvl = 0
        self.lvl_N = INIT_LVL_N
        self.lvl_N1 = INIT_LVL_N1
        self.score = 0
        self.xp = 0

        self.cycle_alien = 0
        self.cycle_power_z = 0
        self.cycle_power_e = 0
        self.cycle_power_r = 0

        # panels
        self.ca = CaseA(self)
        self.cz = CaseZ(self)
        self.ce = CaseE(self)
        self.cr = CaseR(self)
        self.cq = CaseQ(self)
        self.cs = CaseS(self)
        self.cd = CaseD(self)
        self.cf = CaseF(self)

        self.spawn_player()
        self.display_panels_bottom()

    def clean_display(self):
        # manage players
        self.screen.blit(self.background, self.player.rect, self.player.rect)  # erase players
        # manage attacks
        for att in self.player.all_attacks:
            self.screen.blit(self.background, att.rect, att.rect)  # erase Power
        for enemy in self.enemies:
            self.screen.blit(self.background,
                             enemy.lambda_max_health_position(), enemy.lambda_max_health_position())
            self.screen.blit(self.background,
                             enemy.lambda_health_position(),
                             enemy.lambda_health_position())  # erase healthBar
            self.screen.blit(self.background, enemy.rect, enemy.rect)  # erase Alien
        for nmy in self.enemies:
            for att in nmy.all_attacks:
                self.screen.blit(self.background, att.rect, att.rect)  # erase Power
        for itm in self.items:
            self.screen.blit(self.background, itm.rect, itm.rect)  # erase Power

    def update_display(self):
        for event in pygame.event.get():
            self.exit(event)

            if event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._pause = True
                else:
                    self.pressed[event.key] = True
                    self.skills_play(event.key)

            if event.type == KEYUP:
                if not event.key == pygame.K_SPACE:
                    self.pressed[event.key] = False
        pygame.time.delay(2)

        self.movements_play()
        self.player.update_health(self)
        self.screen.blit(self.player.image, self.player.rect)  # draw players
        pygame.time.delay(2)

        # manage player attacks
        for att in self.player.all_attacks:
            att.move(self)
        self.player.all_attacks.draw(self.screen)
        pygame.time.delay(2)

        # manage enemies
        self.cycle_alien += 1
        if self.spawn_enemies():
            self.cycle_alien = 0

        for enemy in self.enemies:
            enemy.move(self)

        for enemy in self.enemies:
            enemy.update_health(self)
        self.enemies.draw(self.screen)
        pygame.time.delay(2)

        # manage enemies attacks

        for nmy in self.enemies:
            for att in nmy.all_attacks:
                att.move(self)
            nmy.all_attacks.draw(self.screen)
        pygame.time.delay(2)

        # manage items
        self.cycle_power_z += 1
        self.cycle_power_e += 1
        self.cycle_power_r += 1
        if self.cycle_power_z == PERIOD_POWER_Z:
            self.spawn_items(ItemPowerZ.NAME)
            self.cycle_power_z = 0

        if self.cycle_power_e == PERIOD_POWER_E:
            self.spawn_items(ItemPowerE.NAME)
            self.cycle_power_e = 0

        if self.cycle_power_r == PERIOD_POWER_R:
            self.spawn_items(ItemPowerR.NAME)
            self.cycle_power_r = 0

        for itm in self.items:
            itm.move(self)
        self.items.draw(self.screen)
        pygame.time.delay(2)

    def run(self):
        while self._open_window:
            pygame.display.update()

            # game started ?
            if not self.is_playing:
                self.screen.blit(self.play_button, self.play_button_rect)  # erase play button
                pygame.time.delay(10)

                # manage user input
                for event in pygame.event.get():
                    self.exit(event)

                    # start game
                    if (event.type == MOUSEBUTTONDOWN and self.play_button_rect.collidepoint(event.pos)) or\
                            (event.type == KEYDOWN and event.key == pygame.K_SPACE):
                        self.screen.blit(self.background,
                                         self.play_button_rect,
                                         self.play_button_rect)
                        self.start()
                        self.is_playing = True
                    pygame.time.delay(2)

            else:
                # pause ?
                if self._pause:
                    self.screen.blit(self.pause_button, self.pause_button_rect)  # erase pause_button

                    for event in pygame.event.get():
                        self.exit(event)

                        # pause
                        if event.type == KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                self.screen.blit(self.background, self.pause_button_rect,
                                                 self.pause_button_rect)  # erase players
                                self._pause = False
                else:

                    self.clean_display()
                    self.update_display()

                    # fetch stats & update lvl
                    self.update_level()
                    self.display_panels_top()
                    self.display_panels_bottom()

                    # Parameters
                    self.display_stats(self.fetch_stats)
