"""Define test for versus"""

import pygame as pg 
from config.window import WIDTH, HEIGHT, TILESIZE
from config.colors import RED

#temp
from temp.enemy import Enemy


class Versus():

    def __init__(self):

        self.BT_attck = pg.Rect((0,HEIGHT-TILESIZE),(TILESIZE,HEIGHT))

    
    def draw(self, surface):
        pg.draw.rect(surface,RED,self.BT_attck.copy())

    def isATK(self,mouse_pos):
        return self.BT_attck.collidepoint(mouse_pos[0],mouse_pos[1])
            
    def selectEnemy(self,listEnemy,mouse_pos):
        for enemy in listEnemy:
            if enemy.rect.collidepoint(mouse_pos[0],mouse_pos[1]):
                return enemy
