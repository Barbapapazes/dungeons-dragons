"""Define a player"""
import pygame as pg
from random import randint
from logger import logger
from config.colors import YELLOW
from config.window import TILESIZE
from config.sprites import ASSETS_SPRITES, PLAYER_SPEED, PLAYER_ROT_SPEED, PLAYER_MAX_HP, PLAYER_HIT_RECT, PLAYER_MAX_MP
from inventory.inventory import Inventory
from utils.tilemap import collide_with_walls
from os import path
from shop.shop import Shop
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    """Create a player"""

    def __init__(self, game, _type, x, y):
        self._layer = 1
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = _type
        self.run_right_images = ASSETS_SPRITES[self.type]["right"]
        self.run_left_images = ASSETS_SPRITES[self.type]["left"]
        self.run_front_images = ASSETS_SPRITES[self.type]["front"]
        self.run_back_images = ASSETS_SPRITES[self.type]["back"]

        self.image = self.run_front_images[1]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0

        self.is_moving = False
        self.frame_count = 0

        self.numberOfAction = 0

        # Stats
        self.HP = 100
        self.max_HP = PLAYER_MAX_HP
        self.shield = 0
        self.MP = 50  # mana
        self.max_MP = PLAYER_MAX_MP

        # Attribut
        self.STR = 70  # strenght
        self.DEX = 60  # dexterity
        self.CON = 40  # constitution
        self.INT = 10  # intelligence
        self.WIS = 10  # lucky
        self.CHA = 60  # charisme

        self.gold = 100

        # Inventory
        self.armor = {'head': None, 'chest': None, 'legs': None, 'feet': None}
        self.weapon = None
        self.sort = None
        self.inventory = Inventory(self, 5, 8)

        # shop, temporary here, to put in a seller
        self.shop = Shop()

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        self.is_moving = False
        keys = pg.key.get_pressed()
        if keys[self.game.game_data["shortcuts"]["player"]["left"]["keys"][2]]:
            self.is_moving = True
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[self.game.game_data["shortcuts"]["player"]["right"]["keys"][2]]:
            self.is_moving = True
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[self.game.game_data["shortcuts"]["player"]["up"]["keys"][2]]:
            self.is_moving = True
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[self.game.game_data["shortcuts"]["player"]["down"]["keys"][2]]:
            self.is_moving = True
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)

    def addMP(self, MP_gain):
        """Add passed HP_gain to the player's mana

        Args:
            HP_gain (int)
        """
        self.MP += MP_gain
        if self.MP > self.max_MP:
            self.MP = self.max_MP

    def subMP(self, MP_lose):
        """Sub passed MP_lose to the player's mana

        Args:
            MP_lose (int)
        """
        self.MP -= MP_lose
        if self.MP < 0:
            self.MP = 0

    def addHp(self, hp_gain):
        """Add passed hp_gain to the player's health

        Args:
            hp_gain (int)
        """
        self.HP += hp_gain
        if self.HP > self.max_HP:
            self.HP = self.max_HP

    def subHp(self, hp_lose):
        """Sub passed hp_lose to the player's health

        Args:
            hp_lose (int)
        """
        self.HP -= hp_lose
        if self.HP < 0:
            self.HP = 0

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

    def equip_sort(self, sort):
        """Put a passed sort in the sort slot

        Args:
            weapon (Weapon)
        """
        if self.sort is not None:
            self.unequip_sort()
        self.sort = sort

    def unequip_sort(self):
        """Set sort to None if it wasn't
        """
        if self.sort is not None:
            self.sort = None

    def update(self):
        self.get_keys()
        self.frame_count += 1
        if self.frame_count >= 27:
            self.frame_count = 0

        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360

        if self.is_moving:
            if 135 < self.rot <= 225:
                self.image = pg.transform.flip(pg.transform.rotate(
                    self.run_right_images[self.frame_count // 9], -self.rot), False, True)
            if 225 < self.rot <= 315:
                self.image = pg.transform.rotate(
                    self.run_front_images[self.frame_count // 9], self.rot - 270)
            if 315 < self.rot <= 360 or 0 <= self.rot < 45:
                self.image = pg.transform.flip(pg.transform.rotate(
                    self.run_left_images[self.frame_count // 9], -self.rot), True, False)
            if 45 < self.rot <= 135:
                self.image = pg.transform.rotate(
                    self.run_back_images[self.frame_count // 9], self.rot - 90)

        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def throwDice(self, Val, modificateur=0, valueOfDice=100):
        """Throw of dice like D&D

        Args:
            Val (int): [characteristic use for test like STR or INT]
            modificateur (int): [malus or bonus on your characteristic]. Defaults to 0.
            valueOfDice (int): [value of dice]. Defaults to 100.

        Returns:
            [Boolean]: [Your reussit of test]
        """
        score = randint(0, valueOfDice)
        logger.info("Your dice is %i / 100 and the succes is under %i", score, Val+modificateur)
        return score <= Val + modificateur
