"""Dictionnary with all shortcuts"""
import pygame as pg

SHORTCUTS_DEFAULT = {
    "window": {
        "save": {"keys": [True, False, pg.K_s], "help": "This is the help"},
        "fps": {"keys": [False, False, pg.K_EQUALS], "help": "this is another help"}
    },
    "game": {
        "up": {"keys": [False, False, pg.K_z], "help": "this is another help"},
        "down": {"keys": [False, False, pg.K_s], "help": "this is another help"},
        " turn left": {"keys": [False, False, pg.K_q], "help": "this is another help"},
        "turn right": {"keys": [False, False, pg.K_d], "help": "this is another help"}
    },
    "shortcuts": {
        "show": {"keys": [True, False, pg.K_k], "help": "this is another help"},
    },
}

CUSTOM_SHORTCUTS_FILENAME = 'custom_shortcuts.json'
