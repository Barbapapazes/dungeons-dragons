"""Used to create a animated sprite"""

import pygame as pg
from pygame.image import get_sdl_image_version
from config.sprites import ASSETS_FLAMES
from random import randint
from collections import deque

default_fn = lambda *args: None


class Animated(pg.sprite.Sprite):
    """Create a animated sprite"""

    def __init__(self, game, frame_per_image, frames, offset=0):
        self.groups = game.animated
        super(Animated, self).__init__(self.groups)

        self.game = game

        images = deque(frames)
        images.rotate(-offset)
        self.frames = images
        self.image = images[0]

        self.rect = self.image.get_rect()
        self.frame_per_image = frame_per_image
        self.frame_total = (len(frames) - 1) * frame_per_image
        self.frame_count = 0

    def update(self, fn=default_fn, *args):
        """Update the sprite"""
        self.frame_count += 1
        if self.frame_count > self.frame_total + 0:
            self.frame_count = 0
            fn(*args)
        else:
            self.image = self.frames[self.frame_count // self.frame_per_image]


class Flames(Animated):
    """Used to create a flame"""

    def __init__(self, game, x, y, width):
        self.x = x
        self.y = y
        self.width = width

        frame_per_image = randint(8, 15)
        frames = list()
        for frame in ASSETS_FLAMES:
            frames.append(pg.transform.scale(frame, (self.width, int(width * frame.get_height() / frame.get_width()))))
        super(Flames, self).__init__(game, frame_per_image, frames, offset=randint(0, 6))

        self.rect.center = (self.x, self.y)
