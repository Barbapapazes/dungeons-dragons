"""Online game screen"""

from os import path

import pygame as pg
from config.colors import BEIGE, GREEN, LIGHTGREY, RED, WHITE, YELLOW
from config.screens import MENU, ONLINE_GAME
from config.sprites import ASSETS_SPRITES, PLAYER_MAX_HP
from config.window import HEIGHT, TILESIZE, WIDTH
from logger import logger
from server.network import Network
from sprites.player import Arrow, Player
from utils.tilemap import Camera, TiledMap
from window import _Elements

vec = pg.Vector2


class OnlineGame(_Elements):
    """Online game screen"""

    def __init__(self):
        self.name = ONLINE_GAME
        self.next = MENU
        super(OnlineGame, self).__init__(self.name, self.next, 'menu', '0.png', {})

        self.current_id = None
        self.player = None
        self.players = dict()

        self.server = None

        self.all_sprites = None
        self.walls = None
        self.arrows = None
        self.current_players = None
        self.current_arrows = None
        self.current_player = None
        self.players = dict()
        self.created_arrows = None

        # map
        self.map = TiledMap(path.join(self.levels_maps, 'arena.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
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
        # dict with current player
        self.current_player = self.current_players[self.current_id]
        # current player
        self.player = Player(
            self, self.current_player["pos"]["x"], self.current_player["pos"]["y"],
            '', {}, ASSETS_SPRITES["soldier"])

        # all created arrows
        self.created_arrows = dict()

        super().setup_transition()

    def make_states_dict(self):
        """Create the state dict

        Returns:
            dict
        """
        previous_dict = super().make_states_dict().copy()
        add_dict = {
            "dead": self.dead_run
        }
        return previous_dict | add_dict

    def create_buttons_dict(self):
        """Create the dict for all buttons


        Returns:
            dict
        """
        return {
            "menu": {
                "text": "Menu",
                "on_click": self.load_next_state,
                "on_click_params": [MENU]
            }
        }

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

    def dead_run(self):
        """Run the dead state"""
        self.dead_update()
        self.dead_draw()

    def dead_update(self):
        """Update the dead state"""
        super().events_buttons()

    def dead_draw(self):
        """Draw the dead state"""
        self.dead_draw_background()
        self.draw_text("Game over", self.title_font, 128, BEIGE, WIDTH // 2, HEIGHT // 2, align="center")
        super().draw_buttons()

    def dead_draw_background(self):
        """Draw the dead background of the dead state"""
        self.draw()
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.screen.blit(self.dim_screen, (0, 0))

    def create_players(self, players):
        """Create players if not created and update if already created

        Args:
            players (Player)

        Returns:
            dict
        """
        players_dict = dict()
        for key, player in players.items():
            if key in self.players.keys():
                # update if already exist
                self.players[key].set_pos(vec(player["pos"]["x"], player["pos"]["y"]))
                self.players[key].set_vel((player["vel"]["x"], player["vel"]["y"]))
                self.players[key].health = player["health"]
                if key == self.current_id:
                    logger.error(player["health"])
                    self.player.health = player["health"]
                players_dict[key] = self.players[key]
            elif key != self.current_id:
                # create if not existe
                p = Player(
                    self, player["pos"]["x"], player["pos"]["y"],
                    '', {}, ASSETS_SPRITES["soldier"])
                p.set_vel((player["vel"]["x"], player["vel"]["y"]))
                players_dict[key] = p
        return players_dict

    def create_arrows(self, arrows):
        """Create arrows if not created and update if already created

        Args:
            arrows (Arrow)

        Returns:
            dict
        """
        arrows_dict = dict()
        for key, value in arrows.items():
            if key in self.created_arrows.keys():
                # update if already existe
                self.created_arrows[key].update()
                if not self.created_arrows[key].is_deleted:
                    arrows_dict[key] = self.created_arrows[key]
                    if self.current_id == self.created_arrows[key].player_id:
                        data = " ".join(["arrow", "update", str(self.created_arrows[key].id),
                                         str(self.created_arrows[key].pos.x), str(self.created_arrows[key].pos.y)])
                        self.server.send(data)
            else:
                # create a new arrow
                pos = vec(int(value["pos"]["x"]), int(value["pos"]["y"]))
                dir = vec(float(value["dir"]["x"]), float(value["dir"]["y"]))
                vel = vec(float(value["vel"]["x"]), float(value["vel"]["y"]))
                a = Arrow(self,
                          pos,
                          dir,
                          vel,
                          int(value["damage"]), key, self.current_id)
                arrows_dict[key] = a

        return arrows_dict

    def update(self):
        """Update main state"""
        self.update_data_server()
        self.update_data()

        self.camera.update(self.player)
        self.player.update()

        self.check_death_player()

    def update_data_server(self):
        """Call the server to update data"""
        data = "move " + str(int(self.player.pos.x)) + " " + str(int(self.player.pos.y)
                                                                 ) + " " + str(int(self.player.vel.x)) + " " + str(int(self.player.vel.y))
        try:
            self.current_players, self.current_arrows = self.server.send(data)
        except Exception as e:
            logger.exception(e)

    def update_data(self):
        """Update state data using server data"""
        self.players = self.create_players(self.current_players)
        self.created_arrows = self.create_arrows(self.current_arrows)
        self.current_player = self.current_players[self.current_id]

    def check_death_player(self):
        """Check if the player is dead"""
        if self.current_player["health"] <= 0:
            self.server.disconnect()
            self.btns_dict = self.create_buttons_dict()
            self.create_buttons(self.screen, start_y_offset=8 * HEIGHT / 10)
            self.toggle_sub_state("dead")

    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        self.screen.blit(self.player.image, self.camera.apply(self.player))

        for player in self.players.values():
            self.screen.blit(player.image, self.camera.apply(player))

        for arrow in self.created_arrows.values():
            self.screen.blit(arrow.image, self.camera.apply(arrow))

        self.draw_player_health(10, 10)

        super().transtition_active(self.screen)

    def draw_player_health(self, x, y):
        """Draw player health

        Args:
            x (int)
            y (int)
        """
        points = self.current_player["health"] / PLAYER_MAX_HP
        if points < 0:
            points = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 20
        fill = points * BAR_LENGTH
        outlined_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        if points > 0.6:
            color = GREEN
        elif points > 0.3:
            color = YELLOW
        else:
            color = RED
        pg.draw.rect(self.screen, color, fill_rect)
        pg.draw.rect(self.screen, WHITE, outlined_rect, 2)
