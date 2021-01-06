"""Define settings for the sprites"""
import os
from os import path
import pygame as pg
from config.window import HEIGHT, TILESIZE, WIDTH
from tools import strip_from_sheet as strip
from itertools import cycle
from logger import logger

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


MALUS_ARC = 2

# all items
ITEMS = {
    f.split('.png')[0]: pg.image.load(path.join(items_folder, f))
    for f in os.listdir(items_folder) if f.endswith('.png')}

# equipables
CONSUMABLE = {
    "red_potion_small": {
        "image_name": "potion_02a",
        "price": 10,
        "weight": 2,
        "heal": 30,
        "shield": 0,
        "object_type": "consumable"
    }
}
SCOPE_HAND = 3 * TILESIZE
SCOPE_SWORD = 5 * TILESIZE
SCOPE_ARC = 13 * TILESIZE
# il faut ajouter l'item type
WEAPONS = {
    "bronze_sword_small": {
        "image_name": "sword_01a",
        "price": 10,
        "weight": 10,
        "slot": "weapon",
        "type": "sword",
        "number_dice": 1,
        "dice_value": 3,
        "scope": SCOPE_SWORD,
        "object_type": "weapon"
    },
    "steal_sword_small": {
        "image_name": "sword_01b",
        "price": 10,
        "weight": 10,
        "slot": "weapon",
        "type": "sword",
        "number_dice": 1,
        "dice_value": 3,
        "scope": SCOPE_SWORD,
        "object_type": "weapon"
    },
    "sapphire_sword_small": {
        "image_name": "sword_01c",
        "price": 10,
        "weight": 10,
        "slot": "weapon",
        "type": "sword",
        "number_dice": 1,
        "dice_value": 3,
        "scope": SCOPE_SWORD,
        "object_type": "weapon"
    },
    "gold_sword_small": {
        "image_name": "sword_01d",
        "price": 10,
        "weight": 10,
        "slot": "weapon",
        "type": "sword",
        "number_dice": 1,
        "dice_value": 3,
        "scope": SCOPE_SWORD,
        "object_type": "weapon"

    },
    "ruby_sword_small": {
        "image_name": "sword_01e",
        "price": 10,
        "weight": 10,
        "slot": "weapon",
        "type": "sword",
        "number_dice": 1,
        "dice_value": 3,
        "scope": SCOPE_SWORD,
        "object_type": "weapon"
    },
    "bronze_sword_medium": {
        "image_name": "sword_02a",
        "price": 10,
        "weight": 10,
        "slot": "weapon",
        "type": "sword",
        "number_dice": 1,
        "dice_value": 3,
        "scope": SCOPE_SWORD,
        "object_type": "weapon"
    },
    "steal_sword_medium": {
        "image_name": "sword_02b",
        "price": 10,
        "weight": 10,
        "slot": "weapon",
        "type": "sword",
        "number_dice": 1,
        "dice_value": 3,
        "scope": SCOPE_SWORD,
        "object_type": "weapon"
    },
    "sapphire_sword_medium": {
        "image_name": "sword_02c",
        "price": 10,
        "weight": 10,
        "slot": "weapon",
        "type": "sword",
        "number_dice": 1,
        "dice_value": 3,
        "scope": SCOPE_SWORD,
        "object_type": "weapon"
    },
    "gold_sword_medium": {
        "image_name": "sword_02d",
        "price": 10,
        "weight": 10,
        "slot": "weapon",
        "type": "sword",
        "number_dice": 1,
        "dice_value": 3,
        "scope": SCOPE_SWORD,
        "object_type": "weapon"
    },
    "ruby_sword_medium": {
        "image_name": "sword_02e",
        "price": 10,
        "weight": 10,
        "slot": "weapon",
        "type": "sword",
        "number_dice": 1,
        "dice_value": 3,
        "scope": SCOPE_SWORD,
        "object_type": "weapon"
    },
    "bronze_arc_small": {
        "image_name": "bow_01a",
        "weight": 15,
        "slot": "weapon",
        "type": "arc",
        "number_dice": 2,
        "dice_value": 10,
        "scope": SCOPE_ARC,
        "price": 10,
        "object_type": "weapon"
    },
    "steal_arc_small": {
        "image_name": "bow_01b",
        "weight": 15,
        "slot": "weapon",
        "type": "arc",
        "number_dice": 2,
        "dice_value": 10,
        "scope": SCOPE_ARC,
        "price": 10,
        "object_type": "weapon"
    },
    "sapphire_arc_small": {
        "image_name": "bow_01c",
        "weight": 15,
        "slot": "weapon",
        "type": "arc",
        "number_dice": 2,
        "dice_value": 10,
        "scope": SCOPE_ARC,
        "price": 10,
        "object_type": "weapon"
    },
    "gold_arc_small": {
        "image_name": "bow_01d",
        "weight": 15,
        "slot": "weapon",
        "type": "arc",
        "number_dice": 2,
        "dice_value": 10,
        "scope": SCOPE_ARC,
        "price": 10,
        "object_type": "weapon"
    },
    "ruby_arc_small": {
        "image_name": "bow_01e",
        "weight": 15,
        "slot": "weapon",
        "type": "arc",
        "number_dice": 2,
        "dice_value": 10,
        "scope": SCOPE_ARC,
        "price": 10,
        "object_type": "weapon"
    },
    "bronze_arc_medium": {
        "image_name": "bow_02a",
        "weight": 15,
        "slot": "weapon",
        "type": "arc",
        "number_dice": 2,
        "dice_value": 10,
        "scope": SCOPE_ARC,
        "price": 10,
        "object_type": "weapon"
    },
    "steal_arc_medium": {
        "image_name": "bow_02b",
        "weight": 15,
        "slot": "weapon",
        "type": "arc",
        "number_dice": 2,
        "dice_value": 10,
        "scope": SCOPE_ARC,
        "price": 10,
        "object_type": "weapon"
    },
    "sapphire_arc_medium": {
        "image_name": "bow_02c",
        "weight": 15,
        "slot": "weapon",
        "type": "arc",
        "number_dice": 2,
        "dice_value": 10,
        "scope": SCOPE_ARC,
        "price": 10,
        "object_type": "weapon"
    },
    "gold_arc_medium": {
        "image_name": "bow_02d",
        "weight": 15,
        "slot": "weapon",
        "type": "arc",
        "number_dice": 2,
        "dice_value": 10,
        "scope": SCOPE_ARC,
        "price": 10,
        "object_type": "weapon"
    },
    "ruby_arc_medium": {
        "image_name": "bow_02e",
        "weight": 15,
        "slot": "weapon",
        "type": "arc",
        "number_dice": 2,
        "dice_value": 10,
        "scope": SCOPE_ARC,
        "price": 10,
        "object_type": "weapon"
    },
    "bronze_arc_large": {
        "image_name": "bow_03a",
        "weight": 15,
        "slot": "weapon",
        "type": "arc",
        "number_dice": 2,
        "dice_value": 10,
        "scope": SCOPE_ARC,
        "price": 10,
        "object_type": "weapon"
    },
    "steal_arc_large": {
        "image_name": "bow_03b",
        "weight": 15,
        "slot": "weapon",
        "type": "arc",
        "number_dice": 2,
        "dice_value": 10,
        "scope": SCOPE_ARC,
        "price": 10,
        "object_type": "weapon"
    },
    "sapphire_arc_large": {
        "image_name": "bow_03c",
        "weight": 15,
        "slot": "weapon",
        "type": "arc",
        "number_dice": 2,
        "dice_value": 10,
        "scope": SCOPE_ARC,
        "price": 10,
        "object_type": "weapon"
    },
    "gold_arc_large": {
        "image_name": "bow_03d",
        "weight": 15,
        "slot": "weapon",
        "type": "arc",
        "number_dice": 2,
        "dice_value": 10,
        "scope": SCOPE_ARC,
        "price": 10,
        "object_type": "weapon"
    },
    "ruby_arc_large": {
        "image_name": "bow_03e",
        "weight": 15,
        "slot": "weapon",
        "type": "arc",
        "number_dice": 2,
        "dice_value": 10,
        "scope": SCOPE_ARC,
        "price": 10,
        "object_type": "weapon"
    },
    "bronze_dagger_small": {
        "image_name": "sword_03a",
        "weight": 10,
        "slot": "weapon",
        "type": "dagger",
        "number_dice": 1,
        "dice_value": 3,
        "scope": SCOPE_SWORD,
        "price": 10,
        "object_type": "weapon",
    },
    "steal_dagger_small": {
        "image_name": "sword_03b",
        "weight": 10,
        "slot": "weapon",
        "type": "dagger",
        "number_dice": 1,
        "dice_value": 3,
        "scope": SCOPE_SWORD,
        "price": 10,
        "object_type": "weapon"
    },
    "sapphire_dagger_small": {
        "image_name": "sword_03c",
        "weight": 10,
        "slot": "weapon",
        "type": "dagger",
        "number_dice": 1,
        "dice_value": 3,
        "scope": SCOPE_SWORD,
        "price": 10,
        "object_type": "weapon"
    },
    "gold_dagger_small": {
        "image_name": "sword_03d",
        "weight": 10,
        "slot": "weapon",
        "type": "dagger",
        "number_dice": 1,
        "dice_value": 3,
        "scope": SCOPE_SWORD,
        "price": 10,
        "object_type": "weapon"
    },
    "ruby_dagger_small": {
        "image_name": "sword_03e",
        "weight": 10,
        "slot": "weapon",
        "type": "dagger",
        "number_dice": 1,
        "dice_value": 3,
        "scope": SCOPE_SWORD,
        "price": 10,
        "object_type": "weapon"
    },
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

SPELLS = {
    "fire_ball": {
        "image_name": "fireBall",
        "type": "heal",
        "scope": 3 * TILESIZE,
        "slot": "spell",
        "object_type": "spell",
        "time_to_live": 2,
        "number_dice": 2,
        "dice_value": 10
    }
}

OTHERS = {
    "bronze_key_small": {
        "object_type": "other",
        "image_name": "key_01a",
        "weight": 10,
        "price": 10
    }
}

ITEMS_PROPERTIES = ARMOR | WEAPONS | SPELLS | OTHERS
ITEMS_NAMES = list(ARMOR.keys()) + list(WEAPONS.keys()) + list(SPELLS.keys()) + list(OTHERS.keys())

WEAPONS_COLS = 5

ARMOR_COLS = WEAPONS_COLS

CONSUMABLE_COLS = WEAPONS_COLS

# Character
WIDTH_CHARACTER = 300
HEIGHT_CHARACTER =300
USABLE_POINTS = 100

# Bounce
BOB_RANGE = 15
BOB_SPEED = 0.4


# Heros
TYPES = ["wizard", "soldier", "thief", "skeleton_F", "skeleton_R", "skeleton_W", "phantom_F", "phantom_R", "phantom_W", "goblin_F", "goblin_R", "goblin_W", "boss", "mini_boss"]
DIRECTIONS = ["up", "down", "left", "right", "idle"]

ASSETS_SPRITES = {
    _type: {
        key: cycle([pg.transform.scale(pg.image.load(path.join(
            sprites_folder, _type, key, f"{i}.png")), (TILESIZE, TILESIZE)) for i in range(3)]) for key in DIRECTIONS
    } for _type in TYPES
}

ASSETS_FIRE_BALL = [pg.image.load(path.join(sprites_folder, "effects_zone", "fire_ball",
                                            "{:04d}.png".format(i))) for i in range(1, 11)]

ASSETS_HEAL = [pg.image.load(path.join(sprites_folder, "effects_zone", "heal",
                                       "{:04d}.png".format(i))) for i in range(1, 60)]

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
