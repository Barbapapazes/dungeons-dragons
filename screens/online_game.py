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
vec = pg.Vector2


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

        # brut data from the server
        self.current_players = self.server.send("get")
        # dict with all players
        self.players = self.create_players(self.current_players)
        self.current_player = self.current_players[self.current_id]
        self.player = Player(
            self, self.current_player["pos"]["x"], self.current_player["pos"]["y"],
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

    def create_players(self, players):
        players_dict = dict()
        for key, player in players.items():
            if key in self.players.keys():
                self.players[key].set_pos(vec(player["pos"]["x"], player["pos"]["y"]))
                self.players[key].set_vel((player["vel"]["x"], player["vel"]["y"]))
                players_dict[key] = self.players[key]
            elif key != self.current_id:
                p = Player(
                    self, player["pos"]["x"], player["pos"]["y"],
                    '', {},
                    100, 0, 100, ASSETS_SPRITES["soldier"])
                p.set_vel((player["vel"]["x"], player["vel"]["y"]))
                players_dict[key] = p

            # il faut ajouter une fonction set pos et set vel pour changer l'image du player

        return players_dict

    def update(self):
        # il va falloir faire une fonction send data en plus de update et draw je pense
        data = "move " + str(int(self.player.pos.x)) + " " + str(int(self.player.pos.y)
                                                                 ) + " " + str(int(self.player.vel.x)) + " " + str(int(self.player.vel.y))
        self.current_players = self.server.send(data)
        self.players = self.create_players(self.current_players)
        self.current_player = self.current_players[self.current_id]
        self.player.update()

        # for key, player in self.players.items():
        # logger.debug(self.players)
        #     if key != self.current_id:
        #         Player(
        #             self, player["x"] * TILESIZE - TILESIZE // 2, player["y"] * TILESIZE -
        #             TILESIZE // 2, '', {},
        #             100, 0, 100, ASSETS_SPRITES["soldier"])

        # logger.info(self.all_sprites)

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        for _, player in self.players.items():
            self.screen.blit(player.image, player.rect)

        super().transtition_active(self.screen)
