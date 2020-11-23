"""Dictionnary with all shortcuts"""
import pygame as pg

SHORTCUTS_DEFAULT = {
    "window": {
        "save": [True, False, pg.K_s],
        "fps": [False, False, pg.K_EQUALS]
    },
    "save a game": [False, False, 107],
    "other": [False, True, 108]
}

CUSTOM_SHORTCUTS_FILENAME = 'custom_shortcuts.json'
