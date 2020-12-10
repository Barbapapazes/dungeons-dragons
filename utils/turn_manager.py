"""Used to manage the turn based gameplay"""


class TurnManager:
    """Manage the turnbased game"""

    def __init__(self, turn_number=0):
        self.players = list()

        self.turn = turn_number

    def add_turn(self):
        """Add a turn"""
        self.turn += 1

    def active_player(self):
        """Return the active player using the turn manager 

        Returns:
            Player
        """
        len_players = len(self.players)
        turn_to_number = self.turn % len_players
        return self.players[turn_to_number]

    def update(self):
        """Update the active player"""
        self.active_player().update()
