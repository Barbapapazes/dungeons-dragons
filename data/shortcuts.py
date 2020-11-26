"""Dictionnary with all shortcuts"""
import pygame as pg

SHORTCUTS_DEFAULT = {
    "window": {
        "save": {"keys": [True, False, pg.K_s], "help": "Used to saved the game"},
        "fps": {"keys": [False, False, pg.K_EQUALS], "help": "Toggle the fps counter"}
    },
    "load_game":  {
        "up": {"keys": [False, False, pg.K_UP], "help": "Used to select a game"},
        "down": {"keys": [False, False, pg.K_DOWN], "help": "Used to select a game"},
        "enter": {"keys": [False, False, pg.K_RETURN], "help": "Used to load a game"},
        "new game": {"keys": [False, False, pg.K_SPACE], "help": "Used to create a new game"}
    },
    "game": {
        "inventory": {"keys": [False, False, pg.K_i], "help": "Toggle the inventory"},
        "menu": {"keys": [False, False, pg.K_m], "help": "Toggle the sub-state"}
    },
    "player": {
        "up": {"keys": [False, False, pg.K_z], "help": "Move the player forward"},
        "down": {"keys": [False, False, pg.K_s], "help": "Move the player backward"},
        "left": {"keys": [False, False, pg.K_q], "help": "Turn the player to the left"},
        "right": {"keys": [False, False, pg.K_d], "help": "Turn the player to the right"},
    },
    "shortcuts": {
        "show": {"keys": [True, False, pg.K_k], "help": "Toggle the shortcuts pane"},
    },
}

CUSTOM_SHORTCUTS_FILENAME = 'custom_shortcuts.json'
