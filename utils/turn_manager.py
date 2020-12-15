"""Used to manage the turn based gameplay"""


from sprites.enemy import Enemy
from sprites.player import Player
from logger import logger


class TurnManager:
    """Manage the turnbased game"""

    def __init__(self, turn_number=0):
        self.players = list()
        self.enemy = list()

        self.turn = turn_number

    def add_turn(self):
        """Add a turn"""
        self.turn += 1

    def get_characters(self):
        """Get all the characters

        Returns:
            list
        """
        return self.players + self.enemy

    def get_relative_turn(self):
        """Get the relative turn

        Returns:
            int
        """
        len_characters = len(self.get_characters())
        turn_to_number = self.turn % len_characters
        return turn_to_number

    def active_characters(self):
        """Return the active character using the turn manager

        Returns:
            Player
        """
        return self.get_characters()[self.get_relative_turn()]

    def is_active_player(self):
        return isinstance(self.active_characters(), Player)

    def is_active_enemy(self):
        return isinstance(self.active_characters(), Enemy)

    def update(self):
        if self.is_active_player():
            self.active_characters().update()
        if self.is_active_enemy():
            self.active_characters().update()

            # mettre la logique de l'enemy ici
