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
        self.border_enemy = None

        self.circle = Circle(game, 0, 0, 0)

        self.active = False

    def start_versus(self):
        self.active = True
        self.set_move_player(False)
        self.logs.add_log("Start the versus")

    def finish_versus(self):
        self.active = False
        self.set_move_player(True)
        self.remove_selected_enemy()
        self.remove_last_player_pos()
        self.remove_action()
        self.logs.add_log("Finish the versus")

    def remove_selected_enemy(self):
        self.selected_enemy = None
        self.border_enemy = None

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

    def set_move_player(self, _bool):
        self.turn_manager.active_character().can_move = _bool

    def select_action(self, pos):
        if self.active and self.turn_manager.is_active_player():
            if not self.action:
                if self.attack_btn.collidepoint(pos[0], pos[1]):
                    self.action = 'attack'
                    self.logs.add_log("Attack is selected")
                    self.logs.add_log("Select a enemy")
                    self.circle.set_width(400)
                    self.circle.set_pos(self.turn_manager.active_character().pos)
                    self.set_move_player(False)
                if self.move_btn.collidepoint(pos[0], pos[1]):
                    self.action = 'move'
                    self.logs.add_log("Move your hero")
                    self.last_player_pos = vec(self.turn_manager.active_character().pos)
                    self.circle.set_width(800)
                    self.circle.set_pos(self.turn_manager.active_character().pos)
                    self.set_move_player(True)
            if self.action == 'attack':
                if self.validate_btn.collidepoint(pos[0], pos[1]):
                    self.remove_action()
                    self.logs.add_log("Enemy attacked")
                    self.selected_enemy.health -= 30
                    self.add_turn()
            if self.action == 'move':
                if self.validate_btn.collidepoint(pos[0], pos[1]):
                    self.remove_action()
                    self.remove_last_player_pos()
                    self.add_turn()

    def select_enemy(self, pos):
        if self.action == "attack":
            if self.is_in_range(pos, 200):  # warning, c'est la moitier de la taille du cercle
                for enemy in self.turn_manager.enemies:
                    _x = pos[0] - self.game.camera.camera.x
                    _y = pos[1] - self.game.camera.camera.y
                    if enemy.rect.collidepoint(_x, _y):
                        self.selected_enemy = enemy
                        self.logs.add_log("Enemy selected")
                        break
            else:
                logger.info("Select inside the range")

    def update(self):
        if self.active:
            if self.action in ["attack", "move"]:
                self.circle.update()
            if self.action == "move":
                dist = self.last_player_pos - self.turn_manager.active_character().pos
                if dist.length_squared() > 370 * 370:
                    self.turn_manager.active_character().pos -= self.turn_manager.active_character().vel * self.game.dt

    def draw(self, screen):
        self.draw_range(screen)
        self.draw_btns(screen)
        self.draw_enemy_border(screen)

    def draw_enemy_border(self, screen):
        if self.selected_enemy:
            image = self.selected_enemy.image.copy()
            image = image.convert_alpha()
            self.create_border(image, RED_PIGMENT)
            image = pg.transform.scale(image, (image.get_width() + 6, image.get_height() + 6))
            rect = self.selected_enemy.rect.copy()
            rect.centerx -= 3
            rect.centery -= 3
            screen.blit(image, self.game.camera.apply_rect(rect))

    def create_border(self, surface, color):
        w, h = surface.get_size()
        r, g, b = color
        for x in range(w):
            for y in range(h):
                a = surface.get_at((x, y))[3]
                surface.set_at((x, y), pg.Color(r, g, b, a))

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
                if isinstance(animated, Circle):
                    screen.blit(animated.image, self.game.camera.apply(animated))

    def add_turn(self):
        self.selected_enemy = None
        self.border_enemy = None
        self.logs.add_log("Next turn")
        self.turn_manager.add_turn()
