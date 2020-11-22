"""Inventory"""

import pygame as pg
from random import randint
from config.window import HEIGHT, WIDTH, TILESIZE
from config.colors import WHITE
from config.inventory import ARMOR_SLOTS, WEAPON_SLOTS, EQUIPMENT_COLS, EQUIPMENT_ROWS, INVENTORY_TILESIZE, INVENTORY_SLOT_GAP
from inventory.items import Item


class Inventory():
    """Represent a inventory"""

    def __init__(self, player, cols, rows):
        """Create the inventory

        Args:
            player (Player)
            cols (Number)
            rows (Number)
        """
        self.rows = rows
        self.cols = cols

        self.slots = []
        self.armor_slots = []
        self.weapon_slots = []

        self.player = player

        self.display_inventory = False
        self.moving_item = None
        self.moving_item_slot = None

        self.create_slots()
        self.set_slot_types()

    def create_slots(self):
        """Create the inventory slots"""
        self.create_bag()
        self.create_equipments()

    def create_equipments(self):
        """Create slots to equipe from a bag"""
        step = INVENTORY_TILESIZE + INVENTORY_SLOT_GAP

        cols = EQUIPMENT_COLS
        rows = EQUIPMENT_ROWS
        min_x = 2 * WIDTH // 4 - (step * cols) // 2 + INVENTORY_SLOT_GAP
        max_x = 2 * WIDTH // 4 + (step * cols) // 2
        min_y = HEIGHT // 2 - (step * rows) // 2 + INVENTORY_SLOT_GAP
        max_y = HEIGHT // 2 + (step * rows) // 2
        for x in range(min_x, max_x, step):
            for y in range(min_y, max_y, step):
                self.armor_slots.append(EquipableSlot(x, y))

        self.weapon_slots.append(EquipableSlot(min_x - step,
                                               max_y - step + INVENTORY_SLOT_GAP))

    def create_bag(self):
        """Create a bag to store item"""
        step = INVENTORY_TILESIZE + INVENTORY_SLOT_GAP

        min_x = 3 * WIDTH // 4 - (step * self.cols) // 2 + INVENTORY_SLOT_GAP
        max_x = 3 * WIDTH // 4 + (step * self.cols) // 2
        min_y = HEIGHT // 2 - (step * self.rows) // 2 + INVENTORY_SLOT_GAP
        max_y = HEIGHT // 2 + (step * self.rows) // 2
        # inventory is 3/4 in width
        for x in range(min_x, max_x, step):
            # inventory is center in height
            for y in range(min_y, max_y, step):
                self.slots.append(InventorySlot(x, y))

    def set_slot_types(self):
        """Used to define slot's type"""
        for index, value in enumerate(ARMOR_SLOTS):
            self.armor_slots[index].slot_type = value
        for index, value in enumerate(WEAPON_SLOTS):
            self.weapon_slots[index].slot_type = value

    def get_all_slots(self):
        """Get all slots fro the inventory

        Returns:
            list: All slots from an inventory
        """
        return self.slots + self.weapon_slots + self.armor_slots

    def draw(self, screen):
        """Used to draw the inventory

        Args:
            screen (Surface)
        """
        if self.display_inventory:
            for slot in self.get_all_slots():
                slot.draw(screen)
            for slot in self.get_all_slots():
                slot.draw_items(screen)

    def toggle_inventory(self):
        """Set dispay_inventory to True it if was False and vice versa"""
        self.display_inventory = not self.display_inventory

    def add_item(self, item, slot=None):
        """Add a passed item to the inventory

        Args:
            item (Item)
            slot (InventorySlot, optional): when we want a specific slot. Defaults to None.
        """
        if slot is None:
            for slots in self.slots:
                if slots.item is None:
                    slots.item = item
                    break
        if slot is not None:
            if slot.item is not None:
                self.moving_item_slot.item = slot.item
                slot.item = item
            else:
                slot.item = item

    def remove_item(self, item):
        """Remove a passed item from the inventory

        Args:
            item (Item)
        """
        for slot in self.slots:
            if slot.item == item:
                slot.item = None
                break

    def move_item(self, screen):
        """Drag function, makes an item following the mouse

        Args:
            screen (Surface)
        """
        mouse_pos = pg.mouse.get_pos()

        for slot in self.get_all_slots():
            if slot.draw(screen).collidepoint(
                    mouse_pos) and slot.item is not None and self.moving_item is None:
                slot.item.is_moving = True
                self.moving_item = slot.item
                self.moving_item_slot = slot
                break

    def place_item(self, screen):
        """Place a item

        Args:
            screen (Surface)
        """
        mouse_pos = pg.mouse.get_pos()

        for slot in self.get_all_slots():
            if slot.draw(screen).collidepoint(
                    mouse_pos) and self.moving_item is not None:
                if isinstance(
                        self.moving_item_slot, EquipableSlot) and isinstance(
                        slot, InventorySlot) and not isinstance(
                        slot, EquipableSlot) and slot.item is None:
                    self.unequip_item(self.moving_item)
                    break
                if isinstance(
                        slot, InventorySlot) and not isinstance(
                        slot, EquipableSlot) and not isinstance(
                        self.moving_item_slot, EquipableSlot):
                    self.remove_item(self.moving_item)
                    self.add_item(self.moving_item, slot)
                    break
                if isinstance(self.moving_item_slot, EquipableSlot) and isinstance(slot.item, Equipable):
                    if self.moving_item.slot == slot.item.slot:
                        self.unequip_item(self.moving_item)
                        self.equip_item(slot.item)
                        break
                if isinstance(
                        slot, EquipableSlot) and isinstance(
                        self.moving_item, Equipable):
                    if slot.slot_type == self.moving_item.slot:
                        self.equip_item(self.moving_item)
                        break
        if self.moving_item is not None:
            self.moving_item.is_moving = False
            self.moving_item = None
            self.moving_item_slot = None

    def check_slot(self, screen, mouse_pos):
        """Use, equipe or unequip the item present in the slot colliding with the mouse_pos

        Args:
            screen (Surface)
            mouse_pos (tuple):
        """
        for slot in self.get_all_slots():
            if isinstance(slot, InventorySlot):
                if slot.draw(screen).collidepoint(mouse_pos):
                    if isinstance(slot.item, Equipable):
                        self.equip_item(slot.item)
                    if isinstance(slot.item, Consumable):
                        self.use_item(slot.item)
            if isinstance(slot, EquipableSlot):
                if slot.draw(screen).collidepoint(mouse_pos):
                    if slot.item is not None:
                        self.unequip_item(slot.item)

    def get_equip_slot(self, item):
        """Return the slot related to the Item if it's an Equipable

        Args:
            item (Item)

        Returns:
            EquipableSlot
        """
        for slot in self.armor_slots + self.weapon_slots:
            if slot.slot_type == item.slot:
                return slot

    def use_item(self, item):
        """Use a passed item if it's a Consumable

        Args:
            item (Item)
        """
        if isinstance(item, Consumable):
            item.use(self, self.player)

    def equip_item(self, item):
        """Equip a passed item if it's an Equipable

        Args:
            item (Item)
        """
        if isinstance(item, Equipable):
            item.equip(self, self.player)

    def unequip_item(self, item):
        """unequip a passed item if it's an Equipable

        Args:
            item (Item): [description]
        """
        if isinstance(item, Equipable):
            item.unequip(self)


class InventorySlot:
    """A slot from the inventory"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.item = None

    def draw(self, screen):
        """Return the drawing of an inventoryslot

        Args:
            screen (surface)

        Returns:
            Rect: the slot
        """
        return pg.draw.rect(
            screen, WHITE, (self.x, self.y, INVENTORY_TILESIZE, INVENTORY_TILESIZE))

    def draw_items(self, screen):
        """Draw an image on an inventory slot if the image is not moving else on the mouse position

        Args:
            screen (Surface)
        """
        if self.item is not None and not self.item.is_moving:
            image = pg.image.load(self.item.img).convert_alpha()
            image = pg.transform.scale(image, (INVENTORY_TILESIZE, INVENTORY_TILESIZE))
            image_x = image.get_width()
            image_y = image.get_height()

            pg.draw.rect(screen, (0, 255, 0), pg.Rect(self.x, self.y, image_x, image_y), 1)

            screen.blit(image, (self.x, self.y))

        if self.item is not None and self.item.is_moving:
            mouse_pos = pg.mouse.get_pos()
            image = pg.image.load(self.item.img).convert_alpha()
            image = pg.transform.scale(image, (INVENTORY_TILESIZE + 10, INVENTORY_TILESIZE + 10))
            image_x = image.get_width()
            image_y = image.get_height()

            screen.blit(image, (mouse_pos[0] - image_x // 2, mouse_pos[1] - image_y // 2))


class EquipableSlot(InventorySlot):
    """A equipable slot"""

    def __init__(self, x, y, slot_type=None):
        InventorySlot.__init__(self, x, y)
        self.slot_type = slot_type


class Consumable(Item):
    """A consumable item"""

    def __init__(self, name,  img, value, hp_gain=0, shield_gain=0):
        Item.__init__(self, name, img, value)
        self.hp_gain = hp_gain
        self.shield_gain = shield_gain

    def use(self, inventory, target):
        """remove the consumable from the inventory inv and uses it on the target player

        Args:
            inventory (Inventory)
            target (player)
        """
        inventory.remove_item(self)
        target.addHp(self.hp_gain)
        target.addShield(self.shield_gain)


class Equipable(Item):
    """Used add equipable ability"""

    def __init__(self, name, img, value):
        super(Equipable, self).__init__(name, img, value)
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
        """Unequip the Equipable Item"""
        self.is_equipped = False
        self.equipped_to = None


class Armor(Equipable):
    """Armor"""

    def __init__(self, name, img, value, shield, slot):
        super(Armor, self).__init__(name, img, value)
        self.shield = shield
        self.slot = slot

    def equip(self, inventory, target):
        """Equip the Armor on the right player's armor slot,
        if an Armor is already in the needed slot, it is unequipped


        Args:
            inventory (Inventory)
            target (Player):
        """
        if inventory.get_equip_slot(self).item is not None:
            inventory.get_equip_slot(self).item.unequip(inventory)
        super().equip(target)
        target.equip_armor(self)
        inventory.remove_item(self)
        inventory.get_equip_slot(self).item = self

    def unequip(self, inventory):
        """Unequip the armor and put it in the inventory inventory

        Args:
            inventory (Inventory)
        """
        self.equipped_to.unequip_armor(self.slot)
        Equipable.unequip(self)
        inventory.add_item(self)
        inventory.get_equip_slot(self).item = None


class Weapon(Equipable):
    """Weapon"""

    def __init__(self, name, img, value, slot, wpn_type, nb_d=1, val_d=5,scope=2):
        super(Weapon, self).__init__(name, img, value)
        self.slot = slot
        self.wpn_type = wpn_type
        self.nb_d = nb_d
        self.val_d = val_d
        self.scope = scope*TILESIZE

    def equip(self, inventory, target):
        """Equip the weapon in the target's weapon slot
        and removes it from the inventory inventory

        Args:
            inventory (Inventory)
            target (Player)
        """
        if inventory.get_equip_slot(self).item is not None:
            inventory.get_equip_slot(self).item.unequip(inventory)
        super().equip(target)
        target.equip_weapon(self)
        inventory.remove_item(self)
        inventory.get_equip_slot(self).item = self

    def unequip(self, inventory):
        """Unequip the weapon and add it to the Inventory 

        Args:
            inventory (Inventory)
        """
        self.equipped_to.unequip_weapon()
        super().unequip()
        inventory.add_item(self)
        inventory.get_equip_slot(self).item = None

    def attack(self):
        dmg = 0
        for _ in range(self.nb_d):
            dmg += randint(1,self.val_d)
        return dmg