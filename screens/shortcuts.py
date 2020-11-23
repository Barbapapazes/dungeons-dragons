"""Shortcuts screen"""

import pygame as pg
import json
from os import path
from window import _State
from logger import logger
from config.window import WIDTH, HEIGHT
from config.colors import BLACK, WHITE, LIGHTER_PURPLE, BLUE_GREY, BLUE_HORIZON, GLOOMY_PURPLE, DARKGREY, LIGHTGREY, GREY
from config.screens import SHORTCUTS, TRANSITION_OUT
from data.shortcuts import SHORTCUTS_DEFAULT, CUSTOM_SHORTCUTS_FILENAME


# charger le bon fichier de shortcuts, comme avec la class window et pour pour ne pas le faire passer dans game data ? afin d'évite le rechargement


class Shortcuts(_State):
    """Shortcuts screen"""

    def __init__(self):
        self.name = SHORTCUTS
        super(Shortcuts, self).__init__(self.name)
        self.next = None

        self.key = None

        self.background = pg.Surface((WIDTH, HEIGHT))

        self.shortcuts = SHORTCUTS_DEFAULT
        self.selected_menu = 0
        self.selected_shortcut = 0
        self.is_menu_selected = False
        self.is_shortcut_selected = False
        self.key = 107
        self.ctrl = None
        self.alt = None
        self.saved = False
        self.alpha = 0
        logger.debug(self.shortcuts)

    def startup(self, dt, game_data):
        """Initialize data at scene start."""
        self.game_data = game_data
        self.dt = dt
        self.background.fill(GLOOMY_PURPLE)
        super().setup_transition()

    def run(self, surface, keys, mouse, dt):
        """Run states"""
        self.screen = surface
        self.keys = keys
        self.dt = dt
        update_level = self.states_dict[self.state]
        if self.state != 'normal':
            self.draw()
        update_level()

    def normal_run(self):
        """Run the normal state"""
        self.draw()

    def get_events(self, event):
        """Events loop"""
        if event.key is not pg.K_RETURN:
            mod = pg.key.get_mods()
            if mod & pg.KMOD_CTRL:
                self.ctrl = not self.ctrl
            elif mod & pg.KMOD_ALT:
                self.alt = not self.alt
            else:
                self.key = event.key

        if event.type == pg.KEYUP:
            if event.key == pg.K_PAGEUP:
                if not self.is_shortcut_selected:
                    if self.is_menu_selected:
                        self.selected_shortcut -= 1
                        if self.selected_shortcut < 0:
                            self.selected_shortcut = 0
                    else:
                        self.selected_menu -= 1
                        if self.selected_menu < 0:
                            self.selected_menu = 0
            elif event.key == pg.K_PAGEDOWN:
                if not self.is_shortcut_selected:
                    if self.is_menu_selected:
                        self.selected_shortcut += 1
                        if self.selected_shortcut > len(
                                self.shortcuts[self.menu_keys[self.selected_menu]].keys()) - 1:
                            self.selected_shortcut = len(
                                self.shortcuts[self.menu_keys[self.selected_menu]].keys()) - 1
                    else:
                        self.selected_menu += 1
                        if self.selected_menu > len(self.shortcuts.keys()) - 1:
                            self.selected_menu = len(self.shortcuts.keys()) - 1
            elif event.key == pg.K_s and pg.key.get_mods() & pg.KMOD_ALT:
                self.save_shortcuts()
                self.saved = True
            elif event.key == pg.K_RETURN:
                if self.is_shortcut_selected:
                    menu = self.menu_keys[self.selected_menu]
                    shortcut_keys = list(self.shortcuts[menu].keys())
                    shortcut = shortcut_keys[self.selected_shortcut]
                    self.shortcuts[menu][shortcut]["keys"] = self.create_shortcut()
                    logger.info(f"Save {self.create_shortcut()} to {shortcut} in {menu}")
                if self.is_menu_selected:
                    self.is_shortcut_selected = True
                else:
                    self.is_menu_selected = True
            elif event.key == pg.K_ESCAPE:
                if self.is_shortcut_selected:
                    self.is_shortcut_selected = False
                else:
                    self.is_menu_selected = False
            logger.debug(self.selected_menu)

    def save_shortcuts(self):
        """Save shortcuts to a custom file"""
        with open(path.join(self.saved_shortcuts, CUSTOM_SHORTCUTS_FILENAME), 'w') as _f:
            _f.write(json.dumps(self.shortcuts))
            logger.info('Save shortcuts to %s', path.join(self.saved_shortcuts, CUSTOM_SHORTCUTS_FILENAME))

    def create_shortcut(self):
        return [self.ctrl, self.alt, self.key]

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_text("shortcuts".upper(), self.title_font, 48, BLACK, WIDTH // 2, 0, align="n")

        self.menu_keys = list(self.shortcuts.keys())
        self.draw_table()
        self.draw_content()

        if self.is_shortcut_selected:
            self.draw_text(
                f"Shortcut à enregistrer : {self.create_text_shortcut(self.ctrl, self.alt, self.key)}", self.title_font,
                24, BLACK, WIDTH // 2, HEIGHT, align="s")

        self.draw_saved()

    def draw_table(self):
        """Draw the table of contents"""
        for index, key in enumerate(self.menu_keys):
            color = GREY
            if index == self.selected_menu:
                color = BLACK
            self.draw_text(key.upper(), self.title_font, 24, color, 12, 60 + 60 * index, align="nw")

    def draw_content(self):
        """Draw all content from the selected_menu value"""
        for index, (key, value) in enumerate(self.shortcuts[self.menu_keys[self.selected_menu]].items()):
            color = GREY
            if index == self.selected_shortcut and self.is_menu_selected:
                color = BLACK
            text = f"{key.upper()} : "
            help = ""
            for key_2, value_2 in value.items():
                if key_2 == 'keys':
                    text += self.create_text_shortcut(value_2[0], value_2[1], value_2[2])
                elif key_2 == 'help':
                    help = f"{value_2}"
            self.draw_text(text,
                           self.title_font, 16, color, WIDTH // 4, 60 + 60 * index, align="nw")
            self.draw_text(help,
                           self.title_font, 12, color, WIDTH // 4 + 12, 80 + 60 * index, align="nw")

    def draw_saved(self):
        """Draw the saved page"""
        if self.saved:
            self.alpha += 15
        if self.alpha >= 255:
            self.saved = False
        if self.alpha > 0 and not self.saved:
            self.alpha -= 15
        if self.saved or self.alpha > 0:
            transition = pg.Surface((WIDTH, HEIGHT))
            transition.fill(BLACK)
            transition.set_alpha(self.alpha)
            self.screen.blit(transition, (0, 0))
            self.draw_text("Saved", self.title_font, 50, WHITE,
                           WIDTH // 2, HEIGHT / 2, align="center")

    @staticmethod
    def create_text_shortcut(ctrl, alt, key):
        return f"{'ctrl + ' if ctrl else ''}{'alt + ' if alt else ''}{pg.key.name(key) if key else ''}"
