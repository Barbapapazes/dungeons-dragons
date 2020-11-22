"""Define settings for the sprites"""

# player
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 200
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
        "type": "sword",
        "nb_d": 1,
        "val_d": 3,
        "scope":2
    },
    "sword steel": {
        "image": "sword.png",
        "weight": 20,
        "slot": "weapon",
        "type": "sword",
        "nb_d": 4,
        "val_d": 6,
        "scope":3

    },
    "arc": {
        "image": "arc.png",
        "weight": 15,
        "slot": "weapon",
        "type": "arc",
        "nb_d": 2,
        "val_d": 10,
        "scope":5

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
