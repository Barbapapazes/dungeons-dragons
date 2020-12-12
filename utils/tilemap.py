"""Used to manage map and camera"""

import pygame as pg
import pytmx
from config.window import WIDTH, HEIGHT
from logger import logger


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixels_alpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        logger.info("Create the map")
        return temp_surface


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)

        self.camera = pg.Rect(x, y, self.width, self.height)


class Minimap:
    """Create a minimap"""

    def __init__(self, img, w, map_ratio, fog=None, cover=None):
        self.img = img
        self.width = w
        self.height = int(w // map_ratio)
        self.img_ratio = w / img.get_width()
        self.size = (WIDTH * self.img_ratio) // 2

        self.resized_map = pg.transform.scale(self.img, (self.width, self.height))

        # Black screen
        self.cover = pg.Surface(self.resized_map.get_size()).convert_alpha()
        self.cover.fill((7, 7, 10))
        if cover:
            self.cover = cover

        # Fog (to see the under map)
        self.fog = pg.Surface(self.resized_map.get_size()).convert_alpha()
        if fog:
            self.fog = fog
        self.fog_color = (0, 0, 0, 150)
        self.fog.fill(self.fog_color)

    @staticmethod
    def draw_player(_map, pos):
        pg.draw.circle(_map, (0, 255, 0), pos, 3, width=2)

    def create_all_players(self, _map, players):
        for player in players:
            self.draw_player(_map, player.pos * self.img_ratio)

    def update(self, player):
        """Update the frog using a pos

        Args:
            pos (list): the x and y of the player
        """
        pos = player.pos * self.img_ratio
        pg.draw.circle(self.cover, pg.Color(0, 0, 0, 0), pos, self.size)
        self.fog.fill(self.fog_color)
        pg.draw.circle(self.fog, pg.Color(0, 0, 0, 0), pos, self.size)

    def create_minimap_data(self):
        """Create a dict to save minimap data

        Returns:
           dict
        """
        return {
            "fog": self.fog,
            "cover": self.cover
        }

    def create(self, player, players):
        """Create the minimap as a surface

        Args:
            player (Player)

        Returns:
            Surface
        """
        pos = player.pos * self.img_ratio
        temp_map = self.resized_map.copy()

        self.draw_player(temp_map, pos)
        self.create_all_players(temp_map, players)

        temp_map.blit(self.fog, (0, 0))
        temp_map.blit(self.cover, (0, 0))
        return temp_map
