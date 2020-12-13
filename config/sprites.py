"""Define settings for the sprites"""
from config.window import TILESIZE
import pygame as pg
from os import path

game_folder = path.dirname('.')
assets_folder = path.join(game_folder, 'assets')
sprites_folder = path.join(assets_folder, 'sprites')

# player
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 200
PLAYER_MAX_HP = 100
PLAYER_MAX_MP = 50
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)


#  ajouter les charastéristiques

# equipables
CONSUMABLE = {
    "potion red": {
        "image": "potionRed.png",
        "price": 10,
        "weight": 2,
        "heal": 30
    }
}

WEAPONS = {
    "sword wood": {
        "image": "swordWood.png",
        "price": 10,
        "weight": 10,
        "slot": "weapon",
        "type": "sword",
        "nb_d": 1,
        "val_d": 3,
        "scope": 2
    },
    "sword steel": {
        "image": "sword.png",
        "price": 10,
        "weight": 20,
        "slot": "weapon",
        "type": "sword",
        "nb_d": 4,
        "val_d": 6,
        "scope": 3

    },
    "arc": {
        "image": "arc.png",
        "weight": 15,
        "slot": "weapon",
        "type": "arc",
        "nb_d": 2,
        "val_d": 10,
        "scope": 5,
        "price": 10,

    },
    "dagger": {
        "image": "upg_dagger.png",
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
        "image": "helmet.png",
        "price": 10,
        "weight": 10,
        "armor": 20,
        "slot": 'head'
    },
    "gold helmet": {
        "image": "upg_helmet.png",
        "price": 10,
        "weight": 15,
        "armor": 30,
        "slot": "head"
    },

    "steel chest": {
        "image": "chest.png",
        "price": 10,
        "weight": 20,
        "armor": 40,
        "slot": "chest"
    },
    "gold chest": {
        "image": "upg_chest.png",
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

TYPES = ["wizard", "soldier", "thief"]
DIRECTIONS = ["front", "back", "left", "right"]
ASSETS_SPRITES = {_type: {key: [pg.transform.scale(pg.image.load(path.join(
    sprites_folder, _type, key, f"{i}.png")), (TILESIZE, TILESIZE)) for i in range(3)] for key in DIRECTIONS} for _type in TYPES}
