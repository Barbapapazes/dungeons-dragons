"""Shortcuts screen"""

import pygame as pg
import json
from os import path
from window import _State
from logger import logger
from config.window import WIDTH, HEIGHT
from config.colors import BLACK, WHITE
from config.screens import SHORTCUTS, TRANSITION_OUT
from data.shortcuts import SHORTCUTS_DEFAULT, CUSTOM_SHORTCUTS_FILENAME


class Shortcuts(_State):
    """Shortcuts screen"""

    def __init__(self):
        self.name = SHORTCUTS
        super(Shortcuts, self).__init__(self.name)
        self.next = None

        self.key = None

        self.background = pg.Surface((WIDTH, HEIGHT))

        self.shortcuts = SHORTCUTS_DEFAULT
        self.selected = 0
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
        self.background.fill((255, 0, 255))
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
                self.selected += 1
                if self.selected > len(self.shortcuts.keys()) - 1:
                    self.selected = len(self.shortcuts.keys()) - 1
            elif event.key == pg.K_PAGEDOWN:
                self.selected -= 1
                if self.selected < 0:
                    self.selected = 0
            elif event.key == pg.K_s and pg.key.get_mods() & pg.KMOD_ALT:
                self.save_shortcuts()
                self.saved = True
            elif event.key == pg.K_RETURN:
                for index, (key, [ctrl, alt, k_key]) in enumerate(self.shortcuts.items()):
                    if index == self.selected:
                        self.shortcuts[key] = self.create_shortcut()

            logger.debug(self.selected)

    def save_shortcuts(self):
        """Save shortcuts to a custom file"""
        with open(path.join(self.saved_shortcuts, CUSTOM_SHORTCUTS_FILENAME), 'w') as _f:
            _f.write(json.dumps(self.shortcuts))
            logger.info('Save shortcuts to %s', path.join(self.saved_shortcuts, CUSTOM_SHORTCUTS_FILENAME))

    def create_shortcut(self):
        return [self.ctrl, self.alt, self.key]

    def create_text_shortcut(self, ctrl, alt, key):
        return f"{'ctrl + ' if ctrl else ''} {'alt + ' if alt else ''} {pg.key.name(key) if key else ''}"

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_text("shortcuts".upper(), self.title_font, 48, BLACK, WIDTH // 2, 0, align="n")
        self.draw_text(self.create_text_shortcut(self.ctrl, self.alt, self.key), self.title_font,
                       36, BLACK, WIDTH // 2, HEIGHT // 4, align="n")
        for index, (key, [ctrl, alt, k_key]) in enumerate(self.shortcuts.items()):
            if index == self.selected:
                self.draw_text(f"{key} : {self.create_text_shortcut(ctrl, alt, k_key)}", self.title_font,
                               36, BLACK, WIDTH // 2, HEIGHT // 2, align="center")

        self.draw_saved()

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
