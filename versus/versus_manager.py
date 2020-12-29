"""Create the versus mananger"""
from config.sprites import ITEMS, SCOPE_HAND
from config.colors import ENERGOS, GLOOMY_PURPLE, RED_PIGMENT, BLUE_MARTINA
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
        self.spell_btn = pg.Rect((2 * TILESIZE, HEIGHT - TILESIZE), (TILESIZE, TILESIZE))
        self.validate_btn = pg.Rect((3 * TILESIZE, HEIGHT - TILESIZE), (TILESIZE, TILESIZE))
        self.action = None
        self.last_player_pos = None
        self.selected_enemy = None
        self.border_enemy = None

        self.circle = Circle(game, 0, 0, 0)

        self.warn = False
        self.active = False

    def check_for_versus(self):
        start = False
        for enemy in self.turn_manager.enemies:
            for player in self.turn_manager.players:
                if self.is_distance(enemy.pos, player.pos, 500):
                    start = True

        warning = False
        warn_list = list()
        for player in self.turn_manager.players:
            for enemy in self.turn_manager.enemies:
                if self.is_distance(player.pos, enemy.pos, 700):
                    warn_list.append(True)
                    warning = True
                    break
                else:
                    warn_list.append(False)
            if warning:
                break

        found = False
        for warn in warn_list:
            if warn:
                found = True

        if not found and self.warn:
            self.warn = False

        if warning and not self.warn:
            self.logs.add_log("You're near a battle")
            self.warn = True
        if start and not self.active:
            self.start_versus()
        elif not start and self.active:
            self.finish_versus()

    def is_distance(self, base_pos, target_pos, _range):
        dist = target_pos - base_pos
        return dist.length_squared() < _range * _range

    def start_versus(self):
        self.active = True
        self.set_move_player(False)
        self.logs.add_log("Start the versus")
        self.add_actions()

    def add_actions(self):
        if self.turn_manager.active_character().type == "Boss":
            self.turn_manager.active_character().number_actions = 1
            self.logs.add_log("Add 1 action")
        else:
            self.turn_manager.active_character().number_actions = 2
            self.logs.add_log("Add 2 actions")

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
                    if self.turn_manager.get_active_weapon_type() in ["hand", "sword"]:
                        self.circle.set_width(self.turn_manager.get_active_scope())
                        self.circle.set_pos(self.turn_manager.active_character().pos)
                    self.set_move_player(False)
                if self.move_btn.collidepoint(pos[0], pos[1]):
                    self.action = 'move'
                    self.logs.add_log("Move your hero")
                    self.last_player_pos = vec(self.turn_manager.active_character().pos)
                    self.circle.set_width(800)
                    self.circle.set_pos(self.turn_manager.active_character().pos)
                    self.set_move_player(True)
                if self.spell_btn.collidepoint(pos[0], pos[1]):
                    logger.debug('spell')
            if self.action == 'attack':
                if self.validate_btn.collidepoint(pos[0], pos[1]):
                    if not self.selected_enemy:
                        self.logs.add_log("Select an enemy")
                        return

                    logger.debug(
                        "il faut utiliser STR pour le type sword alors que on va utiliser DEX pour le type arc, pour le type arc, on peut tirer n'importe où mais plus c'est loin, plus on réduit le DEX")
                    self.remove_action()
                    if self.check_dice():
                        self.logs.add_log("Enemy attacked")
                        damage = self.calc_damage()
                        self.turn_manager.remove_health(damage, self.selected_enemy)
                    else:
                        self.logs.add_log("Missed dice roll")
                    self.check_characters_actions()
            if self.action == 'move':
                if self.validate_btn.collidepoint(pos[0], pos[1]):
                    self.logs.add_log("Hero moved")
                    self.remove_action()
                    self.remove_last_player_pos()
                    self.check_characters_actions()

    def calc_damage(self):
        damage = 0
        if self.turn_manager.get_active_weapon_type() == "hand":
            damage = 10
        else:
            damage = 20
            logger.debug("il faut déterminer la quantité de dégats")
        return damage

    def check_dice(self):
        self.turn_manager.active_character().throw_dice('str')

        return self.turn_manager.active_character().dice["success"]

    def check_characters_actions(self):
        self.turn_manager.active_character().number_actions -= 1
        self.logs.add_log(f"Action remaining : {self.turn_manager.active_character().number_actions}")
        self.set_move_player(False)
        if self.turn_manager.active_character().number_actions == 0:
            self.add_turn()

    def select_enemy(self, pos):
        if self.action == "attack":
            if self.turn_manager.get_active_weapon_type() in ["hand", "sword"]:
                if self.is_in_range(
                        pos, self.turn_manager.get_active_scope() // 2):  # warning, c'est la moitier de la taille du cercle
                    for enemy in self.turn_manager.enemies:
                        _x = pos[0] - self.game.camera.camera.x
                        _y = pos[1] - self.game.camera.camera.y
                        if enemy.rect.collidepoint(_x, _y):
                            self.selected_enemy = enemy
                            self.logs.add_log("Enemy selected")
                            break
                else:
                    self.logs.add_log("Select an enemy in the range")
                    # ça pose des soucis de redondances de click
                    # self.check_characters_actions()
            elif self.turn_manager.get_active_weapon_type() in ["arc"]:
                for enemy in self.turn_manager.enemies:
                    _x = pos[0] - self.game.camera.camera.x
                    _y = pos[1] - self.game.camera.camera.y
                    if enemy.rect.collidepoint(_x, _y):
                        self.selected_enemy = enemy
                        self.logs.add_log("Enemy selected")
                        break

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
            weapon_item = self.turn_manager.get_active_weapon()
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
            surface.fill(GLOOMY_PURPLE)
            screen.blit(surface, self.spell_btn)
            # screen.blit(pg.transform.scale(spell_image, (TILESIZE, TILESIZE)), self.spell_btn)
            surface.fill(ENERGOS)
            screen.blit(surface, self.validate_btn)
            screen.blit(pg.transform.scale(ITEMS["validate"], (TILESIZE, TILESIZE)), self.validate_btn)

    def draw_range(self, screen):
        if self.action == "move" or (
                self.action ==
                "attack" and self.turn_manager.get_active_weapon_type() in ["hand", "sword"]):
            for animated in self.game.animated:
                if isinstance(animated, Circle):
                    screen.blit(animated.image, self.game.camera.apply(animated))

    def add_turn(self):
        self.selected_enemy = None
        self.border_enemy = None
        self.logs.add_log("Next turn")
        self.turn_manager.add_turn()
        # add actions to the next character
        self.set_move_player(False)
        self.add_actions()
