"""Settings for the store"""


# store
STORE_ACTIONS = {
    "get": "get",
    "get_equip": "get and equip",
    "get_use": "get and use",
}
STORE_MENU = ["store"] + list(STORE_ACTIONS.values())

STORE_TILESIZE = 48
STORE_SLOT_GAP = 2

STORE_CATEGORIES = ['consumables', 'weapons', 'armor']

SHOP_ACTIONS = {
    "buy": "buy",
    "buy_equip": "buy and equip",
    "buy_use": "buy and use",
}

SHOP_MENU = ["shop"] + list(SHOP_ACTIONS.values())
