"""Online game screen"""

from config.sprites import ASSETS_SPRITES
import pygame as pg
from os import path
from window import _State
from logger import logger
from sprites.player import Player
from server.network import Network
from config.window import WIDTH, HEIGHT, TILESIZE
from config.colors import LIGHTGREY, BLACK, WHITE, YELLOW
from config.screens import CREDITS, MENU, GAME, TRANSITION_IN, TRANSITION_OUT


class OnlineGame(_State):
    """Online game screen"""

    def __init__(self):
        self.name = "online_game"
        super(OnlineGame, self).__init__(self.name)

        self.current_id = None
        self.player = None
        self.players = dict()

        self.server = None

        self.all_sprites = None

    def startup(self, dt, game_data):
        self.dt = dt
        self.game_data = game_data
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        self.server = Network()
        self.current_id = self.server.connect()
        self.players = self.server.send("get")
        self.current_player = self.players[self.current_id]

        self.player = Player(
            self, self.current_player["x"] * TILESIZE - TILESIZE // 2, self.current_player["y"] * TILESIZE - TILESIZE // 2,
            '', {},
            100, 0, 100, ASSETS_SPRITES["soldier"])

        super().setup_transition()

    def get_events(self, event):
        pass

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
        self.update()
        self.draw()

    @staticmethod
    def draw_grid(surface):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(surface, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(surface, LIGHTGREY, (0, y), (WIDTH, y))

    def update(self):
        # il va falloir faire une fonction send data en plus de update et draw je pense
        self.player.update()
        data = "move " + str(int(self.player.pos.x)) + " " + str(int(self.player.pos.y))
        self.players = self.server.send(data)
        # for key, player in self.players.items():
        #     if key != self.current_id:
        #         Player(
        #             self, player["x"] * TILESIZE - TILESIZE // 2, player["y"] * TILESIZE -
        #             TILESIZE // 2, '', {},
        #             100, 0, 100, ASSETS_SPRITES["soldier"])

        # logger.info(self.all_sprites)

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid(self.screen)
        self.all_sprites.draw(self.screen)
        for key, player in self.players.items():
            if key != self.current_id:
                pg.draw.circle(self.screen, YELLOW, (player["x"], player["y"]), TILESIZE)

        super().transtition_active(self.screen)
