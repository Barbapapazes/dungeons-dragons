"""Create tools"""

from random import randint
import pygame as pg
from logger import logger


def strip_from_sheet(sheet, start, size, columns, rows=1):
    """
    Strips individual frames from a sprite sheet given a start location,
    sprite size, and number of columns and rows.
    """
    frames = []
    for j in range(rows):
        for i in range(columns):
            location = (start[0] + size[0] * i, start[1] + size[1] * j)
            frames.append(sheet.subsurface(pg.Rect(location, size)))
    return frames


def trow_dice(base_value, mod=0, value_dice=100):
    """Throw a dice

    Args:
        base_value (int)
        mod (int, optional) Defaults to 0.
        value_dice (int, optional) Defaults to 100.

    Returns:
        bool: success if the result of the dice is under le base value plus the mod
    """
    result_dice = randint(0, value_dice)
    logger.info("Result dice : %d / %d (must be under %s to success)", result_dice, value_dice, base_value + mod)

    return result_dice <= base_value + mod
