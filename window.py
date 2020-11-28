"""Create the main window and the base for all screens"""
import os
from os import path
import pygame as pg
import sys
import json
from logger import logger
from config.screens import TRANSITION_IN, TRANSITION_OUT, SHORTCUTS
from config.colors import BLACK
from config.window import WIDTH, HEIGHT, FPS, TITLE
from data.shortcuts import SHORTCUTS_DEFAULT, CUSTOM_SHORTCUTS_FILENAME
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

        self.load_data()

    def load_data(self):
        """Load custom ressouces"""
        logger.info('Load data in main window')
        game_folder = path.dirname('.')
        self.assets_folder = path.join(game_folder, 'assets')
        self.img_folder = path.join(self.assets_folder, 'img')
        self.saved_games = path.join(self.assets_folder, 'saved_games')
        self.saved_maps = path.join(self.assets_folder, 'saved_maps')
        self.saved_shortcuts = path.join(self.assets_folder, 'saved_shortcuts')

        self.shortcuts = load_shortcuts()["shortcuts"]
        logger.info("Shortcuts loaded in window: %s", self.shortcuts)

    def setup_states(self, states_dict, start_state):
        """Load all states"""
        logger.info("Load states in window")
        self.states_dict = states_dict
        self.state_name = start_state
        self.state = self.states_dict[self.state_name]

    def flip_state(self, state=None):
        """Change state to a new state"""
        if not state:
            previous, self.state_name = self.state_name, self.state.next
        else:
            previous, self.state_name = self.state_name, state
        logger.info("Flip state, from %s to %s", previous, self.state_name)
        self.persist = self.state.cleanup()
        self.state = self.states_dict[self.state_name]
        print(self.persist)
        self.shortcuts = self.persist["shortcuts"]
        self.state.previous = previous
        logger.info("Startup %s", self.state_name)
        self.state.startup(self.dt, self.persist)

    def run(self):
        """Run the state"""
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.run(self.screen, self.keys, self.mouse, self.dt)
        self.show_fps_caption()

    def events(self):
        """Manage the event"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                if key_for(self.shortcuts["window"]["fps"]["keys"], event):
                    self.show_fps = not self.show_fps
                    logger.info('Show fps: %s', self.show_fps)
                    self.normal_caption()
                self.state.get_events(event)
                if key_for(self.shortcuts["window"]["save"]["keys"], event):
                    pg.event.wait()
                    self.save()
                if key_for(self.shortcuts["shortcuts"]["show"]["keys"], event):
                    state = self.state.previous if self.state.name == SHORTCUTS else SHORTCUTS
                    self.flip_state(state)
                    logger.info('Toggle shortcuts : %s', state)

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
                if event.code =="_State":
                    if event.name == "quit":
                        logger.info("User event : quit")
                        self.done = True

    def save(self):
        """Save game_data"""
        try:
            with open(path.join(self.saved_games, self.persist['file_name']), "w") as outfile:
                file_name = self.persist['file_name']
                shortcuts = self.persist['shortcuts']
                del self.persist['file_name']
                del self.persist['shortcuts']
                # Remove the file name to be able to change manually the file name
                # Remove shortcuts because they have their own file
                json.dump(self.persist["game_data"], outfile)
                self.persist['file_name'] = file_name
                self.persist['shortcuts'] = shortcuts
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
        self.saved_shortcuts = path.join(self.assets_folder, 'saved_shortcuts')
        self.fonts_folder = path.join(self.assets_folder, 'fonts')
        self.title_font = path.join(self.fonts_folder, 'Enchanted Land.otf')
        self.text_font = path.join(self.fonts_folder, 'Roboto-Regular.ttf')
        self.button_font = path.join(self.fonts_folder, 'Enchanted Land.otf')
        self.img_folder = path.join(self.assets_folder, 'img')

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
        """Manage the event for this screen"""

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
        self.set_state(sub_state)
