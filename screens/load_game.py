"""Load game screen"""

from config.buttons import HEIGHT_BUTTON, MARGIN_BUTTON, RADIUS_BUTTON, WIDTH_BUTTON
import os
import json
from os import path
from datetime import datetime
from pygame_widgets import Button
import pygame as pg
from logger import logger
from window import _State
from config.screens import GAME, LOAD_GAME, TRANSITION_OUT
from config.colors import BEIGE, GREEN_DARK, YELLOW_LIGHT
from config.window import WIDTH, HEIGHT
from data.game_data import create_game_data
from utils.shortcuts import key_for


class LoadGame(_State):
    """Load game screen"""

    def __init__(self):
        self.name = LOAD_GAME
        super(LoadGame, self).__init__(self.name)
        self.next = GAME
        self.state = 'normal'

        image = pg.image.load(
            path.join(
                self.img_folder, 'load_game',
                "background.jpg")).convert()
        self.background = pg.transform.scale(image, (WIDTH, HEIGHT))

        self.font_button = pg.font.Font(self.button_font, 50)
        self.fontsize = 20

        self.selected = 0
        self.games = [
            f for f in os.listdir(
                self.saved_games) if f.endswith('.json')]
        self.len_games = len(self.games)

        self.create_buttons()

    def create_buttons(self):
        x = WIDTH // 2 - (WIDTH_BUTTON + 70) // 2
        y_base = 200
        self.btns = list()
        logger.info("Create all buttons from load_game")
        for index, game in enumerate(self.games):
            self.btns.append(
                self.create_button(
                    self.background, x, y_base + 70 * index, WIDTH_BUTTON + 50, HEIGHT_BUTTON, game.split(".")[0],
                    self.font_button, self.fontsize, MARGIN_BUTTON, RADIUS_BUTTON, BEIGE, YELLOW_LIGHT, GREEN_DARK,
                    self.load, [index]))

    def run(self, surface, keys, mouse, dt):
        """Run states"""
        super().run(surface, keys, mouse, dt)
        update_level = self.states_dict[self.state]
        if self.state != 'normal':
            self.draw()
        update_level()

    def normal_run(self):
        """Run the normal state"""
        self.events_buttons()
        self.draw()

    def events_buttons(self):
        """Used to manage the event for buttons"""
        events = pg.event.get()
        for btn in self.btns:
            btn.listen(events)

    def get_events(self, event):
        """Manage event

        Args:
            event (Event)
        """
        if event.type == pg.KEYDOWN:
            if len(self.games):
                if key_for(
                        self.game_data["shortcuts"]["load_game"]["down"]["keys"],
                        event):
                    self.selected += 1
                    if self.selected >= self.len_games:
                        self.selected = self.len_games - 1
                    logger.info('Game selected : %s',
                                self.games[self.selected])
                if key_for(
                        self.game_data["shortcuts"]["load_game"]["up"]["keys"],
                        event):
                    self.selected -= 1
                    if self.selected < 0:
                        self.selected = 0
                    logger.info('Game selected : %s',
                                self.games[self.selected])
        if event.type == pg.KEYUP:
            if len(self.games):
                if key_for(
                        self.game_data["shortcuts"]["load_game"]["enter"]["keys"],
                        event):
                    self.load(self.games[self.selected])
            if key_for(
                    self.game_data["shortcuts"]["load_game"]["new game"]["keys"],
                    event):
                now = datetime.now()
                date = now.strftime("%Y-%b-%d")
                timestamp = datetime.timestamp(now)
                self.game_data['game_data'] = create_game_data()
                self.game_data['file_name'] = f"{date}-{int(timestamp)}.json"
                logger.info("Start a new game")
                super().set_state(TRANSITION_OUT)
        pg.event.clear()

    def load(self, index):
        """Load the selected files

        Args:
            selected (string): name of the file
        """
        selected = self.games[index]
        try:
            with open(path.join(self.saved_games, selected)) as f:
                self.game_data['game_data'] = json.load(f)
                self.game_data['file_name'] = selected
                super().set_state(TRANSITION_OUT)
                logger.info('Load : %s', selected)
        except EnvironmentError as e:
            logger.exception(e)

    def draw(self):
        """Draw loading page"""
        self.screen.blit(self.background, (0, 0))
        self.draw_text(
            "Load a game",
            self.title_font,
            150,
            YELLOW_LIGHT,
            WIDTH // 2,
            15,
            "n")
        # self.draw_files()
        self.draw_buttons()
        self.draw_text(
            f'Press {pg.key.name(self.game_data["shortcuts"]["load_game"]["new game"]["keys"][2])} to create a new file',
            self.title_font,
            56,
            BEIGE,
            WIDTH //
            2,
            HEIGHT,
            align="s")

    def draw_buttons(self):
        """draw all buttons"""
        for btn in self.btns:
            btn.draw()

    def draw_files(self):
        """Print game data file name"""
        for index, name in enumerate(self.games):
            color = BEIGE
            font_size = 25
            if index == self.selected:
                color = YELLOW_LIGHT
                font_size = 26

            self.draw_text(name, self.text_font, font_size, color, WIDTH //
                           2, 250 + 35 * index, align="center")

    @staticmethod
    def create_button(
            background,
            x,
            y,
            width,
            height,
            text,
            font,
            fontsize,
            margin,
            radius,
            inactive_color,
            hover_color,
            pressed_color,
            on_click,
            on_click_params):
        return Button(
            background,
            x,
            y,
            width,
            height,
            text=text,
            font=font,
            fontSize=fontsize,
            margin=margin,
            radius=radius,
            inactiveColour=inactive_color,
            hoverColour=hover_color,
            pressedColour=pressed_color,
            onClick=on_click,
            onClickParams=on_click_params)
