"""Menu screen"""

from os import path
from pygame_widgets import Button
import pygame as pg
from window import _State
from logger import logger
from config.window import WIDTH, HEIGHT
from config.screens import GAME, MENU, TRANSITION_OUT, CREDITS, LOAD_GAME, CHARACTER_CREATION
from utils.shortcuts import load_shortcuts
from config.colors import YELLOW_LIGHT, BEIGE, GREEN_DARK
from config.buttons import HEIGHT_BUTTON, WIDTH_BUTTON, RADIUS_BUTTON, MARGIN_BUTTON


class Menu(_State):
    """Menu screen"""

    def __init__(self):
        self.name = MENU
        super(Menu, self).__init__(self.name)
        self.next = GAME

        # Background image
        image = pg.image.load(
            path.join(
                self.img_folder, 'menu',
                "background.jpg")).convert()
        self.image = pg.transform.scale(image, (WIDTH, HEIGHT))

        # Buttons
        self.font_button = pg.font.Font(self.button_font, 50)
        self.fontsize = 20

        self.create_buttons()

        self.startup(0, load_shortcuts())

    def create_buttons_dict(self):
        return {
            "new_game": {
                "text": "New Game",
                "on_click": self.load_next_state,
                "on_click_params": [CHARACTER_CREATION],
            },
            "load_game": {
                "text": "Load a game",
                "on_click": self.load_next_state,
                "on_click_params": [LOAD_GAME],
            },
            "options": {
                "text": "Options",
                "on_click": self.load_next_state,
                "on_click_params": [CREDITS],
            },
            "quit": {
                "text": "Quit",
                "on_click": self.stop_window,
                "on_click_params": [],
            }
        }

    def create_buttons(self):
        x = WIDTH // 2 - WIDTH_BUTTON // 2
        y = 250
        y_base = 250
        self.btns = list()
        logger.info("Create all buttons from menu")
        for index, (key, value) in enumerate(
                self.create_buttons_dict().items()):
            self.btns.append(self.create_button(
                self.image,
                x,
                y_base + index * 100,
                WIDTH_BUTTON,
                HEIGHT_BUTTON,
                value["text"],
                self.font_button,
                self.fontsize,
                MARGIN_BUTTON,
                RADIUS_BUTTON,
                BEIGE,
                YELLOW_LIGHT,
                GREEN_DARK,
                value["on_click"],
                value["on_click_params"]
            ))

    def load_next_state(self, *next_state):
        self.next = next_state[0]
        super().set_state(TRANSITION_OUT)

    def run(self, surface, keys, mouse, dt):
        """Run states"""
        self.screen = surface
        self.keys = keys
        self.mouse = mouse
        self.dt = dt
        update_level = self.states_dict[self.state]
        if self.state != 'normal':
            self.draw()
        update_level()

    def normal_run(self):
        """Run the normal state"""
        self.events_buttons()
        self.draw()

    def events_buttons(self):
        events = pg.event.get()
        for btn in self.btns:
            btn.listen(events)

    def draw(self):
        """Draw content"""
        self.draw_background()
        self.draw_title()
        self.draw_buttons()

    def draw_background(self):
        """Draw the background"""
        self.screen.blit(self.image, (0, 0))

    def draw_title(self):
        """Draw the title"""
        self.draw_text(
            "Dungeons and Dragons",
            self.title_font,
            150,
            YELLOW_LIGHT,
            WIDTH // 2,
            15,
            align="n")

    def draw_buttons(self):
        """Draw all buttons"""
        for btn in self.btns:
            btn.draw()

    @staticmethod
    def stop_window():
        quit_event = pg.event.Event(pg.USEREVENT, code="_State", name="quit")
        pg.event.post(quit_event)

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
