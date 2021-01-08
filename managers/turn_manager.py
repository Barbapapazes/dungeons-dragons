"""Used to manage the turn based gameplay"""


from config.window import HEIGHT
from config.sprites import SCOPE_HAND
from sprites.enemy import Enemy
from sprites.player import Player
from logger import logger


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

        logger.debug("il faut charger la configuration")

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

    def get_relative_turn(self):
        """Get the relative turn

        Returns:
            int
        """
        len_characters = len(self.get_characters())
        # logger.debug("si il n'y a plus de players, c'est game over")
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
            if self.active_character().weapon:
                scope = self.active_character().weapon.scope
        return scope

    def get_active_weapon(self):
        """Get the active weapon

        Returns:
            Weapon
        """
        return self.active_character().weapon

    def get_active_spell(self):
        """Get the active spell

        Returns:
            Spell
        """
        return self.active_character().spell

    def get_active_weapon_damage(self):
        """Get the damage of the active weapon

        Returns:
            int
        """
        damage = 5
        if self.get_active_weapon() is None:
            damage += self.active_character().characteristics['str']//5
        else:
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

    def remove_health(self, damage, enemy):
        """Remove life to enemy

        Args:
            damage(int)
            enemy(Enemy)
        """
        enemy.subHp(damage)
        if enemy.health == 0:
            if not hasattr(self.active_character(), 'goto'):
                self.active_character().xp += enemy.xp
                self.active_character().level_up()
                self.active_character().game.logs.add_log(f"{self.active_character()} killed {enemy} and gained {enemy.xp} exp !")
            else:
                self.active_character().game.logs.add_log(f"{enemy} was murdered by {self.active_character()}...")
        else:
            self.active_character().game.logs.add_log(f"Remove {damage}, remaining {enemy.health}")

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
            self.players.remove(character)
            if len(self.players) == 0:
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
