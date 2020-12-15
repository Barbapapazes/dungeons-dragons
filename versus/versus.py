"""Create the versus mananger"""
from config.sprites import ITEMS
from config.window import HEIGHT, TILESIZE
import pygame as pg
from logger import logger
from sprites.animated import Circle
vec = pg.Vector2


class VersusManager:

    def __init__(self, game):
        self.game = game
        self.logs = self.game.logs
        self.turn_manager = self.game.turn_manager

        self.attack_btn = pg.Rect((0, HEIGHT - TILESIZE), (TILESIZE, TILESIZE))
        self.action = None
        self.selected_enemy = None

        self.circle = Circle(game, 0, 0, 0)

        self.active = False

    def start_versus(self):
        self.active = True
        self.logs.add_log("Start the versus")

    def finish_versus(self):
        self.active = False
        self.remove_action()
        self.logs.add_log("Finish the versus")

    def remove_action(self):
        self.action = None

    def is_in_range(self, pos, _range):
        updated_pos = vec(pos) - vec(self.game.camera.camera.x, self.game.camera.camera.y)
        dist = updated_pos - self.turn_manager.active_character().pos
        return dist.length_squared() < _range * _range

    def events(self, pos):
        self.select_action(pos)
        self.select_enemy(pos)

    def select_action(self, pos):
        if self.active and self.turn_manager.is_active_player():
            if not self.action:
                if self.attack_btn.collidepoint(pos[0], pos[1]):
                    self.action = 'attack'
                    self.logs.add_log("Attack is selected")
                    self.logs.add_log("Select a enemy")
                    self.circle.set_width(400)
                    self.circle.set_pos(self.turn_manager.active_character().pos)

    def select_enemy(self, pos):
        if self.action == "attack":
            if self.is_in_range(pos, 200): 
                for enemy in self.turn_manager.enemies:
                    if enemy.rect.collidepoint(pos[0], pos[1]):
                        self.selected_enemy = enemy  # on se branle de le stocker, faut jsute le tuer, et il fatu ajouter la barrre de vie
                        self.remove_action()
                        self.logs.add_log("Enemy selected")
                        enemy.health -= 30
                        self.turn_manager.turn += 1
                        # il faut lui enlever des points de vies et vois pour comment on le tue (faire comme dans kids can code)
                        break
            else:
                logger.info("Select inside the range")

    def update(self):
        if self.active:
            if self.action == "attack":
                self.circle.update()

    def draw(self, screen):
        if self.active and self.turn_manager.is_active_player():
            weapon_item = self.turn_manager.active_character().weapon
            weapon_image = None
            if weapon_item:
                weapon_image = weapon_item.image
            else:
                weapon_image = ITEMS["punch"]
            screen.blit(pg.transform.scale(weapon_image, (TILESIZE, TILESIZE)), self.attack_btn)

            if self.action == 'attack':
                self.draw_range(screen)

    def draw_range(self, screen):
        for animated in self.game.animated:
            screen.blit(animated.image, self.game.camera.apply(animated))
