"""Define a spell"""

from random import randint
import pygame as pg
from config.sprites import ASSETS_FIRE_BALL, ASSETS_HEAL
from config.window import TILESIZE
from logger import logger

default_fn = lambda *args: None


class EffectsZone(pg.sprite.Sprite):
    """Create a effect zone"""

    def __init__(self, game, x, y, _type, time_to_live, number_dice, dice_value):
        self.groups = game.all_sprites, game.effects_zones
        super(EffectsZone, self).__init__(self.groups)

        self.game = game
        self.x = x
        self.y = y
        self.type = _type
        self.time_to_live = time_to_live
        self.number_dice = number_dice
        self.dice_value = dice_value

        frames = list()
        raw_frames = ASSETS_FIRE_BALL if _type == "attack" else ASSETS_HEAL
        for frame in raw_frames:
            frame = pg.transform.scale(frame, (TILESIZE, int(TILESIZE * frame.get_height() / frame.get_width())))
            if _type == "heal":
                frame.set_colorkey((1, 1, 1))
            frames.append(frame)

        self.frames = frames
        self.image = frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.frame_per_image = 12
        self.frame_total = (len(frames) - 1) * 12
        self.frame_count = 0

    def update(self, fn=default_fn, *args):
        """Update the sprite"""
        self.frame_count += 1
        if self.frame_count > self.frame_total + 0:
            self.frame_count = 0
            fn(*args)
        else:
            self.image = self.frames[self.frame_count // self.frame_per_image]

    def get_dice_value(self):
        """Get the dice value after the throw"""
        value = 0
        for _ in range(self.number_dice):
            value += randint(1, self.dice_value)
        return value

    def check_time_to_live(self):
        """Check and update the time to live of the effects zone"""
        self.time_to_live -= 1
        logger.debug(self.time_to_live)
        if self.time_to_live == 0:
            self.kill()
