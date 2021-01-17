"""Create the versus mananger"""
import pygame as pg
from config.colors import BLUE_MARTINA, ENERGOS, GLOOMY_PURPLE, RED_PIGMENT
from config.sprites import ITEMS, MALUS_ARC
from config.window import HEIGHT, TILESIZE
from logger import logger
from sprites.animated import Circle
from sprites.effects_zone import EffectsZone

vec = pg.Vector2


class VersusManager:
    """Create a versus"""

    def __init__(self, game):
        self.game = game
        self.logs = self.game.logs
        self.turn_manager = self.game.turn_manager

        self.attack_btn = pg.Rect((0, HEIGHT - TILESIZE), (TILESIZE, TILESIZE))
        self.move_btn = pg.Rect((TILESIZE, HEIGHT - TILESIZE), (TILESIZE, TILESIZE))
        self.spell_btn = pg.Rect((2 * TILESIZE, HEIGHT - TILESIZE), (TILESIZE, TILESIZE))
        self.validate_btn = pg.Rect((3 * TILESIZE, HEIGHT - TILESIZE), (TILESIZE, TILESIZE))

        self.new(game)

    def new(self, game):
        self.circle = Circle(game, 0, 0, 0)
        self.action = None
        self.last_player_pos = None
        self.selected_enemy = None
        self.border_enemy = None
        self.warn = False
        self.active = False
        self.soldier_bonus = False
        self.wizard_bonus = False

        self.spell_pos = None

    def check_for_versus(self):
        """Check if the is a versus and activate it"""
        start = False
        for enemy in self.turn_manager.enemies:
            for player in self.turn_manager.players:
                if self.is_distance(enemy.pos, player.pos, 500):
                    start = True

        if not start:
            warning = False
            warn_list = list()
            # used to be sure that every hero is at the right distance
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
                    break

            if not found and self.warn:
                self.warn = False

            if warning and not self.warn:
                self.logs.add_log("You're near a battle ! Be careful !")
                self.warn = True
        if start and not self.active:
            self.start_versus()
        elif not start and self.active:
            self.finish_versus()

    def is_distance(self, base_pos, target_pos, _range):
        """Check if the target pos is in the range

        Args:
            base_pos (tuple)
            target_pos (tuple)
            _range (int)

        Returns:
            bool
        """
        dist = target_pos - base_pos
        return dist.length_squared() < _range * _range

    def start_versus(self):
        """Start the versus"""
        self.active = True
        self.set_move_player(False)
        self.logs.add_log("Start the versus")
        self.turn_manager.turn = 0
        self.turn_manager.sorted = False
        self.game.game_data["music"]["song"]["start_combat"] = True
        self.add_actions()

    def add_actions(self):
        if self.turn_manager.active_character().type == "boss":
            self.turn_manager.active_character().number_actions = 1
            # self.logs.add_log("Add 1 action")
        else:
            self.turn_manager.active_character().number_actions = 2
            # self.logs.add_log("Add 2 actions")

    def finish_versus(self):
        """Finish the versus"""
        self.active = False
        self.free_all_players()
        self.turn_manager.playable = self.turn_manager.players.index(self.turn_manager.active())
        self.turn_manager.vision = self.turn_manager.playable
        self.remove_selected_enemy()
        self.remove_last_player_pos()
        self.remove_action()
        self.remove_zones_effects()
        self.logs.add_log("Finish the versus")
        self.game.game_data["music"]["song"]["end_combat"] = True

    def remove_zones_effects(self):
        """Remove all zones"""
        for zone in self.game.effects_zones:
            zone.kill()
        logger.info("Remove all effects zones")

    def remove_selected_enemy(self):
        """Remove the selected enemy"""
        self.selected_enemy = None
        self.border_enemy = None

    def remove_action(self):
        """Remove the current action"""
        self.action = None

    def remove_last_player_pos(self):
        """Remove the last player pos"""
        self.last_player_pos = None

    def is_in_range(self, pos, _range):
        """Check if the pos in in the range relatively of the active character

        Args:
            pos (tuple)
            _range (int)

        Returns:
            bool
        """
        updated_pos = vec(pos) - vec(self.game.camera.camera.x, self.game.camera.camera.y)
        dist = updated_pos - self.turn_manager.active_character().pos
        return dist.length_squared() < _range * _range

    def events(self, pos):
        """Manage the events to

        Args:
            pos (tuple)
        """
        self.select_action(pos)
        self.select_enemy(pos)

    def set_move_player(self, _bool):
        """Set if the player can move

        Args:
            _bool (bool)
        """
        self.turn_manager.active_character().can_move = _bool

    def free_all_players(self):
        """All payers can move"""
        for player in self.turn_manager.players:
            player.can_move = True

    def select_action(self, pos):
        """Select the action using buttons

        Args:
            pos (tuple): the pos of the mouse when clicked
        """
        if self.active and self.turn_manager.is_active_player():
            if not self.action:
                if self.attack_btn.collidepoint(
                    pos[0],
                    pos[1]) and not self.wizard_bonus or (
                    self.attack_btn.collidepoint(pos[0],
                                                 pos[1]) and self.soldier_bonus):
                    self.action_attack()
                elif self.attack_btn.collidepoint(pos[0], pos[1]) and self.wizard_bonus:
                    self.logs.add_log("This is a bonus, you have to use your spell !")

                if self.move_btn.collidepoint(pos[0], pos[1]) and not self.soldier_bonus and not self.wizard_bonus:
                    self.action_move()
                elif self.move_btn.collidepoint(pos[0], pos[1]):
                    if self.soldier_bonus:
                        self.logs.add_log("This is a bonus, you have to fight !")
                    elif self.wizard_bonus:
                        self.logs.add_log("This is a bonus, you have to use your spell !")

                if self.spell_btn.collidepoint(
                    pos[0],
                    pos[1]) and not self.soldier_bonus and not self.turn_manager.get_active_spell() is None or(
                    self.spell_btn.collidepoint(pos[0],
                                                pos[1]) and self.wizard_bonus):
                    self.action_spell()
                elif self.spell_btn.collidepoint(pos[0], pos[1]) and self.soldier_bonus:
                    self.logs.add_log("This is a bonus, you have to fight !")
            if self.validate_btn.collidepoint(pos[0], pos[1]):
                logger.debug("%s, %s", self.soldier_bonus, self.wizard_bonus)
                self.validate()

    def validate(self):
        """Used to validate an action"""
        if self.action == 'attack':
            if not self.selected_enemy:
                self.logs.add_log("Select an enemy")
                return

            self.remove_action()
            if self.check_dice():
                self.logs.add_log("Enemy attacked")
                damage = self.calc_damage()
                self.turn_manager.remove_health(damage, self.selected_enemy)
                if self.selected_enemy.health <= 0:
                    self.kill_enemy()
            else:
                self.logs.add_log("Missed dice roll")
            self.selected_enemy = None
            self.check_characters_actions()
        if self.action == 'move':
            self.logs.add_log("Hero moved")
            self.remove_action()
            self.remove_last_player_pos()
            self.check_characters_actions()
        if self.action == 'spell':
            if not self.spell_pos:
                self.logs.add_log("Select a zone")
                return

            EffectsZone(
                self.game, self.spell_pos[0],
                self.spell_pos[1],
                self.turn_manager.get_active_spell().type, self.turn_manager.get_active_spell().time_to_live, self.
                turn_manager.get_active_spell().number_dice, self.turn_manager.get_active_spell().dice_value)
            self.remove_action()
            self.check_characters_actions()

    def kill_enemy(self, enemy=None):
        """Kill an enemy"""
        enemy = self.selected_enemy if enemy is None else enemy
        rel_turn = self.turn_manager.get_relative_turn()
        if self.turn_manager.sorted.index(
                enemy) < self.turn_manager.sorted.index(
                self.turn_manager.active()):
            rel_turn -= 1
        self.turn_manager.enemies.remove(enemy)
        self.turn_manager.sorted.remove(enemy)
        enemy.throw_inventory()
        enemy.throw_equipments()
        enemy.kill()
        self.turn_manager.turn = len(self.turn_manager.sorted) + rel_turn

    def action_attack(self):
        """Used to start a action to attack"""
        self.action = 'attack'
        self.logs.add_log("Attack is selected")
        self.logs.add_log("Select a enemy")
        if self.turn_manager.get_active_weapon_type() in ["hand", "sword"]:
            self.circle.set_width(self.turn_manager.get_active_scope())
            self.circle.set_pos(self.turn_manager.active_character().pos)
        self.set_move_player(False)

    def action_move(self):
        """Used to start a action to move"""
        self.action = 'move'
        self.logs.add_log("Move your hero")
        self.last_player_pos = vec(self.turn_manager.active_character().pos)
        self.circle.set_width(800)
        self.circle.set_pos(self.turn_manager.active_character().pos)
        self.set_move_player(True)

    def action_spell(self):
        """Used to start a action to spell"""
        self.action = "spell"
        self.logs.add_log("Spell selected")
        self.logs.add_log("Select a zone")
        self.circle.set_width(self.turn_manager.get_active_spell().scope)
        self.circle.set_pos(self.turn_manager.active_character().pos)
        self.set_move_player(False)

    def calc_damage(self):
        """Calc the damage depending of the weapon and the protection of the selected enemy

        Returns:
            int: damage, can be under 0
        """
        damage = self.turn_manager.get_active_weapon_damage()
        if self.turn_manager.get_active_weapon_type() == "arc":
            dist = self.selected_enemy.pos - self.turn_manager.active().pos
            logger.debug("[sofiane] il faut ajuster la valuer de MALUS_ARC")
            scope = self.turn_manager.get_active_weapon().scope
            if dist.length_squared() > scope:
                malus = -((dist.length_squared() - scope) // TILESIZE) * MALUS_ARC
                damage -= malus
        protection = self.selected_enemy.get_protection()

        if self.turn_manager.active().type == "thief" and self.turn_manager.active().skill_bonus and self.turn_manager.turn < len(self.turn_manager.sorted):
            self.turn_manager.active().skill_bonus = False
            self.logs.add_log("Use huge attack from thief")
            damage *= 2.2

        self.logs.add_log(
            f'The {self.turn_manager.active()} attacked {self.selected_enemy}, dealing {max(0, damage - protection)} ({damage} - {protection}).')
        return max(0, damage - protection)

    def check_dice(self):
        """Check the str success

        Returns:
            bool
        """
        self.turn_manager.active_character().throw_dice('str')

        return self.turn_manager.active_character().dice["success"]

    def check_characters_actions(self):
        """Check the action of the active character"""
        self.turn_manager.active().number_actions -= 1
        self.set_move_player(False)

        if self.turn_manager.is_active_player() and self.turn_manager.active().level_up() and self.turn_manager.active().number_actions == 0:
            if not self.turn_manager.active().type == "thief":
                self.turn_manager.active().number_actions += 1
                if self.turn_manager.active().type == "soldier":
                    self.soldier_bonus = True
                elif self.turn_manager.active().type == "wizard":
                    self.turn_manager.active().number_actions += 1
                    self.wizard_bonus = True

        if self.turn_manager.active().number_actions <= 0:
            self.add_turn()
        else:
            self.logs.add_log(
                f"Action remaining to {self.turn_manager.active()} : {self.turn_manager.active().number_actions}")

    def select_enemy(self, pos):
        """Select an enemy

        Args:
            pos (tuple)
        """
        if self.action == "attack":
            if self.turn_manager.get_active_weapon_type() in ["hand", "sword"]:
                if self.is_in_range(
                        pos, self.turn_manager.get_active_scope() // 2):  # warning, c'est la moitier de la taille du cercle
                    for enemy in self.turn_manager.enemies:
                        _x = pos[0] - self.game.camera.camera.x
                        _y = pos[1] - self.game.camera.camera.y
                        if enemy.rect.collidepoint(_x, _y):
                            self.selected_enemy = enemy
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
                        break

    def update(self):
        """Manage the update"""
        if self.active:
            if self.action in ["attack", "move", "spell"]:
                self.circle.update()
            if self.action == "move":
                dist = self.last_player_pos - self.turn_manager.active_character().pos
                if dist.length_squared() > 370 * 370:
                    self.turn_manager.active_character().pos -= self.turn_manager.active_character().vel * self.game.dt
            if self.action == "spell":
                mouse_click = pg.mouse.get_pressed()
                pos = pg.mouse.get_pos()
                if mouse_click[0] and self.is_in_range(pos, self.turn_manager.get_active_spell().scope // 2):
                    self.spell_pos = pos
                elif mouse_click[2]:
                    self.spell_pos = None

        self.check_for_versus()

    def draw(self, screen):
        """Draw the versus"""
        # self.draw_range(screen)
        self.draw_btns(screen)
        if self.action == "spell":
            if self.spell_pos:
                pg.draw.circle(screen, GLOOMY_PURPLE, self.spell_pos, TILESIZE, width=2)
            pos = pg.mouse.get_pos()
            if self.is_in_range(pos, self.turn_manager.get_active_spell().scope // 2):
                pg.draw.circle(screen, GLOOMY_PURPLE, pos, TILESIZE, width=2)
        self.draw_enemy_border(screen)

    def draw_enemy_border(self, screen):
        """Draw the enemy border

        Args:
            screen (Surface)
        """
        if self.selected_enemy:
            image = self.selected_enemy.image.copy()
            image = image.convert_alpha()
            self.create_border(image, RED_PIGMENT)
            image = pg.transform.scale(image, (image.get_width() + 6, image.get_height() + 6))
            rect = self.selected_enemy.rect.copy()
            rect.centerx -= 3
            rect.centery -= 3
            screen.blit(image, self.game.camera.apply_rect(rect))
            screen.blit(self.selected_enemy.image, self.game.camera.apply_rect(rect))

    def create_border(self, surface, color):
        """Create the enemy border

        Args:
            surface (Surface)
            color (tuple): the color of the border
        """
        w, h = surface.get_size()
        r, g, b = color
        for x in range(w):
            for y in range(h):
                a = surface.get_at((x, y))[3]
                surface.set_at((x, y), pg.Color(r, g, b, a))

    def draw_btns(self, screen):
        """Draw the buttons

        Args:
            screen (Surface)
        """
        if self.active and self.turn_manager.is_active_player():
            weapon_item = self.turn_manager.get_active_weapon()
            weapon_image = None
            if weapon_item:
                weapon_image = weapon_item.image
            else:
                weapon_image = ITEMS["punch"]

            spell_item = self.turn_manager.get_active_spell()
            spell_image = None
            if spell_item:
                spell_image = spell_item.image

            surface = pg.Surface((TILESIZE, TILESIZE))
            surface.fill(RED_PIGMENT)
            screen.blit(surface, self.attack_btn)
            screen.blit(pg.transform.scale(weapon_image, (TILESIZE, TILESIZE)), self.attack_btn)
            surface.fill(BLUE_MARTINA)
            screen.blit(surface, self.move_btn)
            screen.blit(pg.transform.scale(ITEMS["move"], (TILESIZE, TILESIZE)), self.move_btn)
            if self.turn_manager.active_character().type == "wizard":
                surface.fill(GLOOMY_PURPLE)
                screen.blit(surface, self.spell_btn)
                if spell_image:
                    screen.blit(pg.transform.scale(spell_image, (TILESIZE, TILESIZE)), self.spell_btn)
            surface.fill(ENERGOS)
            screen.blit(surface, self.validate_btn)
            screen.blit(pg.transform.scale(ITEMS["validate"], (TILESIZE, TILESIZE)), self.validate_btn)

    def draw_range(self, screen):
        """Draw the range

        Args:
            screen (Surface)
        """
        if self.action in["move", "spell"] or (
                self.action ==
                "attack" and self.turn_manager.get_active_weapon_type() in ["hand", "sword"]):
            for animated in self.game.animated:
                if isinstance(animated, Circle):
                    screen.blit(animated.image, self.game.camera.apply(animated))

    def add_turn(self):
        """Add a turn"""
        self.selected_enemy = None
        self.border_enemy = None
        self.logs.add_log("Next turn")
        self.turn_manager.add_turn()
        if self.turn_manager.is_active_player():
            self.turn_manager.add_vision()
        self.set_move_player(False)
        self.add_actions()
        self.check_effects_zones_hits()
        self.check_for_effects_zones()
        self.logs.add_log(self.turn_manager.active())

    def check_for_effects_zones(self):
        """Check if the effets zone can live"""
        for zone in self.game.effects_zones:
            zone.check_time_to_live()

    def check_effects_zones_hits(self):
        """Check for hit between characters and effects zone"""
        hits = pg.sprite.spritecollide(self.turn_manager.active_character(), self.game.effects_zones, False)
        for hit in hits:
            value = hit.get_dice_value()
            if hit.type == "heal":
                self.turn_manager.active_character().addHp(value)
            elif hit.type == "attack":
                self.turn_manager.active_character().subHp(value)
            self.logs.add_log(f"{self.turn_manager.active_character()} touch a {hit.type} zone ({value} points)")
