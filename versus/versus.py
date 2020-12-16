"""Create the versus mananger"""
from config.sprites import ITEMS
from config.colors import ENERGOS, RED_PIGMENT, BLUE_MARTINA
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
        self.move_btn = pg.Rect((TILESIZE, HEIGHT - TILESIZE), (TILESIZE, TILESIZE))
        self.validate_btn = pg.Rect((2 * TILESIZE, HEIGHT - TILESIZE), (TILESIZE, TILESIZE))
        self.action = None
        self.last_player_pos = None
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

    def remove_last_player_pos(self):
        self.last_player_pos = None

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
                if self.move_btn.collidepoint(pos[0], pos[1]):
                    self.action = 'move'
                    self.logs.add_log("Move your hero")
                    self.last_player_pos = vec(self.turn_manager.active_character().pos)
                    self.circle.set_width(800)
                    self.circle.set_pos(self.turn_manager.active_character().pos)
            if self.action == 'move':
                if self.validate_btn.collidepoint(pos[0], pos[1]):
                    self.remove_action()
                    self.remove_last_player_pos()
                    self.add_turn()

    def select_enemy(self, pos):
        if self.action == "attack":
            if self.is_in_range(pos, 200):  # warning, c'est la moitier de la taille du cercle
                for enemy in self.turn_manager.enemies:
                    if enemy.rect.collidepoint(pos[0], pos[1]):
                        self.selected_enemy = enemy  # on se branle de le stocker, faut jsute le tuer, et il fatu ajouter la barrre de vie mais on pourrait faire une touche valider et ça permettrait de surligner le personnage que l'on va attaquer
                        self.remove_action()
                        self.logs.add_log("Enemy selected")
                        enemy.health -= 30
                        self.add_turn()
                        # il faut lui enlever des points de vies et vois pour comment on le tue (faire comme dans kids can code)
                        break
            else:
                logger.info("Select inside the range")

    def update(self):
        if self.active:
            if self.action in ["attack", "move"]:
                self.circle.update()
            if self.action == "move":
                dist = self.last_player_pos - self.turn_manager.active_character().pos
                print(dist)
                if dist.length_squared() > 370 * 370:
                    self.turn_manager.active_character().pos -= self.turn_manager.active_character().vel * self.game.dt

    def draw(self, screen):
        self.draw_range(screen)
        self.draw_btns(screen)

    def draw_btns(self, screen):
        if self.active and self.turn_manager.is_active_player():
            weapon_item = self.turn_manager.active_character().weapon
            weapon_image = None
            if weapon_item:
                weapon_image = weapon_item.image
            else:
                weapon_image = ITEMS["punch"]

            surface = pg.Surface((TILESIZE, TILESIZE))
            surface.fill(RED_PIGMENT)
            screen.blit(surface, self.attack_btn)
            screen.blit(pg.transform.scale(weapon_image, (TILESIZE, TILESIZE)), self.attack_btn)
            surface.fill(BLUE_MARTINA)
            screen.blit(surface, self.move_btn)
            screen.blit(pg.transform.scale(ITEMS["move"], (TILESIZE, TILESIZE)), self.move_btn)
            surface.fill(ENERGOS)
            screen.blit(surface, self.validate_btn)
            screen.blit(pg.transform.scale(ITEMS["validate"], (TILESIZE, TILESIZE)), self.validate_btn)

    def draw_range(self, screen):
        if self.action in ['attack', "move"]:
            for animated in self.game.animated:
                screen.blit(animated.image, self.game.camera.apply(animated))

    def add_turn(self):
        self.logs.add_log("Next turn")
        self.turn_manager.add_turn()
