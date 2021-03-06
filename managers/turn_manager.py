"""Used to manage the turn based gameplay"""


import pygame as pg
from config.sprites import SCOPE_HAND
from config.window import HEIGHT
from logger import logger
from sprites.enemy import Enemy
from sprites.player import Player


class TurnManager:
    """Manage the turnbased game"""

    def __init__(self, game, turn_number=0):
        self.game = game
        self.new(turn_number)

    def new(self, turn_number=0):
        self.players = list()
        self.enemies = list()

        self.sorted = None

        self.turn = turn_number
        self.vision = 0
        self.playable = 0

    def get_vision_character(self):
        """Get the character where the camera have to point

        Returns:
            Player
        """
        len_players = len(self.players)
        if len_players == 0:
            return None
        vision_to_number = self.vision % len_players
        return self.players[vision_to_number]

    def get_playable_character(self):
        """Get the character where the camera have to point

        Returns:
            Player
        """
        len_players = len(self.players)
        playable_to_number = self.playable % len_players
        return self.players[playable_to_number]

    def add_vision(self):
        """Add a vision"""
        self.vision += 1

    def add_playable(self):
        """Add a playable"""
        self.playable += 1

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
        """Sort the characters"""
        self.sorted = self.players + self.enemies

        # used to sort characters using the dexterity
        self.sorted.sort(key=get_dice)

        # used to add thief in the begining
        for character in self.sorted:
            if character.type == "thief":
                self.sorted.remove(character)
                self.sorted.insert(0, character)

        # sort the player
        players = list()
        # on regarde chaque player de la liste de players, si on le trouve dans les sorted et qu'il n'est pas déjà placé, on le place et on continue et à la fin la liste des players est triées
        for character in self.sorted:
            if isinstance(character, Player):
                for player in self.players:
                    if player == character and player in self.players:
                        players.append(player)

        self.players = players

    def add_character(self, sprite):
        """Add a sprite during the game

        Args:
            sprite (Player | Enemy)
        """

        if isinstance(sprite, Enemy):
            self.enemies.append(sprite)
        self.sorted.append(sprite)
        self.add_turn()

    def get_relative_turn(self):
        """Get the relative turn

        Returns:
            int
        """
        len_characters = len(self.get_characters())
        turn_to_number = self.turn % len_characters
        return turn_to_number

    def active(self):
        """Get the active depending of RT or Turn

        Returns:

        """
        if self.game.versus_manager.active:
            return self.active_character()
        return self.get_playable_character()

    def active_character(self):
        """Return the active character using the turn manager

        Returns:
            Player
        """
        return self.get_characters()[self.get_relative_turn()]

    def get_active_scope(self):
        """Get the scope of the active player

        Returns:
            int
        """
        scope = None
        if self.is_active_player():
            scope = SCOPE_HAND
            if self.active().weapon:
                scope = self.active().weapon.scope
        return scope

    def get_active_weapon(self):
        """Get the active weapon

        Returns:
            Weapon
        """
        return self.active().weapon

    def get_active_spell(self):
        """Get the active spell

        Returns:
            Spell
        """
        return self.active().spell

    def get_active_weapon_damage(self):
        """Get the damage of the active weapon

        Returns:
            int
        """
        damage = 5
        if self.get_active_weapon() is None:
            damage += self.active().characteristics['str'] // 5
        else:
            self.game.logs.add_log(
                f"Number of dice: {self.get_active_weapon().number_dice}, Dice value: {self.get_active_weapon().dice_value}")
            damage += self.get_active_weapon().attack()
        return damage

    def get_active_weapon_type(self):
        """Get the type of the active weapon

        Returns:
            str
        """
        if self.get_active_weapon() is None:
            return "hand"
        return self.get_active_weapon().type

    def remove_health(self, damage, character):
        """Remove life to a character

        Args:
            damage(int)
            character(Character)
        """
        character.subHp(damage)
        if character.health <= 0:
            # if not hasattr(self.active(), 'goto'):
            if self.is_active_player():
                self.active().xp += character.xp
                self.game.logs.add_log(
                    f"{self.active()} killed {character} !")
            else:
                self.game.logs.add_log(f"{character} was murdered by {self.active()}...")
        else:
            self.game.logs.add_log(f"Remove {damage}, remaining {character.health}")

    def is_active_player(self):
        """Check if the active character is a player

        Returns:
            bool
        """
        return isinstance(self.active(), Player)

    def is_active_enemy(self):
        """Check if the active character is a enemy

        Returns:
            bool
        """
        return isinstance(self.active_character(), Enemy)

    def update(self, is_versus_active):
        """Used to update the turn manager"""
        if is_versus_active:
            if self.is_active_player():
                self.active_character().update()
            if self.is_active_enemy():
                self.active_character().update()
        else:
            for enemy in self.enemies:
                enemy.update()
            self.get_playable_character().update()

    def get_pos_player(self):
        """Get the player position in the characters list, but count only the player

        Returns:
            int: the position of the player in the list
        """
        list_pos = 0
        for character in self.get_characters():
            if self.active_character() == character:
                break
            elif isinstance(character, Player):
                list_pos += 1
        return list_pos

    def remove(self, character):
        """Remove a character"""
        if isinstance(character, Player):
            character.throw_inventory()
            character.throw_equipments()
            self.players.remove(character)
            if character in self.sorted:
                self.sorted.remove(character)
                self.add_turn()
            character.kill()
            if len(self.players) == 0:
                reset_event = pg.event.Event(pg.USEREVENT, code="_State", name="reset")
                pg.event.post(reset_event)
                self.game.create_dim()
                self.game.btns_dict = self.game.create_buttons_dict("game over")
                self.game.create_buttons(self.game.screen, start_y_offset=8 * HEIGHT / 10)
                self.game.toggle_sub_state('game_over')


def get_dice(character):
    """Get the result of the dice dex of a character

    Args:
        character(Character)

    Returns:
        int
    """
    character.throw_dice("dex")
    if not character.dice["success"]:
        # add 101 to be able to sort without using true or false
        character.dice["result"] += 101
    return character.dice["result"]
