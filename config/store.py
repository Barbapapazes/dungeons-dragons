"""Settings for the store"""
import pygame as pg
from os import path

game_folder = path.dirname('.')
assets_folder = path.join(game_folder, 'assets')
img_folfer = path.join(assets_folder, 'img')

# store
STORE_ACTIONS = {
    "get": "get",
    "get_equip": "get and equip",
    "get_use": "get and use",
}
STORE_MENU = ["store"] + list(STORE_ACTIONS.values())

STORE_TILESIZE = 48
STORE_SLOT_GAP = 2

STORE_CATEGORIES = ['consumables', 'weapons', 'armor']

STORE_BG = pg.image.load(path.join(img_folfer, 'store', 'background.png'))

# shop
SHOP_ACTIONS = {
    "buy": "buy",
    "buy_equip": "buy and equip",
    "buy_use": "buy and use",
}

SHOP_MENU = ["shop"] + list(SHOP_ACTIONS.values())
