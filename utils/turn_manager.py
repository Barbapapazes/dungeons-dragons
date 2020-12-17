"""Used to manage the turn based gameplay"""


from sprites.enemy import Enemy
from sprites.player import Player
from logger import logger


class TurnManager:
    """Manage the turnbased game"""

    def __init__(self, turn_number=0):
        self.players = list()
        self.enemies = list()

        self.turn = turn_number

    def add_turn(self):
        """Add a turn"""
        self.turn += 1

    def get_characters(self):
        """Get all the characters

        Returns:
            list
        """
        return self.players + self.enemies

    def get_relative_turn(self):
        """Get the relative turn

        Returns:
            int
        """
        len_characters = len(self.get_characters())
        # logger.debug("si il n'y a plus de partie, c'est game over")
        turn_to_number = self.turn % len_characters
        return turn_to_number

    def active_character(self):
        """Return the active character using the turn manager

        Returns:
            Player
        """
        return self.get_characters()[self.get_relative_turn()]

    def is_active_player(self):
        return isinstance(self.active_character(), Player)

    def is_active_enemy(self):
        return isinstance(self.active_character(), Enemy)

    def update(self):
        if self.is_active_player():
            self.active_character().update()
        if self.is_active_enemy():
            self.active_character().update()

            # mettre la logique de l'enemy ici
    def get_pos_player(self):
        list_pos = 0
        for character in self.get_characters():
            if self.active_character() == character:
                break
            elif isinstance(character, Player):
                list_pos += 1
        return list_pos
