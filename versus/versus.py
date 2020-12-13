"""Define test for versus"""

import pygame as pg
from math import sqrt
from config.window import WIDTH, HEIGHT, TILESIZE
from config.colors import RED, YELLOW, BLUE, BLUE_SKY, WHITE, BLACK
from config.versus import TOUCH_HAND, DISTANCE_MOVE, DMG_ANY_WEAPON, NUM_MSG, SIZE_TEXT
from versus.sort import collisionZoneEffect
from utils.tilemap import Camera
from logger import logger
vec = pg.math.Vector2


class Versus():

    def __init__(self, game, logs):

        self.game = game

        self.action = None
        self.selectEnemy = None
        self.isVersus = False

        self.action = None
        self.selectEnemy = None
        self.active = False

        self.logs = logs

        self.create_button()

    def create_button(self):
        size = (TILESIZE, TILESIZE)
        self.attack_btn = pg.Rect((0, HEIGHT - TILESIZE), size)
        self.spell_btn = pg.Rect((TILESIZE, HEIGHT - TILESIZE), size)
        self.move_btn = pg.Rect((2 * TILESIZE, HEIGHT - TILESIZE), size)

    def is_progress(self):
        return self.action is not None

    def set_action(self, action):
        logger.info("Set the action to : %s", action)
        self.action = action

    def start(self):
        logger.info("Start the versus")
        self.logs.add_log("Start Versus")
        self.active = True
        self.action = None

    def finish(self):
        logger.info("Finish the versus")
        self.logs.add_log("Quit Versus")
        self.active = False

    def selected_enemy(self, enemies, pos):
        for enemy in enemies:
            if enemy.rect.collidepoint(pos[0], pos[1]):
                self.selectEnemy = enemy
                break
        if self.selectEnemy:
            logger.info("Click on an enemy")
            self.set_action(None)

    def range_move(self, surface, player):
        logger.info("Move your hero using your mouse")
        self.logs.add_log("Move your hero")
        pg.draw.circle(surface, YELLOW, player.pos, (DISTANCE_MOVE)*TILESIZE, 2)

    def range_spell(self, screen, player):
        pos = pg.mouse.get_pos()
        pg.draw.circle(screen, BLUE_SKY, pos, player.sort.scope * TILESIZE, 2)

    def CheckMove(self, player, pos):
        return (DISTANCE_MOVE*TILESIZE >= abs(sqrt((player.pos.x-pos[0])**2 + (player.pos.y-pos[1])**2)))

    def check_spell(self, player):
        return (player.sort is not None and (player.MP-player.sort.manaCost >= 0))

    def createZone(self, player, pos):
        player.subMP(player.sort.manaCost)
        player.sort.placeSort(pos, self.game)
        self.ENDofAction(player)

    def ENDofAction(self, player):
        player.numberOfAction -= 1
        self.action = None
        self.selectEnemy = None
        self.game.zoneEffect.update()
        collisionZoneEffect(player, self.game, self.logs)

    def update(self, player, screen):
        self.one_action(player, screen)

    def one_action(self, player, screen):
        # doit return le message à mettre dans le logger
        if(self.action == 'attack'):
            self.logs.add_log("Your action is Attack")
            self.action = 'select_enemy'
            self.logs.add_log("Select your cible")

        if self.selectEnemy is not None:
            dmg = 0
            self.logs.add_log(self.selectEnemy.name)
            if player.weapon is not None:  # check if player had a weapon

                if player.weapon.wpn_type == "sword" and player.weapon.scope >= self.distance(
                        player, self.selectEnemy):
                    if player.throwDice(player.STR):
                        dmg = player.weapon.attack()
                    else:
                        self.logs.add_log("You miss your cible")

                elif player.weapon.wpn_type == "arc":
                    dist = self.distance(player, self.selectEnemy)
                    scope = player.weapon.scope
                    if scope < dist:
                        malus = -((dist - scope) // TILESIZE) * MALUS_ARC
                    else:
                        malus = 0
                    self.logs.add_logger.debug(
                        "dist: %i scp: %i  malus: %i", dist, scope, malus)
                    if player.throwDice(player.DEX, malus):
                        dmg = player.weapon.attack()
                    else:
                        self.logs.add_log("You miss your cible")

                else:
                    self.logs.add_log("It's too far away ")
            else:
                if self.distance(player, self.selectEnemy)//TILESIZE <= TOUCH_HAND:
                    dmg = DMG_ANY_WEAPON
                else:
                    self.logs.add_log("It's too far away ")

            self.selectEnemy.HP -= dmg
            if dmg != 0:
                self.logs.add_log("The enemy " + str(self.selectEnemy.name) + " lose " + str(dmg) + " HP")

            self.ENDofAction(player)

        if self.action == 'move_is_authorized':
            # player pathfinding
            logger.debug("personnage moved wait fct pathfinding")
            self.ENDofAction(player)

    def enemy_turn(self):
        if self.versus.action == 'turn_enemy':
            self.logs.add_log("Start the enemy turn")
            # faut faire faire des trucs à l'enemy
            # self.versus.log("END turn ENEMY")
            # self.player.numberOfAction = 5
            # self.versus.log("vous avez de nouveau 5 actions")
            # collisionZoneEffect(self.player, self)
            self.versus.setAction(None)

    def draw(self, screen, player):
        self.draw_btns(screen)
        self.draw_range(screen, player)

    def draw_range(self, screen, player):
        if(self.action == 'select_enemy'):
            self.range_attack(screen, player)

        if self.action == 'move':
            self.range_move(screen, player)

        if self.action == 'pos_spell':
            self.range_spell(screen, player)

    def range_attack(self, surface, player):
        if player.weapon != None:
            logger.debug(player.weapon.scope)
            pg.draw.circle(surface, RED, player.pos, player.weapon.scope*TILESIZE, 2)
        else:
            radius = (TOUCH_HAND + 1) * TILESIZE
            pos = player.pos - vec(radius)
            range_attack = pg.Rect(pos, (radius * 2, radius * 2))
            pg.draw.ellipse(surface, RED, range_attack.copy(), 2)

    def draw_btns(self, screen):
        btn = pg.Surface((TILESIZE, TILESIZE))
        btn.fill(RED)
        screen.blit(btn, self.attack_btn)
        btn.fill(BLUE)
        screen.blit(btn, self.spell_btn)
        btn.fill(YELLOW)
        screen.blit(btn, self.move_btn)

    @classmethod
    def is_clicked(cls, btn, pos):
        return bool(btn.collidepoint(pos[0], pos[1]))

    # on peut utiliser le fait que ça soit des vecteurs
    @staticmethod
    def distance(player, enemy):
        return sqrt(
            (enemy.x - player.pos.x)**2 + (enemy.y - player.pos.y)**2)
