"""Define settings for the sprites"""

# player
from inventory.inventory import Consumable


PLAYER_SPEED = 150


CONSUMABLE = {
    "potion red": {
        "image": "potionRed.png",
        "weight": 2,
        "heal": 30
    }
}

WEAPONS = {
    "sword": {
        "image": "sword.png",
        "weight": 20,
        "slot": "weapon"
    }
}

ARMOR = {
    "helmest": {
        "image": "helmest.png",
        "weight": 10,
        "armor": 20,
        "type": "head"
    }
}
