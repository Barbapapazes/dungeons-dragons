"""Dictionnary with all shortcuts"""
import pygame as pg

SHORTCUTS_DEFAULT = {
    "window": {
        "save": {"keys": [True, False, pg.K_s], "help": "This is the help"},
        "fps": {"keys": [False, False, pg.K_EQUALS], "help": "this is another help"}
    },
    "load_game":  {
        "up": {"keys": [False, False, pg.K_UP], "help": "Permet de sélectionner une partie"},
        "down": {"keys": [False, False, pg.K_DOWN], "help": "Permet de sélectionner une partie"},
        "enter": {"keys": [False, False, pg.K_RETURN], "help": "Permet de charger une partie"},
        "new game": {"keys": [False, False, pg.K_k], "help": "Permet de créer une nouvelle partie"}
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
        "show": {"keys": [True, False, pg.K_k], "help": "this is another help"},
    },
}

CUSTOM_SHORTCUTS_FILENAME = 'custom_shortcuts.json'
