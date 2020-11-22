"""define temp enemy"""

import pygame as pg  
from config.window import TILESIZE 
from config.colors import CYAN


class Enemy(pg.sprite.Sprite):

    def __init__(self,game,x,y,name="boot"):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.name = name
        self.x = x *TILESIZE
        self.y = y *TILESIZE
        
        self.HP = 100
        

        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        