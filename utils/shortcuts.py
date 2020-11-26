import pygame as pg
import json
import os
from os import path
from logger import logger
from data.shortcuts import SHORTCUTS_DEFAULT, CUSTOM_SHORTCUTS_FILENAME


def key_for(keys, event):
    """Check if keys are pressed

        Args:
            keys (List) : [ctrl, alt, key]
            event (Event)

    Returns:
        Boolean
        """
    mods = pg.key.get_mods()

    key = bool(not mods & pg.KMOD_ALT and not keys[1] and not mods &
               pg.KMOD_CTRL and not keys[0] and event.key == keys[2])

    ctrl = bool(not mods & pg.KMOD_ALT and not keys[1] and mods & pg.KMOD_CTRL and keys[0] and event.key == keys[2])

    alt = bool(mods & pg.KMOD_ALT and keys[1] and not mods & pg.KMOD_CTRL and not keys[0] and event.key == keys[2])

    if bool(mods & pg.KMOD_ALT) and bool(mods & pg.KMOD_CTRL):
        return event.key == keys[2] and keys[0] and keys[1]
    else:
        return key or ctrl or alt


def load_shortcuts():
    """Load shortcuts depending if there is a custom file

    Returns:
        object
    """
    game_folder = path.dirname('.')
    assets_folder = path.join(game_folder, 'assets')
    saved_shortcuts = path.join(assets_folder, 'saved_shortcuts')

    shortcuts = [f for f in os.listdir(saved_shortcuts) if path.isfile(
        path.join(saved_shortcuts, f)) and f.endswith('json')]
    if len(shortcuts) == 0:
        shortcuts = SHORTCUTS_DEFAULT
    else:
        with open(path.join(saved_shortcuts, CUSTOM_SHORTCUTS_FILENAME), 'r') as _f:
            shortcuts = json.load(_f)
    data = {"shortcuts": shortcuts}
    logger.info("Shortcuts loaded in screens: %s", data)
    return data
