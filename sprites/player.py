"""Define a player"""
import pygame as pg
from config.colors import YELLOW
from config.window import TILESIZE
from config.sprites import PLAYER_SPEED, PLAYER_MAX_HP
from inventory.inventory import Inventory
from shop.shop import Shop


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

        # Stats
        self.HP = 100
        self.max_HP = PLAYER_MAX_HP
        self.shield = 0

        # Inventory
        self.armor = {'head': None, 'chest': None, 'legs': None, 'feet': None}
        self.weapon = None
        self.inventory = Inventory(self, 5, 8)

        #shop, temporary here, to put in a seller
        self.shop = Shop()

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
        """Add passed hp_gain to the player's health

        Args:
            hp_gain (int)
        """
        self.HP += hp_gain
        if self.HP > self.max_HP:
            self.HP = self.max_HP

    def addShield(self, shield_gain):
        """Add passed shield_gain to the player's shield

        Args:
            shield_gain (int)
        """
        self.shield += shield_gain

    def equip_armor(self, item):
        """Equip a passed armor item in the right armor slot,
        if an item is already in the needed armor slot, it will be unequiped

        Args:
            item (Armor)
        """
        if self.armor[item.slot] is not None:
            self.unequip_armor(item.slot)
        self.armor[item.slot] = item
        self.shield += item.shield

    def unequip_armor(self, slot):
        """Unequip an armor item from a passed slot

        Args:
            slot (Armor)
        """
        if self.armor[slot] is not None:
            self.shield -= self.armor[slot].shield
            self.armor[slot] = None

    def equip_weapon(self, weapon):
        """Put a passed weapon in the weapon slot

        Args:
            weapon (Weapon)
        """
        if self.weapon is not None:
            self.unequip_weapon()
        self.weapon = weapon

    def unequip_weapon(self):
        """Set weapon to None if it wasn't
        """
        if self.weapon is not None:
            self.weapon = None

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y
