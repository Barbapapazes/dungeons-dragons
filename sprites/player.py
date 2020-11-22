"""Define a player"""
import pygame as pg
from random import randint
from logger import logger
from config.colors import YELLOW
from config.window import TILESIZE
from config.sprites import PLAYER_SPEED, PLAYER_ROT_SPEED, PLAYER_MAX_HP, PLAYER_HIT_RECT
from inventory.inventory import Inventory
from utils.tilemap import collide_with_walls
from shop.shop import Shop
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    """Create a player"""

    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0

        self.nbAct = 0

        # Stats
        self.HP = 100
        self.max_HP = PLAYER_MAX_HP
        self.shield = 0
        self.MA = 50

        # Attribut
        self.STR = 70  # strenght
        self.DEX = 60  # dexterity
        self.CON = 40  # constitution
        self.INT = 10  # intelligence
        self.WIS = 10  # lucky
        self.CHA = 60  # charisme

        # Inventory
        self.armor = {'head': None, 'chest': None, 'legs': None, 'feet': None}
        self.weapon = None
        self.inventory = Inventory(self, 5, 8)

        # shop, temporary here, to put in a seller
        self.shop = Shop()

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[self.game.game_data["shortcuts"]["player"]["left"]["keys"][2]]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[self.game.game_data["shortcuts"]["player"]["right"]["keys"][2]]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[self.game.game_data["shortcuts"]["player"]["up"]["keys"][2]]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[self.game.game_data["shortcuts"]["player"]["down"]["keys"][2]]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)

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
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(pg.Surface((TILESIZE, TILESIZE)), self.rot)
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def throwDice(self, Val, modificateur=0):
        score = randint(0, 100)
        logger.info("Your dice is %i / 100 and the succes is under %i", score, Val+modificateur)
        return score <= Val + modificateur
