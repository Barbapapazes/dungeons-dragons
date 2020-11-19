"""Define a player"""
import pygame as pg
from config.colors import YELLOW
from config.window import TILESIZE
from config.sprites import PLAYER_SPEED
from inventory.inventory import Inventory


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y

        #Stats
        self.HP = 100       #point de vie
        self.max_HP = 100
        self.shield = 0     #armure

        #Inventory
        self.armor = {'head': None, 'chest': None, 'legs': None, 'feet': None}
        self.weapon = None
        self.inventory = Inventory(self, 40, 5, 8)


    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_q]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_z]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def addHp(self, hp_gain):
        self.HP += hp_gain
        if self.HP > self.max_HP:
            self.HP = self.max_HP

    def addShield(self, shield_gain):
        self.shield += shield_gain

    def equip_armor(self, item):
        if self.armor[item.slot] != None:
            self.unequip_armor(item.slot)
        self.armor[item.slot] = item
        self.shield += item.shield

    def unequip_armor(self, slot):
        if self.armor[slot] != None:
            self.shield -= self.armor[slot].shield
            self.armor[slot] = None

    def equip_weapon(self, weapon):
        if self.weapon != None:
            self.unequip_weapon()
        self.weapon = weapon

    def unequip_weapon(self):
        if self.weapon != None:
            self.weapon = None

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y
