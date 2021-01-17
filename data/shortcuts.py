"""Dictionnary with all shortcuts"""
import pygame as pg

SHORTCUTS_DEFAULT = {
    "window": {
        "fps": {"keys": [False, False, pg.K_EQUALS], "help": "Toggle the fps counter"},
        "escape": {"keys": [False, False, pg.K_ESCAPE], "help": "Used to exit a menu"},
        "music": {"keys": [True, False, pg.K_m], "help": "Used to open the music option pane"}
    },
    "game": {
        "inventory": {"keys": [False, False, pg.K_i], "help": "Toggle the inventory"},
        "menu": {"keys": [False, False, pg.K_m], "help": "Toggle the sub-state"},
        "view": {"keys": [False, False, pg.K_v], "help": "Used to change the player view"},
        "playable": {"keys": [False, False, pg.K_c], "help": "Used to change the active player"},
        "map": {"keys": [False, False, pg.K_u], "help": "Used to show a big map"},
        "draw": {"keys": [False, False, pg.K_r], "help": "Used to draw on the big map"},
        "erase": {"keys": [False, False, pg.K_e], "help": "Used to erase drawing on the big map"},
        "new canvas": {"keys": [False, False, pg.K_n], "help": "Restore the canvas of the big map"},
        "console": {"keys": [False, False, pg.K_k], "help": "Toggle the console"},
        "save": {"keys": [True, False, pg.K_s], "help": "Save the canvas"},
        "attack": {"keys": [False, False, pg.K_1], "help": "Start an attack action"},
        "move": {"keys": [False, False, pg.K_2], "help": "Start a move action"},
        "spell": {"keys": [False, False, pg.K_3], "help": "Start a spell action"},
        "validate": {"keys": [False, False, pg.K_RETURN], "help": "Validate an action"},
        "environment": {"keys": [False, False, pg.K_SPACE], "help": "Interact with the environment"},
        "return": {"keys": [False, False, pg.K_ESCAPE], "help": "Quit a sub-state"},
    },
    "online game": {
        "shoot": {"keys": [False, False, pg.K_SPACE], "help": "Shoot"},
    },
    "character creation": {
        "class_r": {"keys": [False, False, pg.K_RIGHT], "help": "Used to choose the next class"},
        "class_l": {"keys": [False, False, pg.K_LEFT], "help": "Used to choose the previous class"},
    },
    "player": {
        "up": {"keys": [False, False, pg.K_z], "help": "Move the player forward"},
        "down": {"keys": [False, False, pg.K_s], "help": "Move the player backward"},
        "left": {"keys": [False, False, pg.K_q], "help": "Move the player to the left"},
        "right": {"keys": [False, False, pg.K_d], "help": "Move the player to the right"},
    },
    "shortcuts": {
        "show": {"keys": [True, False, pg.K_k], "help": "Toggle the shortcuts pane"},
        "save": {"keys": [False, True, pg.K_s], "help": "Used to save shortcuts"},
        "reset": {"keys": [False, True, pg.K_r], "help": "Used to reset to default shortcuts"},
    },
}

CUSTOM_SHORTCUTS_FILENAME = 'custom_shortcuts.json'
