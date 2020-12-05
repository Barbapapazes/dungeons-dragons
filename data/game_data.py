"""Create game data for a game instance"""


def create_game_data():
    """Create game data"""
    return {
        "count": 0,
        "hero": {
            "class": "",
            "characteristics": {
                "str": 0,
                "dex": 0,
                "con": 0,
                "int": 0,
                "wis": 0,
                "cha": 0
            }
        },
    }
