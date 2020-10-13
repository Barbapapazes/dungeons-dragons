import pygame
from random import randint

class Item:
    """ Représente un Item """

    def __init__(self, image, name, weight, price):
        """ Constructeur de l'Item """
        self.image = image
        self.name = name
        self.weight = weight
        self.price = price

class InventoryItem():
    def __init__(self, img):
        self.img = img
        self.is_moving = False


class Equipable(InventoryItem):
    def __init__(self, image,name, weight = 5, price =1):
        super().__init__(image)
        self.is_equipped = False
        self.equipped_to = None

    def equip(self, target):
        self.is_equipped = True
        self.equipped_to = target

    def unequip(self):
        self.is_equipped = False
        self.equipped_to = None


class Weapon(Equipable):

    def __init__(self, image, name, damages, weight, price = 0, scope = 0, nb_d = 0, val_d = 0):
        """ une Epée se définit par un nom et un nombre de degats 
            qu'elle inflige """
        Equipable.__init__(self, image, name, weight, price)
        self.damages = damages
        self.nb_d = nb_d
        self.val_d = val_d
        self.scope = scope

    def attack(self):
        dmg = 0
        for _ in range(self.nb_d):
            dmg += randint(1,self.val_d)
        return dmg

    def equip(self, inv, target):
        if inv.getEquipSlot(self).item != None:
            inv.getEquipSlot(self).item.unequip(inv)
        Equipable.equip(self, target)
        target.equip_weapon(self)
        inv.removeItemInv(self)
        inv.getEquipSlot(self).item = self

    def unequip(self, inv):
        self.equipped_to.unequip_weapon()
        Equipable.unequip(self)
        inv.addItemInv(self)
        inv.getEquipSlot(self).item = None


    
"""
class Armor(Equipable):

    def __init__(self, image, name, shield, slot):
        """ """un item armur est définit par un nom, 
            un nombre de point d'armure et un slot
            (i.e. un type)""" """
        Equipable.__init__(self, image, name)
        self.shield = shield
        self.slot = slot
"""

        