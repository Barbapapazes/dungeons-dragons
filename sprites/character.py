"""Define a character"""

from config.sprites import PLAYER_HIT_RECT
import pygame as pg
from logger import logger
vec = pg.Vector2


class Character(pg.sprite.Sprite):

    def __init__(self, game, x, y, _type, images):
        self._layer = y
        self.groups = game.all_sprites,
        super(Character, self).__init__(self.groups)

        self.game = game
        self.type = _type
        self.images = images

        self.direction = "left"
        self.last_direction = self.direction

        self.x = x
        self.y = y

        self.vel = vec(0, 0)
        self.pos = vec(x, y)

        self.image = next(self.images[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center

        self.frame_time = 60 / 1000
        self.frame_timer = 0
