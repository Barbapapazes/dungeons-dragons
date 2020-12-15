"""Create the versus mananger"""
from config.sprites import ITEMS
from config.window import HEIGHT, TILESIZE
import pygame as pg
from logger import logger


class VersusManager:

    def __init__(self, game):
        self.game = game
        self.logs = self.game.logs
        self.turn_manager = self.game.turn_manager

        self.attack_btn = pg.Rect((0, HEIGHT - TILESIZE), (TILESIZE, TILESIZE))
        self.action = None

        self.active = False

    def start_versus(self):
        self.active = True
        self.logs.add_log("Start the versus")

    def finish_versus(self):
        self.active = False
        self.logs.add_log("Finish the versus")

    def remove_action(self):
        self.action = None

    def select_action(self, pos):
        if self.active and self.turn_manager.is_active_player():
            if not self.action:
                if self.attack_btn.collidepoint(pos[0], pos[1]):
                    self.action = 'attack'
                    self.logs.add_log("User will attack")

    def update(self):
        pass

    def draw(self, screen):
        if self.active and self.turn_manager.is_active_player():
            weapon_item = self.turn_manager.active_character().weapon
            weapon_image = None
            if weapon_item:
                weapon_image = weapon_item.image
            else:
                weapon_image = ITEMS["punch"]
            screen.blit(pg.transform.scale(weapon_image, (TILESIZE, TILESIZE)), self.attack_btn)
