import pygame as pg
import misc, weapons
from pygame.locals import *
from variables import *

class Player(pg.sprite.Sprite):
    """ Player sprite object with various attributes

    Variables: (in addition to pygame's Sprite stuff)
        hp, hp_max, speed, lvl, xp: Self-explanatory
        xp_to_next_level: XP points needed for next level. XP resets on leveling.
        invulnerable: Ticks of invulnerability (i-frames)
        pickup_distance: Distance from which XP and pickups are picked up
        weapons = List of instances of weapons.Weapon

    Methods:
        update(): Pygame's Sprite-update. Decreases i-frames, also checks for movement input for now.
        get_hp(), get_hp_max(), get_xp(), get_xp_to_next_level(): Getters for variables
        damage(amount = 1): Decreases player's HP by [amount] and sets i-frames.
        levelup(): Trigger leveling up; increases [xp_to_next_level] and resets [xp].
            (levelup() is, at least for now, called by Xp.pickup() and not Player)
    """
    def __init__(self, game, hp = 20):
        super().__init__()
        self.game = game
        try:
            self.surf = pg.image.load("./image_generator/sprite.png").convert()
        except:
            try:
                self.surf = pg.image.load("./images/player.png").convert()
            except FileNotFoundError:
                self.surf = pg.Surface([30, 40])
                self.surf.fill((255,255,255))
        self.surf.set_colorkey((0,255,0))
        if not (SPRITE_SCALE == 1 or SPRITE_SCALE == 0):
            self.surf = pg.transform.scale_by(self.surf, SPRITE_SCALE)
        self.rect = self.surf.get_rect()
        self.hp = hp
        self.hp_max = hp
        self.speed = DEFAULT_SPEED
        self.lvl = 1
        self.xp = 0
        self.xp_to_next_level = 100
        self.invulnerable = 0
        self.pickup_distance = DEFAULT_PICKUP_DISTANCE * SPRITE_SCALE
        self.mouse_movement_enabled = False
        self.bullet_damage = 1

        # Create a List of weapons.Weapon instances (with some starting weapons at least for now)
        self.weapons = [weapons.Weapon(game, weapons.Bullet_Line),
                        weapons.Weapon(game, weapons.Orbiters, 500)]

    def update(self):
        """ Decrease i-frames, fire weapons, check for movement input. """
        if self.invulnerable > 0:
            self.invulnerable -= 1
        for weapon in self.weapons:
            weapon.fire()
        # Keyboard input for player movement with arrows & WASD
        if not self.mouse_movement_enabled:
            keys = pg.key.get_pressed()
            if keys[K_UP] or keys[K_w]:
                self.move_player(0, -self.speed)
                while pg.sprite.spritecollideany(self, collideable):
                    self.move_player(0, 1)
            if keys[K_RIGHT] or keys[K_d]:
                self.move_player(self.speed, 0)
                while pg.sprite.spritecollideany(self, collideable):
                    self.move_player(-1, 0)
            if keys[K_DOWN] or keys[K_s]:
                self.move_player(0, self.speed)
                while pg.sprite.spritecollideany(self, collideable):
                    self.move_player(0, -1)
            if keys[K_LEFT] or keys[K_a]:
                self.move_player(-self.speed, 0)
                while pg.sprite.spritecollideany(self, collideable):
                    self.move_player(1, 0)

        # Mouse movement testing
        else:
            MIN_MOUSE_DISTANCE = 30
            mouse_x, mouse_y = pg.mouse.get_pos()
            distance_fromplayer = misc.get_distance((mouse_x, mouse_y), self.rect.center)
            speed_multiplier = min(1, (distance_fromplayer - MIN_MOUSE_DISTANCE)/WIDTH*3.5)

            if distance_fromplayer > MIN_MOUSE_DISTANCE:
                if 3*abs(mouse_x - self.rect.center[0])/WIDTH > abs(mouse_y - self.rect.center[1])/HEIGHT:
                    if mouse_x > self.rect.center[0]:
                        self.move_player(self.speed * speed_multiplier, 0)
                        while pg.sprite.spritecollideany(self, collideable):
                            self.move_player(-1, 0)
                    else:
                        self.move_player(-self.speed * speed_multiplier, 0)
                        while pg.sprite.spritecollideany(self, collideable):
                            self.move_player(1, 0)
                if abs(mouse_x - self.rect.center[0])/WIDTH < 2*abs(mouse_y - self.rect.center[1])/HEIGHT:
                    if mouse_y > self.rect.center[1]:
                        self.move_player(0, self.speed * speed_multiplier)
                        while pg.sprite.spritecollideany(self, collideable):
                            self.move_player(0, -1)
                    else:
                        self.move_player(0, -self.speed * speed_multiplier)
                        while pg.sprite.spritecollideany(self, collideable):
                            self.move_player(0, 1)

    def get_hp(self):
        return self.hp

    def get_hp_max(self):
        return self.hp_max

    def get_xp(self):
        return self.xp

    def get_xp_to_next_level(self):
        return self.xp_to_next_level

    def damage(self, amount = 1):
        """ Decrease HP and set i-frames. """
        if not self.invulnerable:
            self.hp -= amount
            self.invulnerable = 10

            if self.hp <= 0:
                self.player_death()

    def levelup(self):
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level *= 1.5
        self.lvl += 1

    def player_death(self):
        """ Very much temporary, just playing around for now """
        self.surf = pg.transform.rotate(self.surf, 90)
        for sprite in bullet_group:
            sprite.kill()
        self.update = lambda *_: None

    def move_player(self, x, y):
        """ Move every non-player (and non-ui) sprite (-x,-y) pixels """
        for sprite in all_sprites:
            sprite.rect.move_ip(-x,-y)