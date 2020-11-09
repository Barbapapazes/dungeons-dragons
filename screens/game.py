"""Game screen"""

import pygame as pg
from os import path
from window import _State
from sprites.player import Player
from config.window import WIDTH, HEIGHT, TILESIZE
from config.colors import LIGHTGREY, BLACK, WHITE
from config.screens import CREDITS, MENU, GAME, TRANSITION_IN, TRANSITION_OUT


class Game(_State):
    """Game screen"""

    def __init__(self):
        super(Game, self).__init__()
        self.name = GAME
        self.next = None

        self.all_sprites = None

        self.states_dict = self.make_states_dict()

        self.load_data()

    def load_data(self):
        game_folder = path.dirname('.')
        self.assets_folder = path.join(game_folder, 'assets')
        self.fonts_folder = path.join(self.assets_folder, 'fonts')
        self.title_font = path.join(self.fonts_folder, 'Roboto-Regular.ttf')

    def startup(self, dt, game_data):
        self.dt = dt
        self.game_data = game_data
        self.all_sprites = pg.sprite.Group()

        Player(self, 2, 4)
        super().setup_transition()

    def make_states_dict(self):
        """Make the dictionary of state methods for the level.


        Returns:
            object: define all the possible states for a screen
        """
        states_dict = {TRANSITION_IN: self.transition_in,
                       TRANSITION_OUT: self.transition_out,
                       'normal': self.normal_run,
                       'menu': self.menu_run
                       }

        return states_dict

    def get_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.next = MENU
                super().set_state(TRANSITION_OUT)
            if event.key == pg.K_RIGHT:
                self.next = CREDITS
                super().set_state(TRANSITION_OUT)
        if event.type == pg.KEYUP:
            if event.key == pg.K_m:
                self.state = 'normal' if self.state == 'menu' else 'menu'

    def run(self, surface, keys, dt):
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
        self.update()
        self.draw()
        self.check_for_menu()

    def menu_run(self):
        """Run the menu state"""
        self.screen.fill(BLACK)
        self.draw_text("C'est un sub-state ! Un menu dans l'écran game",
                       self.title_font, 15, WHITE, WIDTH // 2, HEIGHT // 2, 'center')

    def check_for_menu(self):
        """Check if the user want to access to the menu"""

    @staticmethod
    def draw_grid(surface):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(surface, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(surface, LIGHTGREY, (0, y), (WIDTH, y))

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid(self.screen)
        self.all_sprites.draw(self.screen)
        super().transtition_active(self.screen)
