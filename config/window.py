"""Define settings for the window"""


from data.options import CUSTOM_SETTINGS_FILENAME
import json
from logger import logger
from os import path

default_settings = {
    "width": 1024,
    "height": 768
}


def get(_type):
    """Used to get value for the settings file 

    Args:
        _type (string)

    Returns:
        int | str
    """
    value = 0
    try:
        with open(path.join('.', 'assets', 'saved_settings', CUSTOM_SETTINGS_FILENAME), 'r') as _f:
            value = json.load(_f)[_type]
    except:
        value = default_settings[_type]

    logger.info("Load %s : %s", _type, value)
    return value


WIDTH = get("width")
HEIGHT = get("height")


FPS = 60
TITLE = 'Donjons et Dragons'

TILESIZE = 64
