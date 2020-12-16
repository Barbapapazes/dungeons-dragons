"""Settings for the store"""


SHOP_TILESIZE = 48
SHOP_SLOT_GAP = 2

SHOP_CATEGORIES = ['consumables', 'weapons', 'armor']

ACTIONS = {
    "buy": "buy",
    "buy_equip": "buy and equip",
    "buy_use": "buy and use",
}

MENU_DATA = ["shop"] + list(ACTIONS.values())
