"""Settings dor shop"""


SHOP_TILESIZE = 48
SHOP_SLOT_GAP = 2

SHOP_CATEGORIES = ['consumables', 'weapons', 'armor']

ACTIONS = {
    "buy": "buy",
    "buy_equip": "buy and equip",
    "buy_use": "buy and use",
    "sell": "sell",
    "equip": "equip",
    "unequip": "unequip",
    "use": "use",
}

MENU_DATA = ["shop"] + list(ACTIONS.values())
