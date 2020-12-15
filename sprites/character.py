"""Define a character"""

from utils.tilemap import collide_with_walls
from config.sprites import PLAYER_HIT_RECT
import pygame as pg
from logger import logger
vec = pg.Vector2


class Character(pg.sprite.Sprite):

    def __init__(self, game, x, y, _type, images, hit_rect):
        self._layer = y
        self.groups = game.all_sprites,
        super(Character, self).__init__(self.groups)

        self.game = game
        self.type = _type
        self.images = images

        self.direction = "left"

        self.x = x
        self.y = y

        self.vel = vec(0, 0)
        self.pos = vec(x, y)

        self.image = next(self.images[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = hit_rect
        self.hit_rect.center = self.rect.center

        self.frame_time = 60 / 1000
        self.frame_timer = 0

    def update(self):
        self.update_image()

        self.pos += self.vel * self.game.dt
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.update_collisions()

    def update_image(self):
        self.frame_timer += self.game.dt
        if self.frame_timer >= self.frame_time:
            self.frame_timer -= self.frame_time
            self.image = next(self.images[self.direction])

    def update_collisions(self):
        """Manage the collisions"""
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def __str__(self):
        return f"Sprite {self.type}"
