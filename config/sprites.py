"""Define settings for the sprites"""

# player
PLAYER_SPEED = 150
PLAYER_MAX_HP = 100

#  ajouter les charastéristiques

# equipables
CONSUMABLE = {
    "potion red": {
        "image": "potionRed.png",
        "weight": 2,
        "heal": 30
    }
}

WEAPONS = {
    "sword wood": {
        "image": "swordWood.png",
        "weight": 10,
        "slot": "weapon",
        "type": "sword"
    },
    "sword steel": {
        "image": "sword.png",
        "weight": 20,
        "slot": "weapon",
        "type": "sword"

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
