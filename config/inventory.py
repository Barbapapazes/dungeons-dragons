"""Settings for inventory"""


ARMOR_SLOTS = ['head', 'chest', 'legs', 'feet']
WEAPON_SLOTS = ['weapon']

INVENTORY_TILESIZE = 48
INVENTORY_SLOT_GAP = 2

EQUIPMENT_COLS = len(WEAPON_SLOTS)
EQUIPMENT_ROWS = len(ARMOR_SLOTS)

ACTIONS = {
    "sell": "sell",
    "equip": "equip",
    "unequip": "unequip",
    "use": "use",
    "throw": "throw",
}

MENU_DATA = ["inventory"] + list(ACTIONS.values())
