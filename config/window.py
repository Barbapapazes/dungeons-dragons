"""Define settings for the window"""


from data.options import CUSTOM_SETTINGS_FILENAME
import json
from os import path


def get(_type):
    """Used to get value for the settings file 

    Args:
        _type (string)

    Returns:
        int | str
    """
    value = 0
    with open(path.join('.', 'assets', 'saved_settings', CUSTOM_SETTINGS_FILENAME), 'r') as _f:
        value = json.load(_f)[_type]
    return value


WIDTH = get("width")
HEIGHT = get("height")


FPS = 60
TITLE = 'Donjons et Dragons'

TILESIZE = 64
