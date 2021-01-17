"""Utils function for music"""
import json
import os
from os import path

from data.music_data import CUSTOM_MUSIC_FILENAME, MUSIC_DEFAULT


def load_music():
    """Load music depending if there is a custom file

    Returns:
        object
    """
    game_folder = path.dirname('.')
    assets_folder = path.join(game_folder, 'assets')
    saved_music = path.join(assets_folder, 'saved_music')

    shortcuts = [f for f in os.listdir(saved_music) if path.isfile(
        path.join(saved_music, f)) and f.endswith('json')]
    if len(shortcuts) == 0:
        shortcuts = MUSIC_DEFAULT
    else:
        with open(path.join(saved_music, CUSTOM_MUSIC_FILENAME), 'r') as _f:
            shortcuts = json.load(_f)
    data = {"music": shortcuts}
    return data
