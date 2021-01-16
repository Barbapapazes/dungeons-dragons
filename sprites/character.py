"""Define a character"""
from random import randint, uniform
import pygame as pg
from utils.tilemap import collide_with_walls
from config.sprites import PLAYER_HIT_RECT, TYPES_HEROS
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
        self.spell = None
        self.shield = 0

        self.xp = 0
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
        self.skill_bonus = False
        if not hasattr(self, "goto"):
            self.images = images
            self.image = next(self.images[self.direction])
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.hit_rect = hit_rect
            self.hit_rect.center = self.rect.center

        self.frame_time = 210 / 1000
        self.frame_timer = 0

    def update(self):
        """Update the sprite"""
        self.update_image()

        self.pos += self.vel * self.game.dt
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.update_collisions()

    def save_equipments(self):
        """Save the equipments of the player

        Returns:
            dict
        """
        armor = {key: value.save() if value else None for key, value in self.armor.items()}
        return {
            "armor": armor,
            "weapon": self.weapon.save() if self.weapon else None,
            "spell": self.spell.save() if self.spell else None
        }

    def throw_inventory(self):
        """drop every item stored inside the enemy's inventory
        """
        for slot in self.inventory.slots:
            if slot.item:
                self.inventory.throw_item(slot.item)

    def update_image(self):
        """Update the image sprite"""
        self.frame_timer += self.game.dt
        if self.frame_timer >= self.frame_time:
            self.frame_timer -= self.frame_time
            self.image = next(self.images[self.direction])

    def update_collisions(self):
        """Manage the collisions"""
        self.hit_rect.centerx = self.pos.x
        if collide_with_walls(self, self.game.walls, 'x'):
            self.vel.x = -self.vel.x/2
        self.hit_rect.centery = self.pos.y
        if collide_with_walls(self, self.game.walls, 'y'):
            self.vel.y = -self.vel.y/2
        self.rect.center = self.hit_rect.center

    def __str__(self):
        return f"Sprite {self.type}"

    def addHp(self, hp_gain):
        """Add passed hp_gain to the player's health

        Args:
            hp_gain (int)
        """
        self.health += hp_gain
        if self.health > self.max_HP:
            self.health = self.max_HP
        self.game.logs.add_log(f'{self} has {self.health} remaining, (+{hp_gain})')

    def subHp(self, hp_lose):
        """Sub passed hp_lose to the player's health
        Args:
            hp_lose (int)
        """
        self.health -= hp_lose
        if self.health < 0:
            self.health = 0
        else:
            self.game.logs.add_log(f'{self} has {self.health} remaining, (-{hp_lose})')

    def equip_armor(self, item):
        """Equip a passed armor item in the right armor slot,
        if an item is already in the needed armor slot, it will be unequipped

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

    def get_protection(self):
        protection = self.characteristics['con'] // 5
        for bodypart in self.armor:
            if self.armor[bodypart] is not None:
                protection += self.armor[bodypart].shield // 5
        return protection

    def groupCount(self, grouplist, count=0):
        """computes the number of entities belonging to the same group that can see one another
        Args:
            grouplist (list): list containing the entities of "self's group"
            count (int, optional): counter
        Returns:
            int: number of entities that can see one another
        """
        # for i in grouplist:
        #     logger.info(i)
        # logger.info(count)
        for someone in grouplist:
            if someone == self:
                grouplist.remove(someone)
                count += 1
            if (someone.pos - self.pos).length() <= self.view_range:
                if hasattr(someone, "goto"):
                    someone.player_spotted = self.player_spotted
                return Character.groupCount(someone, grouplist, count)
        return count

    def level_up(self):
        logger.debug("%s, %s", self, self.xp)
        if self.xp >= 100 and self.type in TYPES_HEROS:
            self.xp = self.xp % 100
            for i in self.characteristics:
                self.characteristics[i] += 5
            self.game.logs.add_log(f"{self} leveled up !")
            self.game.notification_manager.active = True
            self.game.notification_manager.content["title"] = "Level up !"
            if self.type == "soldier":
                self.game.notification_manager.content["content"] = "Unlock a fight action !"
            elif self.type == "wizard":
                self.game.notification_manager.content["content"] = "Unlock two spell actions !"
            elif self.type == "thief":
                self.skill_bonus = True
                self.game.notification_manager.content["content"] = "Unlock a big punch next turn !"
            return True
        return False
