"""Define a character"""
from random import randint, uniform
import pygame as pg
from utils.tilemap import collide_with_walls
from config.sprites import PLAYER_HIT_RECT
from logger import logger
from inventory.inventory import Inventory

vec = pg.math.Vector2

players = pg.sprite.Group()
enemies = pg.sprite.Group()


class Character(pg.sprite.Sprite):
    """Used to define a character"""

    def __init__(self, game, x, y, _type, images, hit_rect):
        self._layer = y
        self.groups = game.all_sprites
        super(Character, self).__init__(self.groups)

        self.characteristics = {
            "str": 0,
            "dex": 0,
            "con": 0,
            "int": 0,
            "wis": 0,
            "cha": 0
        }
        # Inventory
        self.inventory = Inventory(self, 5, 8)
        self.armor = {'head': None, 'chest': None, 'legs': None, 'feet': None}
        self.weapon = None

        self.game = game
        self.type = _type
        self.direction = "idle"

        self.dice = {
            "success": False,
            "result": 0
        }

        self.x = x
        self.y = y

        self.vel = vec(0, 0)
        self.pos = vec(x, y)

        self.number_actions = 0
        if not hasattr(self, "goto"):
            logger.debug(
                "c'est pour le player, donc on peut la mettre dans le player, ne pas donner d'images au character et passer la class avec un _")
            self.images = images
            self.image = next(self.images[self.direction])
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.hit_rect = hit_rect
            self.hit_rect.center = self.rect.center

        self.frame_time = 60 / 1000
        self.frame_timer = 0

    def update(self):
        """Update the sprite"""
        self.update_image()

        self.pos += self.vel * self.game.dt
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.update_collisions()

    def update_image(self):
        """Update the image sprite"""
        self.frame_timer += self.game.dt
        if self.frame_timer >= self.frame_time:
            self.frame_timer -= self.frame_time
            self.image = next(self.images[self.direction])

    def update_collisions(self):
        """Manage the collisions"""
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def __str__(self):
        return f"Sprite {self.type}"

    def throw_dice(self, base_value, mod=0, value_dice=100):
        """Throw a dice

        Args:
            base_value (str)
            mod (int, optional) Defaults to 0.
            value_dice (int, optional) Defaults to 100.

        Returns:
            bool: success if the result of the dice is under le base value plus the mod
        """
        result_dice = randint(0, value_dice)
        self.dice["result"] = result_dice
        self.dice["success"] = result_dice <= self.characteristics[base_value] + mod
        _type = "success" if self.dice["success"] else "failed"
        self.game.logs.add_log(
            f"Dice {_type}, result {result_dice}/{value_dice}, under {self.characteristics[base_value] + mod} to success")
        logger.info("Result dice : %d / %d (must be under %s to success)",
                    result_dice, value_dice, self.characteristics[base_value] + mod)

    def get_protection(self):
        protection = 1
        for bodypart in self.armor:
            if self.armor[bodypart] is not None:
                protection += self.armor[bodypart]
        return protection

    def groupCount(self, grouplist, count=0):
        """computes the number of entities belonging to the same group that can see one another
        Args:
            grouplist (list): list containing the entities of "self's group"
            count (int, optional): counter
        Returns:
            int: number of entities that can see one another
        """
        for someone in grouplist:
            if someone == self:
                grouplist.remove(someone)
                count += 1
            if (someone.pos - self.pos).length_squared() <= self.view_range:
                if hasattr(someone, "goto"):
                    someone.player_spotted = self.player_spotted
                return Character.groupCount(someone, grouplist, count)
        return count
