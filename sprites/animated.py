"""Used to create a animated sprite"""

from random import randint
from collections import deque
import pygame as pg
from logger import logger
from config.sprites import ASSETS_CAMP_FIRE, ASSETS_CHANDELIER, ASSETS_CIRCLE, ASSETS_FLAMES
from config.sprites import ASSETS_FLAMES, ASSETS_BOOK_OPENING

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


class CampFire(Animated):
    """Used to create a camp fire"""

    def __init__(self, game, x, y, width):
        self.x = x
        self.y = y
        self.width = width

        frame_per_image = randint(12, 18)
        frames = list()
        for frame in ASSETS_CAMP_FIRE:
            frames.append(pg.transform.scale(frame, (self.width, int(width * frame.get_height() / frame.get_width()))))
        super(CampFire, self).__init__(game, frame_per_image, frames, offset=randint(0, 6))

        self.rect.center = (self.x, self.y)


class Chandelier(Animated):
    """Used to create a camp fire"""

    def __init__(self, game, x, y, width):
        self.x = x
        self.y = y
        self.width = width

        frame_per_image = randint(12, 18)
        frames = list()
        for frame in ASSETS_CHANDELIER:
            frames.append(pg.transform.scale(frame, (self.width, int(width * frame.get_height() / frame.get_width()))))
        super(Chandelier, self).__init__(game, frame_per_image, frames, offset=randint(0, 6))

        self.rect.center = (self.x, self.y + self.frames[0].get_height() // 2)


class Book(Animated):
    """Used to create a book"""

    def __init__(self, game, x, y, width):
        self.x = x
        self.y = y
        self.width = width

        frame_per_image = 6
        frames = list()
        for frame in ASSETS_BOOK_OPENING:
            frames.append(pg.transform.scale(frame, (self.width, int(
                self.width * frame.get_height() / frame.get_width()))))
        super(Book, self).__init__(game, frame_per_image, frames)

        self.rect.center = (self.x, self.y)

    def set_frames(self, frames):
        tmp_frames = list()
        for frame in frames:
            tmp_frames.append(pg.transform.scale(frame, (self.width, int(
                self.width * frame.get_height() / frame.get_width()))))
        self.frames = tmp_frames
        self.frame_total = (len(frames) - 1) * self.frame_per_image
        self.frame_count = 0


class Circle(Animated):
    """Used to create an circle for player range"""

    def __init__(self, game, x, y, width):
        self.x = x
        self.y = y
        self.width = width

        frame_per_image = 6
        frames = list()

        for frame in ASSETS_CIRCLE:
            frame.set_colorkey((50, 50, 50))
            frames.append(frame)
        super(Circle, self).__init__(game, frame_per_image, frames)

        self.rect.center = (self.x, self.y)

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.rect.center = pos

    def set_width(self, width):
        if self.width != width:
            self.width = width
            tmp_frames = list()
            for frame in self.frames:
                frame = pg.transform.scale(frame, (width, width))
                frame.set_colorkey((50, 50, 50))
                tmp_frames.append(frame)
            self.frames = tmp_frames
            self.rect = self.frames[0].get_rect()
