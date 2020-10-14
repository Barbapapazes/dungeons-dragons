"""Create the main window and the base for all screens"""

import sys
import pygame as pg
from config.window import WIDTH, HEIGHT, FPS, TITLE
from config.colors import BLACK


class Window():
    """Manage the window and all the states"""

    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.normal_caption()
        self.clock = pg.time.Clock()
        self.dt = None

        self.done = False
        self.current_time = 0.0
        self.keys = pg.key.get_pressed()
        self.states_dict = {}
        self.state_name = None
        self.state = None

        self.show_fps = False

    def setup_states(self, states_dict, start_state):
        """Load all states"""
        self.states_dict = states_dict
        self.state_name = start_state
        self.state = self.states_dict[self.state_name]

    def flip_state(self):
        """Change state to a new state"""
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.states_dict[self.state_name]
        self.state.previous = previous
        self.state.startup(self.current_time, persist)

    def update(self):
        """Update the state"""
        self.current_time = pg.time.get_ticks()
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, self.keys, self.current_time)
        self.show_fps_caption()
        pg.display.update()

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
                self.state.events(event)
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
                self.state.events(event)

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
            self.update()

    @staticmethod
    def quit():
        """Quit all"""
        pg.quit()
        sys.exit()


class _State():
    """Base class for all screens"""

    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0

        self.done = False
        self.quit = False

        self.state = None
        self.states_dict = self.make_states_dict()
        self.next = None
        self.previous = None

        self.game_data = {}

        self.alpha = None
        self.transition_surface = {}

    def startup(self, current_time, game_data):
        """Load all data for this screen"""
        self.game_data = game_data
        self.start_time = current_time

    def setup_transition(self):
        """Generate all things to manage state transition"""
        self.alpha = 255
        self.state = 'transition in'
        self.transition_surface = pg.Surface((WIDTH, HEIGHT))
        self.transition_surface.fill(BLACK)
        self.transition_surface.set_alpha(self.alpha)

    def events(self, event):
        """Manage the event for this screen"""

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

    def update(self, surface, keys, current_time):
        """Update states"""

    def make_states_dict(self):
        """Make the dictionary of state methods for the level.


        Returns:
            object: define all the possible states for a screen
        """
        states_dict = {'transition in': self.transition_in,
                       'transition out': self.transition_out,
                       'normal': self.normal_update}

        return states_dict

    def transition_in(self, *arg):
        """Transition into scene with a fade."""
        self.transition_surface.set_alpha(self.alpha)
        self.alpha -= 35
        if self.alpha <= 0:
            self.alpha = 0
            self.state = 'normal'

    def transition_out(self, *arg):
        """Transition out of scene with a fade."""
        self.transition_surface.set_alpha(self.alpha)
        self.alpha += 35
        if self.alpha >= 255:
            self.done = True

    def transtition_active(self, surface):
        """Check if there is a transition to remove the unused blit surface"""
        if self.state != 'normal':
            surface.blit(self.transition_surface, (0, 0))

    def normal_update(self, *arg):
        """Update the normal state"""
