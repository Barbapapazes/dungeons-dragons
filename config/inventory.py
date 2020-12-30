"""Settings for inventory"""
from logger import logger

ARMOR_SLOTS = ['head', 'chest', 'legs', 'feet']
WEAPON_SLOTS = ['weapon']
SPELL_SLOTS = ['spell']

INVENTORY_TILESIZE = 48
INVENTORY_SLOT_GAP = 2

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
