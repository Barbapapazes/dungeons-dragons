"""Define settings for the window"""


from data.options import CUSTOM_SETTINGS_FILENAME
import json
from logger import logger
from os import path

DEFAULT_SETTINGS = {
    "width": 1024,
    "height": 768
}


def get(_type, data):
    """Used to get value for the settings file 

    Args:
        _type (string)
        data (dict)

    Returns:
        int | str
    """
    value = 0
    try:
        with open(path.join('.', 'assets', 'saved_settings', CUSTOM_SETTINGS_FILENAME), 'r') as _f:
            value = json.load(_f)[_type]
    except:
        value = data[_type]

    logger.info("Load %s : %s", _type, value)
    return value


WIDTH = get("width", DEFAULT_SETTINGS)
HEIGHT = get("height", DEFAULT_SETTINGS)


FPS = 60
TITLE = 'Donjons et Dragons'

TILESIZE = 64
