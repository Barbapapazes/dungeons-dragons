import pygame as pg
from config.window import WIDTH
from config.colors import WHITE


UIHEIGTH = 300
INVTILESIZE = 48


class Inventory():

    def __init__(self, player, totalSlots, cols, rows):
        self.totalSlots = totalSlots
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
        """Update the inventory_slots list
        """
        while len(self.inventory_slots) != self.totalSlots:
            for x in range(WIDTH//2 - ((INVTILESIZE+2) * self.cols)//2, 
                            WIDTH//2 + ((INVTILESIZE+2) * self.cols) //2, 
                                                            INVTILESIZE+2):
                for y in range(UIHEIGTH, UIHEIGTH+INVTILESIZE * self.rows, 
                                                        INVTILESIZE+2):
                    self.inventory_slots.append(InventorySlot(x, y))

        while len(self.armor_slots) != 4:
            for y in range(UIHEIGTH-100, UIHEIGTH-100+(INVTILESIZE+1) * 4, 
                                                            INVTILESIZE+2):
                self.armor_slots.append(EquipableSlot(self.inventory_slots[0].x - 100, y))

        while len(self.weapon_slots) != 1:
            self.weapon_slots.append(EquipableSlot(self.armor_slots[3].x - 50, 
                                                        self.armor_slots[3].y))

    def setSlotTypes(self):
        """Used to define Armor and Weapon slots
        """
        self.armor_slots[0].slottype = 'head'
        self.armor_slots[1].slottype = 'chest'
        self.armor_slots[2].slottype = 'legs'
        self.armor_slots[3].slottype = 'feet'
        self.weapon_slots[0].slottype = 'weapon'

    def draw(self, screen): 
        """Used to draw the inventory

        Args:
            screen (Surface)
        """
        if self.display_inventory:
            for slot in self.armor_slots + self.inventory_slots + self.weapon_slots:
                slot.draw(screen)
            for slot in self.armor_slots + self.inventory_slots + self.weapon_slots:
                slot.drawItems(screen)

    def toggleInventory(self):
        """Set dispay_inventory to True it if was False and vice versa
        """
        self.display_inventory = not self.display_inventory

    def addItemInv(self, item, slot=None):
        """Add a passed item to the inventory

        Args:
            item (Item)
            slot (InventorySlot, optional): when we want a specific slot. Defaults to None.
        """
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
        """Remove a passed item from the inventory

        Args:
            item (Item)
        """
        for slot in self.inventory_slots:
            if slot.item == item:
                slot.item = None
                break

    def moveItem(self, screen):
        """Drag function, makes an item following the mouse 

        Args:
            screen (Surface)
        """
        mousepos = pg.mouse.get_pos()
        
        for slot in self.inventory_slots + self.armor_slots + self.weapon_slots:
            if slot.draw(screen).collidepoint(mousepos) and slot.item != None and self.movingitem == None:
                slot.item.is_moving = True
                self.movingitem = slot.item
                self.movingitemslot = slot
                break

    def placeItem(self, screen):
        """

        Args:
            screen (Surface)
        """
        mousepos = pg.mouse.get_pos()
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
        """Use, equipe or unequip the item present in the slot colliding with the mousepos

        Args:
            screen (Surface)
            mousepos (tuple):
        """
        for slot in self.inventory_slots + self.armor_slots + self.weapon_slots:
            if isinstance(slot, InventorySlot):
                if slot.draw(screen).collidepoint(mousepos):
                    if isinstance(slot.item, Equipable):
                        self.equipItem(slot.item)
                    if isinstance(slot.item, Consumable):
                        self.useItem(slot.item)
            if isinstance(slot, EquipableSlot):
                if slot.draw(screen).collidepoint(mousepos):
                    if slot.item != None:
                        self.unequipItem(slot.item)

    def getEquipSlot(self, item):
        """Return the slot related to the Item if it's an Equipable

        Args:
            item (Item)

        Returns:
            EquipableSlot
        """
        for slot in self.armor_slots + self.weapon_slots:
            if slot.slottype == item.slot:
                return slot

    def useItem(self, item):
        """Use a passed item if it's a Consumable

        Args:
            item (Item)
        """
        if isinstance(item, Consumable):
            item.use(self, self.player)

    def equipItem(self, item):
        """Equip a passed item if it's an Equipable 

        Args:
            item (Item)
        """
        if isinstance(item, Equipable):
            item.equip(self, self.player)

    def unequipItem(self, item):
        """unequip a passed item if it's an Equipable

        Args:
            item ([type]): [description]
        """
        if isinstance(item, Equipable):
            item.unequip(self)


class InventorySlot:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.item = None

    def draw(self, screen):
        """return the drawing of an inventoryslot

        Args:
            screen (surface)

        Returns:
            [type]: [description]
        """
        return pg.draw.rect(screen, WHITE, (self.x, self.y, INVTILESIZE, INVTILESIZE))

    def drawItems(self, screen):
        """Draw an image on an inventory slot if the image is not moving else on the mouse position

        Args:
            screen (Surface)
        """
        if self.item != None and not self.item.is_moving:
            self.image = pg.image.load(self.item.img).convert_alpha()
            screen.blit(self.image, (self.x-7, self.y-7))
        if self.item != None and self.item.is_moving:
            mousepos1 = pg.mouse.get_pos()
            self.image = pg.image.load(self.item.img).convert_alpha()
            screen.blit(self.image, (mousepos1[0]-20,mousepos1[1]-20))


class EquipableSlot(InventorySlot):

    def __init__(self, x, y, slottype=None):
        InventorySlot.__init__(self, x, y)
        self.slottype = slottype

class Item():

    def __init__(self, img, value):
        self.img = img
        self.value = value
        self.is_moving = False

class Consumable(Item):

    def __init__(self, img, value, hp_gain=0, shield_gain=0):
        Item.__init__(self, img, value)
        self.hp_gain = hp_gain
        self.shield_gain = shield_gain

    def use(self, inv, target):
        """remove the consumable from the inventory inv and uses it on the target player

        Args:
            inv (Inventory)
            target (player)
        """
        inv.removeItemInv(self)
        target.addHp(self.hp_gain)
        target.addShield(self.shield_gain)

class Equipable(Item):

    def __init__(self, img, value):
        Item.__init__(self, img, value)
        self.is_equipped = False
        self.equipped_to = None

    def equip(self, target):
        """equip the Equipable Item on the target

        Args:
            target (player)
        """
        self.is_equipped = True
        self.equipped_to = target

    def unequip(self):
        """Unequip the Equipable Item
        """
        self.is_equipped = False
        self.equipped_to = None

class Armor(Equipable):

    def __init__(self, img, value, shield, slot):
        Equipable.__init__(self, img, value)
        self.shield = shield
        self.slot = slot

    def equip(self, inv, target):
        """Equip the Armor on the right player's armor slot, 
        if an Armor is already in the needed slot, it is unequiped 


        Args:
            inv (Inventory)
            target (Player): 
        """
        if inv.getEquipSlot(self).item != None:
            inv.getEquipSlot(self).item.unequip(inv)
        Equipable.equip(self, target)
        target.equip_armor(self)
        inv.removeItemInv(self)
        inv.getEquipSlot(self).item = self

    def unequip(self, inv):
        """Unequip the armor and put it in the inventory inventory

        Args:
            inv (Inventory)
        """
        self.equipped_to.unequip_armor(self.slot)
        Equipable.unequip(self)
        inv.addItemInv(self)
        inv.getEquipSlot(self).item = None

class Weapon(Equipable):

    def __init__(self, img, value, slot, wpn_type):
        Equipable.__init__(self, img, value)
        self.slot = slot
        self.wpn_type = wpn_type

    def equip(self, inv, target):
        """Equip the weapon in the target's weapon slot
        and removes it from the inventory inventory

        Args:
            inv (Inventory)
            target (Player)
        """
        if inv.getEquipSlot(self).item != None:
            inv.getEquipSlot(self).item.unequip(inv)
        Equipable.equip(self, target)
        target.equip_weapon(self)
        inv.removeItemInv(self)
        inv.getEquipSlot(self).item = self

    def unequip(self, inv):
        """Unequip the weapon and add it to the Inventory inv

        Args:
            inv (Inventory)
        """
        self.equipped_to.unequip_weapon()
        Equipable.unequip(self)
        inv.addItemInv(self)
        inv.getEquipSlot(self).item = None
