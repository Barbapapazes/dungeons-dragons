"""Define a player"""
from sprites.character import Character
import pygame as pg
from random import randint, uniform
from logger import logger
from config.colors import YELLOW
from config.window import TILESIZE
from config.sprites import ASSETS_SPRITES, ITEMS, PLAYER_SPEED, PLAYER_ROT_SPEED, PLAYER_MAX_HP, PLAYER_HIT_RECT, PLAYER_MAX_MP
from inventory.inventory import Inventory
from utils.tilemap import collide_with_walls
from os import path
from store.shop import Shop
vec = pg.math.Vector2


class Player(Character):
    """Create a player"""

    def __init__(self, game, x, y, _type, characteristics, health, xp, gold, images):
        super(Player, self).__init__(game, x, y, _type, images, PLAYER_HIT_RECT)
        self.can_move = True

        self.characteristics = characteristics
        self.health = health
        self.xp = xp
        self.gold = gold

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

        # Inventory
        self.armor = {'head': None, 'chest': None, 'legs': None, 'feet': None}
        self.weapon = None
        self.spell = None
        self.inventory = Inventory(self, 5, 8)

    def save(self):
        """Used to save the player data

        Returns:
            dict
        """
        return {
            "class": self.type,
            "pos": {
                "x": self.pos.x,
                "y": self.pos.y
            },
            "characteristics": self.characteristics,
            "health": self.health,
            "xp": self.xp,
            "health": self.health,
            "gold": self.gold,
            "inventory": self.inventory.save(),
            "equipments": self.save_equipments()
        }

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

    def get_keys(self):
        """Used to check the keys"""
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        self.direction = "idle"
        if self.can_move:
            if keys[self.game.game_data["shortcuts"]["player"]["left"]["keys"][2]]:
                self.direction = "left"
                self.vel.x = -PLAYER_SPEED
            if keys[self.game.game_data["shortcuts"]["player"]["right"]["keys"][2]]:
                self.direction = "right"
                self.vel.x = PLAYER_SPEED
            if keys[self.game.game_data["shortcuts"]["player"]["up"]["keys"][2]]:
                self.direction = "up"
                self.vel.y = -PLAYER_SPEED
            if keys[self.game.game_data["shortcuts"]["player"]["down"]["keys"][2]]:
                self.direction = "down"
                self.vel.y = PLAYER_SPEED
            if self.vel.x != 0 and self.vel.y != 0:
                self.vel *= 0.7071
            if self.game.name == "online_game":
                if keys[pg.K_SPACE]:
                    self.shoot()

    def shoot(self):
        """Used to launch an arrow"""
        direction = {
            "idle": -90,
            "left": 180,
            "right": 0,
            "up": -90,
            "down": 90
        }
        logger.debug("on va utiliser la position de la sourie pour envoyer la flèche à partir de la position du joueur")
        mouse_pos = pg.mouse.get_pos()
        # dir = vec(1, 0).rotate(-direction[self.direction])
        dir = vec(mouse_pos[0] - self.pos[0] - self.game.camera.camera.x,
                  mouse_pos[1] - self.pos[1] - self.game.camera.camera.y)
        dir.scale_to_length(1.0)
        damage = 10
        data = " ".join(
            ["arrow", str(int(self.pos.x)),
             str(int(self.pos.y)),
             str(dir.x),
             str(dir.y),
             str(damage), str(self.game.current_id)])
        # logger.debug(data)
        logger.debug("si on est en mode server, on envoie, sinon non, on fait une flèche en local")
        self.game.server.send(data)
        # logger.debug(dir)
        # Arrow(self.game, self.pos, dir, 10)

    def update(self):
        """Used to update the player"""
        self.get_keys()
        super().update()

    def get_direction(self):
        """Used to create the direction of the sprite, when in auto-mode"""
        angle = self.vel.angle_to(vec(0, 1))
        if 180 - 45 <= angle < 180 + 45:
            self.direction = "up"
        if 90 - 45 <= angle < 90 + 45:
            self.direction = "right"
        if -90 - 45 <= angle < -90 + 45:
            self.direction = "left"
        if 0 - 45 <= angle < 0 + 45:
            self.direction = "down"

    def set_vel(self, vel):
        """Set the velocity of the player

        Args:
            vel ([type]): [description]
        """
        self.direction = "idle"
        if vel[0] != 0 or vel[1] != 0:
            self.vel = vec(vel)
            self.get_direction()
        self.update_image()

    def set_pos(self, pos):
        """Set the pos of the player

        Args:
            pos (tuple)
        """
        self.pos = pos
        self.rect.center = self.pos

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

    def addHp(self, hp_gain):
        """Add passed hp_gain to the player's health

        Args:
            hp_gain (int)
        """
        self.HP += hp_gain
        logger.debug(hp_gain)
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

    def addShield(self, shield_gain):
        """Add passed shield_gain to the player's shield

        Args:
            shield_gain (int)
        """
        self.shield += shield_gain

    def equip_spell(self, spell):
        """Put a passed spell in the spell slot

        Args:
            weapon (Weapon)
        """
        if self.spell is not None:
            self.unequip_spell()
        self.spell = spell

    def unequip_spell(self):
        """Set spell to None if it wasn't
        """
        if self.spell is not None:
            self.spell = None

        # self.frame_count += 1
        # if self.frame_count >= 27:
        #     self.frame_count = 0

        # self.rot = (self.rot + self.rot_speed * self.game.dt) % 360

        # if self.is_moving:
        #     if 135 < self.rot <= 225:
        #         self.image = pg.transform.flip(pg.transform.rotate(
        #             self.run_right_images[self.frame_count // 9], -self.rot), False, True)
        #     if 225 < self.rot <= 315:
        #         self.image = pg.transform.rotate(
        #             self.run_front_images[self.frame_count // 9], self.rot - 270)
        #     if 315 < self.rot <= 360 or 0 <= self.rot < 45:
        #         self.image = pg.transform.flip(pg.transform.rotate(
        #             self.run_left_images[self.frame_count // 9], -self.rot), True, False)
        #     if 45 < self.rot <= 135:
        #         self.image = pg.transform.rotate(
        #             self.run_back_images[self.frame_count // 9], self.rot - 90)


class Arrow(pg.sprite.Sprite):
    """Create an arrow"""

    def __init__(self, game, pos, dir, damage, id, player_id):
        self._layer = 20
        self.groups = game.all_sprites, game.arrows,
        super(Arrow, self).__init__(self.groups)
        self.game = game
        self.id = id
        self.player_id = player_id

        self.image = ITEMS["arrow_01e"]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * 300 * uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage
        self.is_deleted = False

    def update(self):
        """Update the arrow"""
        self.pos += self.vel * self.game.dt
        logger.debug("%s, %s, %s", self.pos, self.vel, self.game.dt)
        self.rect.center = self.pos
        # if pg.sprite.spritecollide(self, self.game.walls, False):
        #     self.kill()
        if pg.time.get_ticks() - self.spawn_time > 1000:
            if self.game.name == "online_game":
                data = " ".join(["arrow", "remove", str(self.id), str(self.player_id)])
                self.is_deleted = True
                logger.debug(
                    "on peut faire ça en dehors pour éviter d'avoir trop de choses dans la flèche, le is_deleted se suffit à lui même")
                self.game.server.send(data)
            else:
                self.kill()
