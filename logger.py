"""Logger"""

import logging
from colorlog import ColoredFormatter
from os import environ

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
# f_handler = logging.FileHandler('file.log')
level = logging.ERROR if environ.get('PYTHON_ENV') == "production" else logging.DEBUG

c_handler.setLevel(level)
# f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = ColoredFormatter(
    '%(asctime)s - %(log_color)s%(levelname)s%(reset)s - %(message)s',
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    })
# f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
# f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.setLevel(logging.DEBUG)
# logger.addHandler(f_handler)
