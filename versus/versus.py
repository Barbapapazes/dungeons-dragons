"""Define test for versus"""

import pygame as pg
from config.window import WIDTH, HEIGHT, TILESIZE
from config.colors import RED, YELLOW
from config.versus import TOUCH_HAND
from logger import logger

# temp
from temp.enemy import Enemy


class Versus():

    def __init__(self):

        self.BT_attck = pg.Rect((0, HEIGHT - TILESIZE), (TILESIZE, HEIGHT))
        self.BT_move = pg.Rect((2*TILESIZE, HEIGHT - TILESIZE), (TILESIZE, HEIGHT))

    def draw(self, surface):
        pg.draw.rect(surface, RED, self.BT_attck.copy())
        pg.draw.rect(surface,YELLOW,self.BT_move.copy())

    def isMove(self, mouse_pos):
        return self.BT_move.collidepoint(mouse_pos[0], mouse_pos[1])

    def isATK(self, mouse_pos):
        return self.BT_attck.collidepoint(mouse_pos[0], mouse_pos[1])

    def selectEnemy(self, listEnemy, mouse_pos):
        for enemy in listEnemy:
            if enemy.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                return enemy

    def rangeATK(self,surface,player):
        if player.weapon != None:
            logger.debug(player.weapon.scope)
            pg.draw.circle(surface,RED,player.pos,player.weapon.scope*TILESIZE,2)
        else:
            pg.draw.circle(surface,RED,player.pos,(TOUCH_HAND+1)*TILESIZE,2)

