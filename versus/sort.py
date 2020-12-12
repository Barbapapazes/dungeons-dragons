"""Define sort for Versus"""


import pygame as pg
from random import randint
from inventory.inventory import Equipable 
from config.colors import GREEN_DARK
from config.window import TILESIZE, FPS
from logger import logger




class Sort(Equipable):
    
    def __init__(self,name,img,price,slot,manaCost,srt_type,timeSort,weight=0,nb_d=1, val_d=5, scope=2):
        super(Sort,self).__init__(name,img,price,weight)
        self.slot= slot
        self.manaCost =manaCost
        self.srt_type =srt_type
        self.timeSort = timeSort #seconde 
        self.nb_d = nb_d
        self.val_d = val_d
        self.scope =scope
        self.dammage = 0



    def equip(self, inventory, target):
        """Equip the sort in the target's sort slot
        and removes it from the inventory inventory

        Args:
            inventory(Inventory)
            target(Player)
        """
        if inventory.get_equip_slot(self).item is not None:
            inventory.get_equip_slot(self).item.unequip(inventory)
        super().equip(target)
        target.equip_sort(self)
        inventory.remove_item(self)
        inventory.get_equip_slot(self).item = self

    def unequip(self, inventory):
        """Unequip the sort and add it to the Inventory

        Args:
            inventory(Inventory)
        """
        self.equipped_to.unequip_sort()
        super().unequip()
        inventory.add_item(self)
        inventory.get_equip_slot(self).item = None


    
    def DefineDMG(self):
        """Define dammage zone"""
        dammage = 0
        for _ in range(self.nb_d):
            dammage += randint(1, self.val_d)
        return dammage



    def placeSort(self,mouse_pos,game):
        logger.debug("create a zone effect")
        ZoneEffect(game,mouse_pos,self.scope,self.timeSort,self.DefineDMG(),self.srt_type)
        




class ZoneEffect(pg.sprite.Sprite):

    def __init__(self,game,mouse_pos,scope,time,DMG,type):
        self.groups = game.zoneEffect
        pg.sprite.Sprite.__init__(self,self.groups)
        self.screen = game.screen
        self.x = mouse_pos[0]
        self.y = mouse_pos[1]
        self.rect = pg.Rect(self.x-scope*TILESIZE,self.y-scope*TILESIZE,2*scope*TILESIZE,2*scope*TILESIZE)
        self.time = time * FPS
        self.dammage = DMG
        self.type = type

    def draw(self):
        pg.draw.rect(self.screen,GREEN_DARK,self.rect.copy())


    def update(self):
        self.time -= 1
        if self.time <= 0:
            self.kill()

        self.draw()


def collisionZoneEffect(person,ZoneEffect):
    for zone in ZoneEffect:
        if pg.sprite.collide_rect(person,zone):
            if zone.type == "heal":
                logger.info("Une personne gagne %d PV de la zone magique",zone.dammage)
                person.addHp(zone.dammage)
            else:    
                logger.info("Une personne subit %d dégat de la zone magique",zone.dammage)
                person.subHp(zone.dammage)

