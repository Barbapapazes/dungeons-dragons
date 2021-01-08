"""Define a player"""
from random import uniform

import pygame as pg
from config.screens import ONLINE_GAME
from config.sprites import (ITEMS, PLAYER_HIT_RECT,
                            PLAYER_MAX_HP, PLAYER_MAX_MP,
                            PLAYER_SPEED)
from logger import logger
from sprites.character import Character, players

vec = pg.math.Vector2


class Player(Character):
    """Create a player"""

    def __init__(self, game, x, y, _type, characteristics, health, xp, gold, images):
        self.groups = players
        pg.sprite.Sprite.__init__(self, self.groups)
        super(Player, self).__init__(game, x, y, _type, images, PLAYER_HIT_RECT)

        self.can_move = True

        self.characteristics = characteristics
        self.health = health
        self.xp = xp
        self.gold = gold
        self.spell = None

        self.last_shot = 0

        # Stats
        self.HP = 100
        self.max_HP = PLAYER_MAX_HP
        self.shield = 0
        self.MP = 50  # mana
        self.max_MP = PLAYER_MAX_MP
        self.view_range = 500

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
            if self.game.name == ONLINE_GAME:
                if keys[pg.K_SPACE]:
                    self.shoot()

    def shoot(self):
        """Used to launch an arrow"""
        now = pg.time.get_ticks()
        if now - self.last_shot > 100:
            self.last_shot = now
            mouse_pos = pg.mouse.get_pos()
            _dir = vec(mouse_pos[0] - self.pos[0] - self.game.camera.camera.x,
                       mouse_pos[1] - self.pos[1] - self.game.camera.camera.y)
            _dir.scale_to_length(1.0)
            spread = uniform(-15, 15)
            _dir = _dir.rotate(spread)
            _vel = _dir * 300 * uniform(0.8, 1.2)
            damage = 10
            data = " ".join(
                ["arrow", str(int(self.pos.x)),
                 str(int(self.pos.y)),
                 str(_dir.x),
                 str(_dir.y),
                 str(_vel.x),
                 str(_vel.y),
                 str(damage), str(self.game.current_id)])

            self.game.server.send(data)

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


class Arrow(pg.sprite.Sprite):
    """Create an arrow"""

    def __init__(self, game, pos, _dir, vel, damage, _id, player_id):
        self._layer = 20
        self.groups = game.all_sprites, game.arrows,
        super(Arrow, self).__init__(self.groups)
        self.game = game
        self.id = _id
        self.player_id = player_id

        self.image = pg.transform.rotate(ITEMS["arrow_01e"], _dir.angle_to(vec(-1, -1)))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = vel
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage
        self.is_deleted = False

    def update(self):
        """Update the arrow"""
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > 1000:
            if self.game.name == ONLINE_GAME:
                self.is_deleted = True
                # this can be done outside of this class and we can send data only for the owner
                data = " ".join(["arrow", "remove", str(self.id), str(self.player_id)])
                self.game.server.send(data)
            else:
                self.kill()
