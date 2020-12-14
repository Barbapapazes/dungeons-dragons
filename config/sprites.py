"""Define settings for the sprites"""
import os
from os import path
import pygame as pg
from config.window import HEIGHT, TILESIZE, WIDTH
from tools import strip_from_sheet as strip

pg.init()
pg.display.set_mode((WIDTH, HEIGHT))

game_folder = path.dirname('.')
assets_folder = path.join(game_folder, 'assets')
items_folder = path.join(assets_folder, "img", 'items')
sprites_folder = path.join(assets_folder, 'sprites')

# player
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 200
PLAYER_MAX_HP = 100
PLAYER_MAX_MP = 50
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)


# all items
ITEMS = {
    f.split('.png')[0]: pg.image.load(path.join(items_folder, f)).convert_alpha()
    for f in os.listdir(items_folder) if f.endswith('.png')}

# equipables
CONSUMABLE = {
    "potion red": {
        "image": ITEMS["potion_02a"],
        "price": 10,
        "weight": 2,
        "heal": 30
    }
}

WEAPONS = {
    "sword wood": {
        "image": ITEMS["sword_01a"],
        "price": 10,
        "weight": 10,
        "slot": "weapon",
        "type": "sword",
        "nb_d": 1,
        "val_d": 3,
        "scope": 2
    },
    "sword steel": {
        "image": ITEMS["sword_01c"],
        "price": 10,
        "weight": 20,
        "slot": "weapon",
        "type": "sword",
        "nb_d": 4,
        "val_d": 6,
        "scope": 3

    },
    "arc": {
        "image": ITEMS["bow_01a"],
        "weight": 15,
        "slot": "weapon",
        "type": "arc",
        "nb_d": 2,
        "val_d": 10,
        "scope": 5,
        "price": 10,

    },
    "dagger": {
        "image": ITEMS["sword_03a"],
        "price": 10,
        "weight": 5,
        "slot": "weapon",
        "type": "dagger",
        "nb_d": 7,
        "val_d": 3,
        "scope": 3,
        "price": 10,

    }
}

ARMOR = {
    "steel helmet": {
        "image": ITEMS["helmet_01b"],
        "price": 10,
        "weight": 10,
        "armor": 20,
        "slot": 'head'
    },
    "gold helmet": {
        "image": ITEMS["helmet_01d"],
        "price": 10,
        "weight": 15,
        "armor": 30,
        "slot": "head"
    },
    "steel chest": {
        "image": ITEMS["armor_01a"],
        "price": 10,
        "weight": 20,
        "armor": 40,
        "slot": "chest"
    },
    "gold chest": {
        "image": ITEMS["armor_01d"],
        "price": 10,
        "weight": 30,
        "armor": 70,
        "slot": "chest"
    }
}


WEAPONS_COLS = 5
WEAPONS_ROWS = len(WEAPONS.keys()) // WEAPONS_COLS + 1

ARMOR_COLS = WEAPONS_COLS
ARMOR_ROWS = len(ARMOR.keys()) // WEAPONS_COLS + 1

CONSUMABLE_COLS = WEAPONS_COLS
CONSUMABLE_ROWS = len(CONSUMABLE.keys()) // WEAPONS_COLS + 1

# Character
WIDTH_CHARACTER = 150
HEIGHT_CHARACTER = 150
USABLE_POINTS = 12

# Items
BOB_RANGE = 15
BOB_SPEED = 0.4
ASSETS_ITEMS = {
    "key": pg.image.load(path.join(sprites_folder, 'items', "key_silver.png"))
}


# Heros
TYPES = ["wizard", "soldier", "thief"]
DIRECTIONS = ["front", "back", "left", "right"]

ASSETS_SPRITES = {_type: {key: [pg.transform.scale(pg.image.load(path.join(
    sprites_folder, _type, key, f"{i}.png")), (TILESIZE, TILESIZE)) for i in range(3)] for key in DIRECTIONS} for _type in TYPES}

ASSETS_DOOR = [pg.transform.scale(pg.image.load(path.join(
    sprites_folder, "door", "opening", f"{i}.png")), (TILESIZE, TILESIZE)) for i in range(14)]
