"""Settings for inventory"""
from logger import logger

ARMOR_SLOTS = ['head', 'chest', 'legs', 'feet']
WEAPON_SLOTS = ['weapon']
SPELL_SLOTS = ['spell']

INVENTORY_TILESIZE = 48
INVENTORY_SLOT_GAP = 2

logger.debug("il faut mettre la case de spell que si c'est un wizard")
EQUIPMENT_COLS = len(WEAPON_SLOTS)
EQUIPMENT_ROWS = len(ARMOR_SLOTS) + len(SPELL_SLOTS)

ACTIONS = {
    "sell": "sell",
    "equip": "equip",
    "unequip": "unequip",
    "use": "use",
    "throw": "throw",
}

MENU_DATA = ["inventory"] + list(ACTIONS.values())
