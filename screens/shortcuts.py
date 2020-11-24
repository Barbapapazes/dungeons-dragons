"""Shortcuts screen"""

import pygame as pg
import json
from os import path
from window import _State
from logger import logger
from config.window import WIDTH, HEIGHT
from config.colors import BLACK, WHITE, GLOOMY_PURPLE, GREY
from config.screens import SHORTCUTS
from data.shortcuts import CUSTOM_SHORTCUTS_FILENAME


class Shortcuts(_State):
    """Shortcuts screen"""

    def __init__(self):
        self.name = SHORTCUTS
        super(Shortcuts, self).__init__(self.name)
        self.next = None

        self.key = None

        self.background = pg.Surface((WIDTH, HEIGHT))

        self.shortcuts = None
        self.selected_menu = 0
        self.selected_shortcut = 0
        self.is_menu_selected = False
        self.is_shortcut_selected = False
        self.key = 107
        self.ctrl = None
        self.alt = None
        self.saved_file = False
        self.saved_memory = False
        self.alpha_actions = 0

    def startup(self, dt, game_data):
        """Initialize data at scene start."""
        self.game_data = game_data
        self.shortcuts = self.game_data["shortcuts"]
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
        self.capture_new_shortcuts(event)

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
                logger.info("Menu : %d, Shortcut : %d", self.selected_menu, self.selected_shortcut)
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
                logger.info("Menu : %d, Shortcut : %d", self.selected_menu, self.selected_shortcut)
            elif event.key == pg.K_s and pg.key.get_mods() & pg.KMOD_ALT:
                self.game_data["shortcut"] = self.shortcuts
                self.save_shortcuts()
                self.saved_file = True
            elif event.key == pg.K_RETURN:
                if self.is_shortcut_selected:
                    # saved the new shortcut in the program data
                    menu = self.menu_keys[self.selected_menu]
                    shortcut_keys = list(self.shortcuts[menu].keys())
                    shortcut = shortcut_keys[self.selected_shortcut]
                    self.shortcuts[menu][shortcut]["keys"] = self.create_shortcut()
                    logger.info(f"Save {self.create_shortcut()} to {shortcut} in {menu}, memory")
                    self.saved_memory = True
                # select from menu to shortcut and new shortcut
                if self.is_menu_selected:
                    self.is_shortcut_selected = True
                    logger.info("A shortcut is selected")
                else:
                    self.is_menu_selected = True
                    logger.info("A menu is selected")

            elif event.key == pg.K_ESCAPE:
                # unselect all
                if self.is_shortcut_selected:
                    self.is_shortcut_selected = False
                    logger.info("A shortcut is unselected")
                else:
                    self.is_menu_selected = False
                    logger.info("A menu is unselected")

    def capture_new_shortcuts(self, event):
        """Capture key to create a recort form a shortcut

        Args:
            event (Event)
        """
        if event.key is not pg.K_RETURN and self.is_shortcut_selected:
            mod = pg.key.get_mods()
            if mod & pg.KMOD_CTRL:
                self.ctrl = not self.ctrl
                logger.info("CTRL set to %s", self.ctrl)
            elif mod & pg.KMOD_ALT:
                self.alt = not self.alt
                logger.info("ALT set to %s", self.alt)
            else:
                self.key = event.key
                logger.info("KEY set to %s", self.key)

    def save_shortcuts(self):
        """Save shortcuts to a custom file"""
        with open(path.join(self.saved_shortcuts, CUSTOM_SHORTCUTS_FILENAME), 'w') as _f:
            _f.write(json.dumps(self.shortcuts))
            logger.info('Save shortcuts to %s', path.join(self.saved_shortcuts, CUSTOM_SHORTCUTS_FILENAME))

    def create_shortcut(self):
        """Create the array for a shortcut

        Returns:
            list
        """
        return [self.ctrl, self.alt, self.key]

    def draw(self):
        """Draw content"""
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
        if self.saved_file or self.saved_memory:
            self.alpha_actions += 15
        if self.alpha_actions >= 255:
            self.saved_file = False
            self.saved_memory = False
        if self.alpha_actions > 0 and not self.saved_file and not self.saved_memory:
            self.alpha_actions -= 15
        if self.saved_file or self.alpha_actions > 0 or self.saved_memory:
            transition = pg.Surface((WIDTH, HEIGHT))
            transition.fill(BLACK)
            transition.set_alpha(self.alpha_actions)
            self.screen.blit(transition, (0, 0))
            text = ''
            if self.saved_file:
                text = "Saved in a file"
            if self.saved_memory:
                text = "Saved in memory"
            self.draw_text(text, self.title_font, 50, WHITE,
                           WIDTH // 2, HEIGHT / 2, align="center")

    @staticmethod
    def create_text_shortcut(ctrl, alt, key):
        """Create the string the show the chosen shortcut

        Args:
            ctrl (int)
            alt (int)
            key (int)

        Returns:
            str
        """
        return f"{'ctrl + ' if ctrl else ''}{'alt + ' if alt else ''}{pg.key.name(key) if key else ''}"
