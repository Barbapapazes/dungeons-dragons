"""Define test for versus"""

import pygame as pg
from math import sqrt
from config.window import WIDTH, HEIGHT, TILESIZE
from config.colors import RED, YELLOW
from config.versus import TOUCH_HAND, DISTANCE_MOVE
from utils.tilemap import Camera
from logger import logger

# temp
from temp.enemy import Enemy


class Versus():

    def __init__(self):

        self.BT_attck = pg.Rect((0, HEIGHT - TILESIZE), (TILESIZE, HEIGHT))
        self.BT_move = pg.Rect((2*TILESIZE, HEIGHT - TILESIZE), (TILESIZE, HEIGHT))
    

    def setCamera(self,camera):
        self.camera=camera
       

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
            self.CircleATK= pg.Rect((player.pos.x-(TOUCH_HAND+1)*TILESIZE,player.pos.y -(TOUCH_HAND+1)*TILESIZE),((TOUCH_HAND+1)*TILESIZE*2,(TOUCH_HAND+1)*TILESIZE*2))
            #pg.draw.circle(surface,RED,player.pos,(TOUCH_HAND+1)*TILESIZE,2)
            pg.draw.ellipse(surface,RED,self.CircleATK.copy(),2)
    
    def rangeMOV(self,surface,player):
        pg.draw.circle(surface,YELLOW,player.pos,(DISTANCE_MOVE)*TILESIZE,2)

    def CheckMove(self,mouse_pos,player):
        return  (DISTANCE_MOVE*TILESIZE >= abs(sqrt((player.pos.x-mouse_pos[0])**2 + (player.pos.y-mouse_pos[1])**2)))


