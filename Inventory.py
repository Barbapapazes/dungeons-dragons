import pygame, sys
from settings import *
from Items import *


class Inventory():

    def __init__(self, player, totalSlots, cols, rows, max_weight = 100):
        self.totalSlots = totalSlots
        self.max_weight = max_weight
        self.act_weight = 0
        self.rows = rows
        self.cols = cols
        self.inventory_slots = []
        self.armor_slots = []
        self.weapon_slots = []
        self.display_inventory = False
        self.player = player
        self.appendSlots()
        self.setSlotTypes()

        self.movingitem = None
        self.movingitemslot = None

    def appendSlots(self):
        while len(self.inventory_slots) != self.totalSlots:
            for x in range(WIDTH//2 - ((INVTILESIZE+2) * self.cols)//2, WIDTH//2 + ((INVTILESIZE+2) * self.cols) //2, INVTILESIZE+2):
                for y in range(UIHEIGTH, UIHEIGTH+INVTILESIZE * self.rows, INVTILESIZE+2):
                    self.inventory_slots.append(InventorySlot(x, y))

        while len(self.armor_slots) != 4:
            for y in range(UIHEIGTH-100, UIHEIGTH-100+(INVTILESIZE+1) * 4, INVTILESIZE+2):
                self.armor_slots.append(EquipableSlot(self.inventory_slots[0].x - 100, y))

        while len(self.weapon_slots) != 1:
            self.weapon_slots.append(EquipableSlot(self.armor_slots[3].x - 50, self.armor_slots[3].y))

    def setSlotTypes(self):
        self.armor_slots[0].slottype = 'head'
        self.armor_slots[1].slottype = 'chest'
        self.armor_slots[2].slottype = 'legs'
        self.armor_slots[3].slottype = 'feet'
        self.weapon_slots[0].slottype = 'weapon'

    def draw(self, screen):
        if self.display_inventory:
            for slot in self.armor_slots + self.inventory_slots + self.weapon_slots:
                slot.draw(screen)
            for slot in self.armor_slots + self.inventory_slots + self.weapon_slots:
                slot.drawItems(screen)

    def toggleInventory(self):
            self.display_inventory = not self.display_inventory

    def addItemInv(self, item, slot=None):
        if slot == None:
            for slots in self.inventory_slots:
                if slots.item == None:
                    slots.item = item
                break
        if slot != None:
            if slot.item != None:
                self.movingitemslot.item = slot.item
                slot.item = item
            else:
                slot.item = item

    def removeItemInv(self, item):
        for slot in self.inventory_slots:
            if slot.item == item:
                slot.item = None
                break

    def moveItem(self, screen):
        mousepos = pygame.mouse.get_pos()
        for slot in self.inventory_slots + self.armor_slots + self.weapon_slots:
            if slot.draw(screen).collidepoint(mousepos) and slot.item != None:
                slot.item.is_moving = True
                self.movingitem = slot.item
                self.movingitemslot = slot
                break

    def placeItem(self, screen):
        mousepos = pygame.mouse.get_pos()
        for slot in self.inventory_slots + self.armor_slots + self.weapon_slots:
            if slot.draw(screen).collidepoint(mousepos) and self.movingitem != None:
                if isinstance(self.movingitemslot, EquipableSlot) and isinstance(slot, InventorySlot) and not isinstance(slot, EquipableSlot) and slot.item == None:
                    self.unequipItem(self.movingitem)
                    break
                if isinstance(slot, InventorySlot) and not isinstance(slot, EquipableSlot) and not isinstance(self.movingitemslot, EquipableSlot):
                    self.removeItemInv(self.movingitem)
                    self.addItemInv(self.movingitem, slot)
                    break
                if isinstance(self.movingitemslot, EquipableSlot) and isinstance(slot.item, Equipable):
                    if self.movingitem.slot == slot.item.slot:
                        self.unequipItem(self.movingitem)
                        self.equipItem(slot.item)
                        break
                if isinstance(slot, EquipableSlot) and isinstance(self.movingitem, Equipable):
                    if slot.slottype == self.movingitem.slot:
                        self.equipItem(self.movingitem)
                        break
        if self.movingitem != None:
            self.movingitem.is_moving = False
            self.movingitem = None
            self.movingitemslot = None

    def checkSlot(self, screen, mousepos):
        for slot in self.inventory_slots + self.armor_slots + self.weapon_slots:
            if isinstance(slot, InventorySlot):
                if slot.draw(screen).collidepoint(mousepos):
                    if isinstance(slot.item, Equipable):
                        self.equipItem(slot.item)
                    """if isinstance(slot.item, Consumable):
                        self.useItem(slot.item)"""
            if isinstance(slot, EquipableSlot):
                if slot.draw(screen).collidepoint(mousepos):
                    if slot.item != None:
                        self.unequipItem(slot.item)

    def getEquipSlot(self, item):
        for slot in self.armor_slots + self.weapon_slots:
            if slot.slottype == item.slot:
                return slot

    """def useItem(self, item):
        if isinstance(item, Consumable):
            item.use(self, self.player)"""

    def equipItem(self, item):
        if isinstance(item, Equipable):
            item.equip(self, self.player)

    def unequipItem(self, item):
        if isinstance(item, Equipable):
            item.unequip(self)

class InventorySlot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.item = None

    def draw(self, screen):
        return pygame.draw.rect(screen, WHITE, (self.x, self.y, INVTILESIZE, INVTILESIZE))

    def drawItems(self, screen):
        if self.item != None and not self.item.is_moving:
            self.image = pygame.image.load(self.item.img).convert_alpha()
            screen.blit(self.image, (self.x-7, self.y-7))
        if self.item != None and self.item.is_moving:
            mousepos1 = pygame.mouse.get_pos()
            self.image = pygame.image.load(self.item.img).convert_alpha()
            screen.blit(self.image, (mousepos1[0]-20,mousepos1[1]-20))

class EquipableSlot(InventorySlot):
    def __init__(self, x, y, slottype=None):
        InventorySlot.__init__(self, x, y)
        self.slottype = slottype

