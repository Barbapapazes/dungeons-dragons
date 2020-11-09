"""Create the main window and the base for all screens"""

from config.screens import TRANSITION_IN, TRANSITION_OUT
from config.colors import BLACK
from config.window import WIDTH, HEIGHT, FPS, TITLE
import pygame as pg
import sys
from os import path
import json


class Window():
    """Manage the window and all the states"""

    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.normal_caption()
        self.clock = pg.time.Clock()
        self.dt = None
        self.keys = pg.key.get_pressed()

        self.done = False
        self.states_dict = {}
        self.state_name = None
        self.state = None

        self.show_fps = False

        self.load_data()

    def load_data(self):
        game_folder = path.dirname('.')
        self.assets_folder = path.join(game_folder, 'assets')
        self.saved_games = path.join(self.assets_folder, 'saved_games')

    def setup_states(self, states_dict, start_state):
        """Load all states"""
        self.states_dict = states_dict
        self.state_name = start_state
        self.state = self.states_dict[self.state_name]

    def flip_state(self):
        """Change state to a new state"""
        previous, self.state_name = self.state_name, self.state.next
        self.persist = self.state.cleanup()
        print(self.persist)
        self.state = self.states_dict[self.state_name]
        self.state.previous = previous
        self.state.startup(self.dt, self.persist)

    def run(self):
        """Run the state"""
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.run(self.screen, self.keys, self.dt)
        self.show_fps_caption()

    def events(self):
        """Manage the event"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                if event.key == pg.K_EQUALS:
                    self.show_fps = not self.show_fps
                    self.normal_caption()
                self.state.get_events(event)
                if event.key == pg.K_s and pg.key.get_mods() & pg.KMOD_CTRL:
                    pg.event.wait()
                    print("save game data")
                    self.save()
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
                self.state.get_events(event)

    def save(self):
        # pourquoi ne pas passer ça dans le state pour gérer la sauvegarde à tout moment
        with open(path.join(self.saved_games, "game_data.json"), "w") as outfile:
            json.dump(self.persist, outfile)

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
        while not self.done:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.run()
            pg.display.update()

    @staticmethod
    def quit():
        """Quit all"""
        pg.quit()
        sys.exit()


class _State():
    """Base class for all screens"""

    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        self.screen = None
        self.keys = None
        self.dt = 0

        self.done = False
        self.quit = False

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
        game_folder = path.dirname('.')
        self.assets_folder = path.join(game_folder, 'assets')
        self.fonts_folder = path.join(self.assets_folder, 'fonts')
        self.title_font = path.join(self.fonts_folder, 'Roboto-Regular.ttf')

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

    def run(self, surface, keys, dt):
        """Run states"""
        self.screen = surface
        self.keys = keys
        self.dt = dt

    def set_state(self, value):
        """Change the state"""
        self.state = value

    def cleanup(self):
        """Finish the screen

        Returns:
            object: game data
        """
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
