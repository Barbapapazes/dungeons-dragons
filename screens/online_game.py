"""Online game screen"""

from utils.tilemap import Camera, Minimap, TiledMap
from config.sprites import ASSETS_SPRITES
import pygame as pg
from os import path
from window import _State
from logger import logger
from sprites.player import Arrow, Player
from server.network import Network
from config.window import WIDTH, HEIGHT, TILESIZE
from config.colors import GREEN, LIGHTGREY, BLACK, RED, WHITE, YELLOW
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

        self.map = TiledMap(path.join(self.levels_maps, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        # self.minimap = Minimap(
        #     self.map_img,
        #     225,
        #     self.map_rect.width /
        #     self.map_rect.height, self.game_data["minimap"]["fog"], self.game_data["minimap"]["cover"])
        self.camera = Camera(self.map.width, self.map.height)

    def startup(self, dt, game_data):
        self.dt = dt
        self.game_data = game_data
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.arrows = pg.sprite.Group()

        self.server = Network()
        self.current_id = self.server.connect()

        # brut data from the server
        self.current_players, self.current_arrows = self.server.send("get")
        # dict with all players
        self.players = self.create_players(self.current_players)
        self.current_player = self.current_players[self.current_id]
        self.player = Player(
            self, self.current_player["pos"]["x"], self.current_player["pos"]["y"],
            '', {},
            100, 0, 100, ASSETS_SPRITES["soldier"])
        # create all arrows
        self.new_arrows = dict()

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
                self.players[key].health = player["health"]
                if key == self.current_id:
                    logger.error(player["health"])
                    self.player.health = player["health"]
                players_dict[key] = self.players[key]
            elif key != self.current_id:
                p = Player(
                    self, player["pos"]["x"], player["pos"]["y"],
                    '', {},
                    100, 0, 100, ASSETS_SPRITES["soldier"])
                p.set_vel((player["vel"]["x"], player["vel"]["y"]))
                players_dict[key] = p
        return players_dict

    def create_arrows(self, arrows):
        arrows_dict = dict()
        for key, value in arrows.items():
            if key in self.new_arrows.keys():
                self.new_arrows[key].update()
                # il faut mettre à jour la flèche dans le server
                # il faut ajouter le current id pour que le current joueur mette à jour les arrows et envoie l'update au server
                if not self.new_arrows[key].is_deleted:
                    arrows_dict[key] = self.new_arrows[key]
                    data = " ".join(["arrow", "update", str(self.new_arrows[key].id),
                                     str(self.new_arrows[key].pos.x), str(self.new_arrows[key].pos.y)])
                    self.server.send(data)
            else:
                # logger.debug(value)
                # logger.debug(arrows)
                pos = vec(int(value["pos"]["x"]), int(value["pos"]["y"]))
                dir = vec(float(value["dir"]["x"]), float(value["dir"]["y"]))
                # logger.debug("on a un souci avec le dir, il vaut 0 et dont la velocity est null")
                a = Arrow(self,
                          pos,
                          dir,
                          int(value["damage"]), key, self.current_id)
                arrows_dict[key] = a

        return arrows_dict

    def update(self):
        # il va falloir faire une fonction send data en plus de update et draw je pense
        data = "move " + str(int(self.player.pos.x)) + " " + str(int(self.player.pos.y)
                                                                 ) + " " + str(int(self.player.vel.x)) + " " + str(int(self.player.vel.y))
        try:
            self.current_players, self.current_arrows = self.server.send(data)
        except:
            pass
        self.players = self.create_players(self.current_players)
        self.new_arrows = self.create_arrows(self.current_arrows)
        self.current_player = self.current_players[self.current_id]
        self.camera.update(self.player)

        self.player.update()
        # for _, arrow in self.new_arrows.items():
        #     arrow.update()
        # hits = pg.sprite.spritecollide(self.player, self.new_arrows, False)
        # for hit in hits:
        #     if hit.player_id == self.current_id:
        #         logger.debug(hit)

    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        self.screen.blit(self.player.image, self.camera.apply(self.player))

        for _, player in self.players.items():
            self.screen.blit(player.image, self.camera.apply(player))

        # on peut utiliser value
        for _, arrow in self.new_arrows.items():
            self.screen.blit(arrow.image, self.camera.apply(arrow))

        # logger.debug(self.player.health)
        draw_player_health(self.screen, 10, 10, self.current_player["health"] / 100)
        # il faut mettre une constante sur le 100

        # for arrow in self.arrows:
        #     self.screen.blit(arrow.image, self.camera.apply(arrow))

        super().transtition_active(self.screen)


def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    # logger.debug(pct)
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outlined_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outlined_rect, 2)
