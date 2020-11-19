"""Load game screen"""

import pygame as pg
import os
import json
from os import path
from logger import logger
from window import _State
from config.screens import MENU, LOAD_GAME, TRANSITION_OUT
from config.colors import BURGUNDY, WHITE
from config.window import WIDTH, HEIGHT
from data.game_data import create_game_data


class LoadGame(_State):
    """Load game screen"""

    def __init__(self):
        self.name = LOAD_GAME
        super(LoadGame, self).__init__(self.name)
        self.next = MENU
        self.state = 'normal'

        self.background = pg.Surface((WIDTH, HEIGHT))

        # if (len(games) == 1):
        #     with open(path.join(self.saved_games, games[0])) as f:
        #         self.startup(0, json.load(f))
        # else:
        #     self.startup(0, create_game_data())
        self.selected = 0
        self.games = [f for f in os.listdir(self.saved_games) if f.endswith('.json')]
        self.len_games = len(self.games)

        self.startup(0, 0)

    def run(self, surface, keys, mouse, dt):
        """Run states"""
        super().run(surface, keys, mouse, dt)
        update_level = self.states_dict[self.state]
        if self.state != 'normal':
            self.draw()
        update_level()

    def normal_run(self):
        """Run the normal state"""
        self.draw()

    def get_events(self, event):
        """Manage event

        Args:
            event (Event)
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                self.selected += 1
                if self.selected >= self.len_games:
                    self.selected = self.len_games - 1
                logger.info('Game selected : %s', self.games[self.selected])
            if event.key == pg.K_UP:
                self.selected -= 1
                if self.selected < 0:
                    self.selected = 0
                logger.info('Game selected : %s', self.games[self.selected])
        if event.type == pg.KEYUP:
            if event.key == pg.K_RETURN:
                self.load(self.games[self.selected])

        pg.event.clear()

    def load(self, selected):
        """Load the selected files

        Args:
            selected (string): name of the file
        """
        try:
            with open(path.join(self.saved_games, selected)) as f:
                self.game_data = json.load(f)
                self.game_data['file_name'] = selected
                super().set_state(TRANSITION_OUT)
                logger.info('Load : %s', selected)
        except EnvironmentError as e:
            logger.exception(e)

    def draw(self):
        """Draw loading page"""
        self.background.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        self.draw_text("Load a game", self.title_font, 30, WHITE, WIDTH // 2, HEIGHT // 2, "center")
        self.draw_files()

    def draw_files(self):
        """Print game data file name"""
        for index, name in enumerate(self.games):
            color = WHITE
            font_size = 25
            if index == self.selected:
                color = BURGUNDY
                font_size = 26

            self.draw_text(name, self.title_font, font_size, color, WIDTH //
                           2, HEIGHT * 6 / 10 + 35 * index, align="center")
