"""Create the main window and the base for all screens"""
import json
import sys
from os import path
from utils.music import load_music

import pygame as pg
from pygame_widgets import Button

from components.cursor import Cursor
from config.buttons import (HEIGHT_BUTTON, MARGIN_BUTTON, RADIUS_BUTTON,
                            WIDTH_BUTTON)
from config.colors import BEIGE, BLACK, GREEN_DARK, WHITE, YELLOW_LIGHT
from config.screens import (CHARACTER_CREATION, INTRODUCTION, NEW_GAME, OPTIONS_MUSIC,
                            SHORTCUTS, TRANSITION_IN, TRANSITION_OUT)
from config.window import FPS, HEIGHT, TITLE, WIDTH
from logger import logger
from managers.music_manager import MusicManager
from utils.shortcuts import key_for, load_shortcuts


class Window():
    """Manage the window and all the states"""

    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        logger.info("Start pygame")
        pg.init()
        logger.info("Create window")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.normal_caption()
        self.clock = pg.time.Clock()
        self.dt = None
        self.keys = pg.key.get_pressed()
        self.mouse = pg.mouse.get_pressed()

        self.done = False
        self.states_dict = {}
        self.state_name = None
        self.state = None

        self.show_fps = False
        self.previous = {}

        self.load_data()

    def load_data(self):
        """Load custom ressouces"""
        logger.info('Load data in main window')
        game_folder = path.dirname('.')
        self.assets_folder = path.join(game_folder, 'assets')
        self.img_folder = path.join(self.assets_folder, 'img')
        self.music_folder = path.join(self.assets_folder, 'music')
        self.saved_games = path.join(self.assets_folder, 'saved_games')
        self.saved_maps = path.join(self.assets_folder, 'saved_maps')
        self.saved_minimap = path.join(self.assets_folder, 'saved_minimap')
        self.saved_shortcuts = path.join(self.assets_folder, 'saved_shortcuts')

        self.shortcuts = load_shortcuts()["shortcuts"]
        self.music_loaded = load_music()["music"]

        self.music = MusicManager(self, self.music_loaded)

    def setup_states(self, states_dict, start_state):
        """Load all states"""
        logger.info("Load states in window")
        self.states_dict = states_dict
        self.state_name = start_state
        self.state = self.states_dict[self.state_name]
        self.music.flip_music()

    def flip_state(self, state=None):
        """Change state to a new state"""
        if not state:
            previous, self.state_name = self.state_name, self.state.next
        else:
            previous, self.state_name = self.state_name, state
        logger.info("Flip state, from %s to %s", previous, self.state_name)
        self.persist = self.state.cleanup()
        self.state = self.states_dict[self.state_name]
        self.shortcuts = self.persist["shortcuts"]
        self.music_loaded = self.persist["music"]
        self.music.set_data(self.music_loaded)
        self.state.previous = previous
        logger.info("Startup %s", self.state_name)
        self.state.startup(self.dt, self.persist)
        self.music.flip_music()

    def run(self):
        """Run the state"""
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.run(self.screen, self.keys, self.mouse, self.dt)
        self.show_fps_caption()
        self.music.update()

    def events(self):
        """Manage the event"""
        events = pg.event.get()
        self.state.all_events(events)
        for event in events:
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                if key_for(self.shortcuts["window"]["fps"]["keys"], event):
                    self.show_fps = not self.show_fps
                    logger.info('Show fps: %s', self.show_fps)
                    self.normal_caption()
                self.state.get_events(event)
                # if key_for(self.shortcuts["window"]["save"]["keys"], event):
                #     pg.event.wait()
                #     self.save()
                if key_for(self.shortcuts["shortcuts"]["show"]["keys"], event):
                    state = self.state.previous if self.state.name == SHORTCUTS else SHORTCUTS
                    self.flip_state(state)
                    logger.info('Toggle shortcuts : %s', state)
                if key_for(self.shortcuts["window"]["music"]["keys"], event):
                    state = self.state.previous if self.state.name == OPTIONS_MUSIC else OPTIONS_MUSIC
                    self.flip_state(state)
                    logger.info('Toggle music option : %s', state)

            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
                self.state.get_events(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse = pg.mouse.get_pressed()
                self.state.get_events(event)
            elif event.type == pg.MOUSEBUTTONUP:
                self.mouse = pg.mouse.get_pressed()
                self.state.get_events(event)
            elif event.type == pg.USEREVENT:
                self.state.get_events(event)

            if event.type == pg.USEREVENT:
                if event.code == "_State":
                    if event.name == "quit":
                        logger.info("User event : quit")
                        self.done = True
                    if event.name == 'save':
                        logger.info("User event: save")
                        self.save(event.data)
                    if event.name == 'reset':
                        logger.info("User event: reset")
                        self.reset()

    def reset(self):
        self.states_dict[NEW_GAME].new()
        self.states_dict[CHARACTER_CREATION].new()
        self.states_dict[INTRODUCTION].new()

    def save(self, data):
        """Used to save the game data"""
        self.save_game_data(data)
        self.save_minimap_data()

    def save_minimap_data(self):
        """Save the fog and the cover from game_data"""
        minimap_data = self.state.game_data["minimap"]
        filename = self.persist["file_name"].split(".json")[0]
        minimap_types = ["cover", "fog"]
        for _type in minimap_types:
            try:
                path_cover = path.join(self.saved_minimap, f"{filename}-{_type}.png")
                pg.image.save(minimap_data[_type], path_cover)
                logger.info('File %s saved in %s', f"{filename}-{_type}.png", path.abspath(self.saved_minimap))
            except EnvironmentError as e:
                logger.exception(e)

    def save_game_data(self, data):
        """Save game_data"""
        try:
            with open(path.join(self.saved_games, self.persist['file_name']), "w") as outfile:
                json.dump(data, outfile)
                logger.info('File %s saved', self.persist['file_name'])
        except EnvironmentError as e:
            logger.exception(e)

    @staticmethod
    def normal_caption():
        """Add title to the window"""
        pg.display.set_caption(TITLE)

    def show_fps_caption(self):
        """Add FPS to the title of the window"""
        if self.show_fps:
            fps = self.clock.get_fps()
            pg.display.set_caption(f"{TITLE} - {fps:.2f}")

    def main(self):
        """Main loop for entire program"""
        logger.info('Start window')
        while not self.done:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.run()
            pg.display.update()

    @staticmethod
    def quit():
        """Quit all"""
        logger.info("Quit window")
        pg.quit()
        sys.exit()


class _State():
    """Base class for all screens"""

    # pylint: disable=too-many-instance-attributes

    def __init__(self, name):
        logger.info('Start state %s', name)
        self.screen = None
        self.keys = None
        self.mouse = None
        self.dt = 0

        self.done = False
        self.quit = False
        self.name = name

        self.state = None
        self.states_dict = self.make_states_dict()
        self.next = None
        self.previous = None

        self.game_data = {}

        self.alpha = None
        self.transition_surface = {}

        self.load_data()

    def load_data(self):
        """Load assets"""
        logger.info('Load data for state %s', self.name)
        game_folder = path.dirname('.')
        self.assets_folder = path.join(game_folder, 'assets')
        self.saved_games = path.join(self.assets_folder, 'saved_games')
        self.saved_maps = path.join(self.assets_folder, 'saved_maps')
        self.levels_maps = path.join(self.assets_folder, 'levels_maps')
        self.saved_minimap = path.join(self.assets_folder, 'saved_minimap')
        self.saved_shortcuts = path.join(self.assets_folder, 'saved_shortcuts')
        self.saved_music = path.join(self.assets_folder, 'saved_music')
        self.saved_settings = path.join(self.assets_folder, 'saved_settings')
        self.fonts_folder = path.join(self.assets_folder, 'fonts')
        self.title_font = path.join(self.fonts_folder, 'Enchanted Land.otf')
        self.text_font = path.join(self.fonts_folder, 'Roboto-Regular.ttf')
        self.button_font = path.join(self.fonts_folder, 'Enchanted Land.otf')
        self.img_folder = path.join(self.assets_folder, 'img')
        self.sprites_folder = path.join(self.assets_folder, 'sprites')

    def draw_text(self, text, font_name, size, color, x, y, align="nw", screen=None):
        """Used to draw text

        Args:
            text (str)
            font_name (str)
            size (int)
            color (tuple)
            x (int)
            y (int)
            align (str, optional): where we want that the text is aligned. Defaults to "nw".
            screen (Surface, optional): Defaults to None.
        """
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        if not screen:
            self.screen.blit(text_surface, text_rect)
        else:
            screen.blit(text_surface, text_rect)

    def startup(self, dt, game_data):
        """Load all data for this screen"""
        logger.info('Start up state %s', self.name)
        self.game_data = game_data
        self.dt = dt
        self.setup_transition()

    def setup_transition(self):
        """Generate all things to manage state transition"""
        self.alpha = 255
        self.state = TRANSITION_IN
        self.transition_surface = pg.Surface((WIDTH, HEIGHT))
        self.transition_surface.fill(BLACK)
        self.transition_surface.set_alpha(self.alpha)

    def get_events(self, event):
        """Manage events one by one

        Args:
            event (Event)
        """

    def all_events(self, events):
        """Manage all events

        Args:
            events (array)
        """

    def run(self, surface, keys, mouse, dt):
        """Run states"""
        self.screen = surface
        self.keys = keys
        self.mouse = mouse
        self.dt = dt

    def set_state(self, value):
        """Change the state"""
        self.state = value

    def cleanup(self):
        """Finish the screen

        Returns:
            object: game data
        """
        logger.info('Quit state %s', self.name)
        self.done = False
        return self.game_data

    def make_states_dict(self):
        """Make the dictionary of state methods for the level.


        Returns:
            object: define all the possible states for a screen
        """
        states_dict = {
            TRANSITION_IN: self.transition_in,
            TRANSITION_OUT: self.transition_out,
            'normal': self.normal_run
        }

        return states_dict

    def transition_in(self):
        """Transition into scene with a fade."""
        self.transition_surface.set_alpha(self.alpha)
        self.alpha -= 25
        if self.alpha <= 0:
            self.alpha = 0
            self.state = 'normal'
        self.transtition_active(self.screen)

    def transition_out(self):
        """Transition out of scene with a fade."""
        self.transition_surface.set_alpha(self.alpha)
        self.alpha += 25
        if self.alpha >= 255:
            self.done = True
        self.transtition_active(self.screen)

    def transtition_active(self, surface):
        """Check if there is a transition to remove the unused blit surface"""
        surface.blit(self.transition_surface, (0, 0))

    def normal_run(self):
        """Update the normal state"""

    def toggle_sub_state(self, state):
        """Toggle a substate from a state

        Args:
            state (str): the name of the substate
        """
        sub_state = 'normal' if self.state == state else state
        logger.info('Start sub-state %s in %s', sub_state, self.name)
        self.game_data["music"]["sound"]["click"] = True
        self.set_state(sub_state)


class _Elements(_State):
    """Used to create a absctract layer to add a backround and simple buttons over a state and under a screen"""

    def __init__(self, name, _next, folder_name, img_name, btns_dict, **kwargs):
        logger.info('Start elements %s', name)
        self.name = name
        super(_Elements, self).__init__(name)
        self.next = _next
        self.btns = list()
        self.btns_dict = btns_dict

        # load the background image
        image = pg.image.load(
            path.join(self.img_folder, folder_name, img_name)).convert()
        self.image = pg.transform.scale(image, (WIDTH, HEIGHT))
        self.background = self.image.copy()

        # button
        self.fontsize = 50
        self.action = False
        self.action_alpha = 0

        offset = kwargs.get('btns_offset', 80)
        width = kwargs.get('btns_width', WIDTH_BUTTON)
        start_y_offset = kwargs.get('btns_start_y_offset', 250)
        self.create_buttons(self.background, start_y_offset=start_y_offset, offset=offset, width=width)

    def create_back_button(self, background, on_click, on_click_params):
        """Create the back button"""
        _x = HEIGHT_BUTTON
        _y = HEIGHT_BUTTON
        self.back_btn = self.create_button(
            background, _x, _y, WIDTH_BUTTON // 2, HEIGHT_BUTTON // 2, "Back", self.button_font, self.fontsize // 2,
            MARGIN_BUTTON, RADIUS_BUTTON, BEIGE, YELLOW_LIGHT, GREEN_DARK, on_click, on_click_params)

    def draw_action(self, content):
        """Draw a screen with the content

        Args:
            content (str): message to show
        """
        if self.action:
            self.action_alpha += 300 * self.dt

        if self.action_alpha >= 255:
            self.action = False

        if self.action_alpha > 0 and not self.action:
            self.action_alpha -= 300 * self.dt

        if self.action or self.action_alpha > 0:
            transition = pg.Surface((WIDTH, HEIGHT)).convert_alpha()
            transition.fill(BLACK)
            transition.set_alpha(self.action_alpha)
            self.draw_text(content, self.title_font, 50, WHITE,
                           WIDTH // 2, HEIGHT / 2, align="center", screen=transition)
            self.screen.blit(transition, (0, 0))

    def create_buttons(self, background, start_y_offset=250, offset=80, width=WIDTH_BUTTON):
        """Create buttons"""
        _x = WIDTH // 2 - WIDTH_BUTTON // 2
        y_base = start_y_offset
        self.btns = list()
        logger.info("Create all buttons from %s", self.name)
        for index, (_, value) in enumerate(
                self.btns_dict.items()):
            if value["text"]:
                self.btns.append(self.create_button(
                    background,
                    _x,
                    y_base + index * offset,
                    width,
                    HEIGHT_BUTTON,
                    value["text"],
                    self.button_font,
                    self.fontsize,
                    MARGIN_BUTTON,
                    RADIUS_BUTTON,
                    BEIGE,
                    YELLOW_LIGHT,
                    GREEN_DARK,
                    value["on_click"],
                    value["on_click_params"]
                ))

    def all_events(self, events):
        """Used to access to all events in a screen

        Args:
            events (Events)
        """

    def load_next_state(self, *next_state):
        """Load the new state"""
        self.next = next_state[0]
        self.game_data["music"]["sound"]["click"] = True
        super().set_state(TRANSITION_OUT)

    def events_buttons(self, back=False):
        """Used to manage the event for buttons"""
        events = pg.event.get()
        for btn in self.btns:
            btn.listen(events)
        if back:
            self.back_btn.listen(events)

    def draw_elements(self, name, back=False, background=True):
        """Draw all elements"""
        if background:
            self.draw_background()
        self.draw_title(name)
        self.draw_buttons(back)

    def draw_background(self):
        """Draw the background"""
        self.screen.blit(self.background, (0, 0))

    def draw_title(self, title):
        """Draw the title"""
        self.draw_text(
            title,
            self.title_font,
            150,
            YELLOW_LIGHT,
            WIDTH // 2,
            min(15, 1 * HEIGHT // 20),
            align="n")

    def draw_subtitle(self, subtitle):
        """Draw the subtitle"""
        self.draw_text(
            subtitle,
            self.title_font,
            60,
            YELLOW_LIGHT,
            WIDTH // 2,
            min(180, 6 * HEIGHT // 20),
            align="n")

    def draw_buttons(self, back=False):
        """Draw all buttons"""
        for btn in self.btns:
            btn.draw()
        if back:
            self.back_btn.draw()

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
        """Create button

        Args:
            background (Surface)
            x (int)
            y (int)
            width (int)
            height (int)
            text (str)
            font (Font)
            fontsize (int)
            margin (int)
            radius (int)
            inactive_color (tuple)
            hover_color (tuple)
            pressed_color (tuple)
            on_click (fn)
            on_click_params (list)

        Returns:
            Button
        """
        return Button(
            background,
            x,
            y,
            width,
            height,
            text=text,
            font=pg.font.Font(font, fontsize),
            fontSize=fontsize,
            margin=margin,
            radius=radius,
            inactiveColour=inactive_color,
            hoverColour=hover_color,
            pressedColour=pressed_color,
            onClick=on_click,
            onClickParams=on_click_params)

    @staticmethod
    def create_slider(
            title,
            name,
            x,
            y,
            width,
            height,
            surface,
            min,
            max,
            step,
            start,
            font,
            draw_text, color, handle_color):
        """Create a slider

        Args:
            title (str)
            name (str)
            x (int)
            y (int)
            width (int)
            height (int)
            surface (Surface)
            min (int)
            max (int)
            step (int)
            start (int)
            font (str)
            draw_text (func)
            color (tuple)
            handle_color (tuple)

        Returns:
            Cursor
        """
        return Cursor(
            title,
            name,
            x,
            y,
            width,
            height,
            surface,
            min,
            max,
            step,
            start,
            font,
            draw_text, color, handle_color)
