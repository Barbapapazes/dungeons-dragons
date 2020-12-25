"""Define settings for the screens"""
import os
from os import path
import pygame as pg

game_folder = path.dirname('.')
assets_folder = path.join(game_folder, 'assets')
img_folder = path.join(assets_folder, "img")

# screens
LOAD_GAME = 'load_game'
MENU = 'menu'
GAME = 'game'
CREDITS = 'credits'
SHORTCUTS = 'shortcuts'
CHARACTER_CREATION = "character_creation"
OPTIONS = "options"
NEW_GAME = "new_game"
INTRODUCTION = "introduction"
CHOOSE_MAP = "choose_map"

# states
TRANSITION_IN = 'transition in'
TRANSITION_OUT = 'transition out'

# backgrounds
BACKGROUND_MENU = [pg.image.load(path.join(img_folder, "menu", f"{i}.png"))
                   for i in range(15)]

BACKGROUND_CREDITS = [pg.image.load(path.join(img_folder, "credits", "{:04d}.png".format(i)))
                      for i in range(1, 9)]

BACKGROUND_INTRODUCTION = [pg.image.load(path.join(img_folder, "introduction", "{:04d}.png".format(i)))
                           for i in range(1, 10)]
