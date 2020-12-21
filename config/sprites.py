"""Define settings for the sprites"""
import os
from os import path
import pygame as pg
from config.window import HEIGHT, TILESIZE, WIDTH
from tools import strip_from_sheet as strip
from itertools import cycle

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
    f.split('.png')[0]: pg.image.load(path.join(items_folder, f))
    for f in os.listdir(items_folder) if f.endswith('.png')}

# OBJECTS = ['armor', '']
# SIZES = ['small', 'medium', 'large']
# ajouter dans la doc la création de la carte

# equipables
CONSUMABLE = {
    "potion red": {
        "image": ITEMS["potion_02a"],
        "image_name": "potion_02a",
        "price": 10,
        "weight": 2,
        "heal": 30
    }
}

WEAPONS = {
    "sword wood": {
        "image": ITEMS["sword_01a"],  # on peut enlerver ce champs là
        "image_name": "sword_01a",
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
        "image_name": "sword_01c",
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
        "image_name": "bow_01a",
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
        "image_name": "sword_03a",
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

ARMOR = {  # on va utiliser ses champs là et faire des .keys pour la création depuis la map et là on va mettre des randints et pour l'attribution au marchant, on va en prendre entre 1 et 5 aléatoires
    "bronze_helmet_small": {
        "image_name": "helmet_01a",
        "price": 10,
        "weight": 10,
        "shield": 20,
        "slot": 'head',
        "object_type": "armor"
    },
    "steal_helmet_small": {
        "image_name": "helmet_01b",
        "price": 10,
        "weight": 10,
        "shield": 20,
        "slot": 'head',
        "object_type": "armor"
    },
    "sapphire_helmet_small": {
        "image_name": "helmet_01c",
        "price": 10,
        "weight": 10,
        "shield": 20,
        "slot": 'head',
        "object_type": "armor"
    },
    "gold_helmet_small": {
        "image_name": "helmet_01d",
        "price": 10,
        "weight": 15,
        "shield": 30,
        "slot": "head",
        "object_type": "armor"
    },
    "ruby_helmet_small": {
        "image_name": "helmet_01e",
        "price": 10,
        "weight": 15,
        "shield": 30,
        "slot": "head",
        "object_type": "armor"
    },
    "bronze_helmet_medium": {
        "image_name": "helmet_02a",
        "price": 10,
        "weight": 10,
        "shield": 20,
        "slot": 'head',
        "object_type": "armor"
    },
    "steal_helmet_medium": {
        "image_name": "helmet_02b",
        "price": 10,
        "weight": 10,
        "shield": 20,
        "slot": 'head',
        "object_type": "armor"
    },
    "sapphire_helmet_medium": {
        "image_name": "helmet_02c",
        "price": 10,
        "weight": 10,
        "shield": 20,
        "slot": 'head',
        "object_type": "armor"
    },
    "gold_helmet_medium": {
        "image_name": "helmet_02d",
        "price": 10,
        "weight": 15,
        "shield": 30,
        "slot": "head",
        "object_type": "armor"
    },
    "ruby_helmet_medium": {
        "image_name": "helmet_02e",
        "price": 10,
        "weight": 15,
        "shield": 30,
        "slot": "head",
        "object_type": "armor"
    },
    "bronze_chest_small": {
        "image_name": "armor_01a",
        "price": 10,
        "weight": 20,
        "shield": 40,
        "slot": "chest",
        "object_type": "armor"
    },
    "steal_chest_small": {
        "image_name": "armor_01b",
        "price": 10,
        "weight": 20,
        "shield": 40,
        "slot": "chest",
        "object_type": "armor"
    },
    "sapphire_chest_small": {
        "image_name": "armor_01c",
        "price": 10,
        "weight": 20,
        "shield": 40,
        "slot": "chest",
        "object_type": "armor"
    },
    "gold_chest_small": {
        "image_name": "armor_01d",
        "price": 10,
        "weight": 20,
        "shield": 40,
        "slot": "chest",
        "object_type": "armor"
    },
    "ruby_chest_small": {
        "image_name": "armor_01e",
        "price": 10,
        "weight": 30,
        "shield": 70,
        "slot": "chest",
        "object_type": "armor"
    },
    "bronze_boots_small": {
        "image_name": "boots_01a",
        "price": 10,
        "weight": 20,
        "shield": 40,
        "slot": "feet",
        "object_type": "armor"
    },
    "steal_boots_small": {
        "image_name": "boots_01b",
        "price": 10,
        "weight": 20,
        "shield": 40,
        "slot": "feet",
        "object_type": "armor"
    },
    "sapphire_boots_small": {
        "image_name": "boots_01c",
        "price": 10,
        "weight": 20,
        "shield": 40,
        "slot": "feet",
        "object_type": "armor"
    },
    "gold_boots_small": {
        "image_name": "boots_01d",
        "price": 10,
        "weight": 20,
        "shield": 40,
        "slot": "feet",
        "object_type": "armor"
    },
    "ruby_boots_small": {
        "image_name": "boots_01e",
        "price": 10,
        "weight": 30,
        "shield": 70,
        "slot": "feet",
        "object_type": "armor"
    }
}

ITEMS_PROPERTIES = ARMOR
ITEMS_NAMES = ARMOR.keys()


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

# Bounce
BOB_RANGE = 15
BOB_SPEED = 0.4


# Heros
TYPES = ["wizard", "soldier", "thief", "enemy_1"]
DIRECTIONS = ["up", "down", "left", "right", "idle"]

ASSETS_SPRITES = {
    _type: {
        key: cycle([pg.transform.scale(pg.image.load(path.join(
            sprites_folder, _type, key, f"{i}.png")), (TILESIZE, TILESIZE)) for i in range(3)]) for key in DIRECTIONS
    } for _type in TYPES
}

ASSETS_MERCHANT = [pg.image.load(path.join(sprites_folder, "merchant", f"{i}.png"))
                   for i in range(4)]

ASSETS_DOOR = [pg.transform.scale(
    pg.image.load(path.join(sprites_folder, "door", "opening", f"{i}.png")),
    (TILESIZE, TILESIZE)) for i in range(14)]

ASSETS_CHEST = [pg.transform.scale(
    pg.image.load(path.join(sprites_folder, "chest", f"{i}.png")),
    (TILESIZE, TILESIZE)) for i in range(8)]

ASSETS_FLAMES = [pg.image.load(path.join(sprites_folder, "flames", f"{i}.png"))
                 for i in range(6)]

ASSETS_CAMP_FIRE = [pg.image.load(path.join(sprites_folder, "camp_fire", "{:04d}.png".format(i)))
                    for i in range(1, 9)]

ASSETS_CHANDELIER = [pg.image.load(path.join(sprites_folder, "chandelier", "{:04d}.png".format(i)))
                     for i in range(1, 6)]

ASSETS_BOOK_OPENING = [pg.image.load(path.join(sprites_folder, "book", "opening",  f"{i}.png"))
                       for i in range(4)]
ASSETS_BOOK_NEXT = [pg.image.load(path.join(sprites_folder, "book", "next",  f"{i}.png"))
                    for i in range(5)]

ASSETS_CIRCLE = [pg.image.load(path.join(sprites_folder, "circle", "{:04d}.png".format(i)))
                 for i in range(1, 60)]
