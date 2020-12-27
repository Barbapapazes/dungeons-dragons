"""Used to manage the turn based gameplay"""


from config.sprites import SCOPE_HAND
from sprites.enemy import Enemy
from sprites.player import Player
from logger import logger


class TurnManager:
    """Manage the turnbased game"""

    def __init__(self, turn_number=0):
        self.players = list()
        self.enemies = list()

        self.sorted = None

        self.turn = turn_number

    def add_turn(self):
        """Add a turn"""
        self.turn += 1

    def get_characters(self):
        """Get all the characters

        Returns:
            list
        """
        if not self.sorted:
            self.sort_characters()
        return self.sorted

    def sort_characters(self):
        self.sorted = self.players + self.enemies

        logger.debug(
            "il faut enregistrer la configuration (depuis le save_game dans game.py) via la position des players j'imagine")

        # used to sort characters using the dexterity
        self.sorted.sort(key=get_dice)

        # used to add thief in the begining
        for character in self.sorted:
            if character.type == "thief":
                self.sorted.remove(character)
                self.sorted.insert(0, character)

    def get_relative_turn(self):
        """Get the relative turn

        Returns:
            int
        """
        len_characters = len(self.get_characters())
        # logger.debug("si il n'y a plus de players, c'est game over")
        turn_to_number = self.turn % len_characters
        return turn_to_number

    def active_character(self):
        """Return the active character using the turn manager

        Returns:
            Player
        """
        return self.get_characters()[self.get_relative_turn()]

    def get_active_scope(self):
        scope = None
        if self.is_active_player():
            scope = SCOPE_HAND
            if self.active_character().weapon:
                scope = self.active_character().weapon.scope
        logger.debug(scope)
        return scope

    def get_active_weapon(self):
        return self.active_character().weapon

    def get_active_weapon_type(self):
        if self.get_active_weapon() is None:
            return "hand"
        return self.get_active_weapon().wpn_type

    def remove_health(self, damage, enemy):
        enemy.health -= damage
        self.active_character().game.logs.add_log(f"Remove {damage}, remaining {enemy.health}")
    # il faut enlever de la vie en fonction le l'arme choisi mais aussi en fonction du joueur actif, on va donc passer en paramètre le joueur sélectionner, le signaler dans le logs et on va aussi utiliser l'arme pour savoir si c'est un arc et donc faire le calcul dégresif ou si c'est une arme classique

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


def get_dice(character):
    character.throw_dice("dex")
    if not character.dice["success"]:
        # add 101 to be able to sort without using true or false
        character.dice["result"] += 101
    return character.dice["result"]
