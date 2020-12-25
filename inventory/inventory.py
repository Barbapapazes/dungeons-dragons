"""Inventory"""

from config.sprites import ITEMS
from random import randint
from sprites.item import PlacableItem
import pygame as pg
from logger import logger
from utils.container import Container
from inventory.items import Item
from config.window import HEIGHT, WIDTH, TILESIZE
from config.colors import WHITE, GOLD, BLUE_SKY, PINK, YELLOW_LIGHT
from config.inventory import ACTIONS, ARMOR_SLOTS, MENU_DATA, WEAPON_SLOTS, EQUIPMENT_COLS, EQUIPMENT_ROWS, INVENTORY_TILESIZE, INVENTORY_SLOT_GAP, SORT_SLOTS
vec = pg.Vector2


class Inventory:
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
        self.sort_slots = []

        self.player = player

        self.display_inventory = False
        self.moving_item = None
        self.moving_item_slot = None

        self.create_slots()
        self.set_slot_types()

        self.menu_data = MENU_DATA

    @classmethod
    def create_inventory(cls, data):
        items = list()
        for item in data:
            logger.debug(item)
            if item["object_type"] == "item":
                items.append(
                    Item(
                        item["name"],
                        ITEMS[item["image_name"]],
                        item["image_name"],
                        item["price"],
                        item["weight"]))
            elif item["object_type"] == "armor":
                items.append(
                    Armor(
                        item["name"], ITEMS[item["image_name"]],
                        item["image_name"], item["price"], item["weight"], item["shield"], item["slot"]))
            elif item["object_type"] == "weapon":
                items.append(
                    Weapon(
                        item["name"],
                        ITEMS[item["image_name"]],
                        item["image_name"],
                        item["price"],
                        item["slot"],
                        item["type"],
                        item["weight"],
                        item["nb_d"],
                        item["val_d"],
                        item["scope"]))
            elif item["object_type"] == "consumable":
                items.append(
                    Consumable(
                        item["name"],
                        ITEMS[item["image_name"]],
                        item["image_name"],
                        item["price"],
                        item["weight"],
                        item["hp_gain"],
                        item["shield_gain"]))

        return items

    def save(self):
        inventory_list = list()
        for slot in self.slots:
            if slot.item:
                inventory_list.append(slot.item.save())

        return inventory_list

    def create_slots(self):
        """Create the inventory slots"""
        self.create_bag()
        self.create_equipments()

    def create_equipments(self):
        """Create slots to equip from a bag"""
        step = INVENTORY_TILESIZE + INVENTORY_SLOT_GAP

        cols = EQUIPMENT_COLS
        rows = EQUIPMENT_ROWS
        min_x = 2 * WIDTH // 4 - (step * cols) // 2 + INVENTORY_SLOT_GAP
        max_x = 2 * WIDTH // 4 + (step * cols) // 2
        min_y = HEIGHT // 2 - (step * rows) // 2 + INVENTORY_SLOT_GAP
        max_y = HEIGHT // 2 + (step * rows) // 2
        for _x in range(min_x, max_x, step):
            for _y in range(min_y, max_y, step):
                self.armor_slots.append(EquipableSlot(_x, _y, INVENTORY_TILESIZE, WHITE))

        self.weapon_slots.append(EquipableSlot(min_x - step,
                                               max_y - step + INVENTORY_SLOT_GAP, INVENTORY_TILESIZE, PINK))

        self.sort_slots.append(EquipableSlot(min_x - 2*step,
                                             max_y - step + INVENTORY_SLOT_GAP, INVENTORY_TILESIZE, BLUE_SKY))

    def create_bag(self):
        """Create a bag to store item"""
        step = INVENTORY_TILESIZE + INVENTORY_SLOT_GAP

        min_x = 3 * WIDTH // 4 - (step * self.cols) // 2 + INVENTORY_SLOT_GAP
        max_x = 3 * WIDTH // 4 + (step * self.cols) // 2
        min_y = HEIGHT // 2 - (step * self.rows) // 2 + INVENTORY_SLOT_GAP
        max_y = HEIGHT // 2 + (step * self.rows) // 2
        # inventory is 3/4 in width
        for _x in range(min_x, max_x, step):
            # inventory is center in height
            for _y in range(min_y, max_y, step):
                self.slots.append(InventorySlot(_x, _y, INVENTORY_TILESIZE, WHITE))

    def set_slot_types(self):
        """Used to define slot's type"""
        for index, value in enumerate(ARMOR_SLOTS):
            self.armor_slots[index].slot_type = value
        for index, value in enumerate(WEAPON_SLOTS):
            self.weapon_slots[index].slot_type = value
        for index, value in enumerate(SORT_SLOTS):
            self.sort_slots[index].slot_type = value

    def get_all_slots(self):
        """Get all slots fro the inventory

        Returns:
            list: All slots from an inventory
        """
        return self.slots + self.weapon_slots + self.armor_slots + self.sort_slots

    def get_equip_slot(self, item):
        """Return the slot related to the Item if it's an Equipable

        Args:
            item (Item)

        Returns:
            EquipableSlot
        """
        for slot in self.armor_slots + self.weapon_slots + self.sort_slots:
            if slot.slot_type == item.slot:
                return slot

    def find_item(self, item):
        """Find the slot in which a passed item is contained,
            None if no slot contains this item

        Args:
            item(Item)
        """
        for slot in self.get_all_slots():
            if slot.item == item:
                return slot
        return None

    def move_item(self):
        """Drag function, makes an item following the mouse"""
        mouse_pos = pg.mouse.get_pos()

        for slot in self.get_all_slots():
            if slot.rect.collidepoint(
                    mouse_pos) and slot.item is not None and self.moving_item is None:
                logger.info("Select %s from inventory", slot.item)
                slot.item.is_moving = True
                self.moving_item = slot.item
                self.moving_item_slot = slot
                break

    def place_item(self, shop_item=None, from_shop=False):
        """Place a item

        Args:
            shop_item (Item, optional) Defaults to None.
        """
        mouse_pos = pg.mouse.get_pos()

        if shop_item:
            self.moving_item = shop_item
            self.moving_item.is_moving = True

        self.outside = True
        for slot in self.get_all_slots():

            if slot.rect.collidepoint(
                    mouse_pos) and (self.moving_item is not None or shop_item):

                if isinstance(
                        self.moving_item_slot, EquipableSlot) and isinstance(
                        slot, InventorySlot) and not isinstance(
                        slot, EquipableSlot) and slot.item is None:
                    self.unequip_item(self.moving_item)
                    self.outside = False
                    break
                if isinstance(
                        slot, InventorySlot) and not isinstance(
                        slot, EquipableSlot) and not isinstance(
                        self.moving_item_slot, EquipableSlot):
                    self.remove_item(self.moving_item)
                    self.add_item(self.moving_item, slot)
                    self.outside = False
                    break
                if isinstance(self.moving_item_slot, EquipableSlot) and isinstance(slot.item, Equipable):
                    if self.moving_item.slot == slot.item.slot:
                        self.unequip_item(self.moving_item)
                        self.equip_item(slot.item)
                        self.outside = False
                        break
                if isinstance(
                        slot, EquipableSlot) and isinstance(
                        self.moving_item, Equipable):
                    if slot.slot_type == self.moving_item.slot:
                        self.equip_item(self.moving_item)
                        self.outside = False
                        break

        if self.outside and shop_item and not from_shop:
            self.throw_item(shop_item)

        if self.moving_item is not None:
            self.moving_item.is_moving = False
            self.moving_item = None
            self.moving_item_slot = None

    def check_slot(self, action, mouse_pos):
        """Use, equipe or unequip the item present in the slot colliding with the mouse_pos

        Args:
            action(String)
            mouse_pos (tuple):
        """
        for slot in self.get_all_slots():
            if isinstance(
                    slot, EquipableSlot):
                if slot.rect.collidepoint(mouse_pos):
                    if slot.item is not None:
                        if action == ACTIONS['unequip']:
                            self.unequip_item(slot.item)
                        else:
                            logger.info('Action can not be done')
                        if action == ACTIONS['throw']:
                            logger.info('Action can not be done')
            elif isinstance(slot, InventorySlot):
                if slot.rect.collidepoint(mouse_pos):
                    logger.debug(type(slot))
                    if action == ACTIONS['throw']:
                        self.throw_item(slot.item)
                    if isinstance(slot.item, Equipable):
                        if action == ACTIONS['equip']:
                            self.equip_item(slot.item)
                        else:
                            logger.info('Action can not be done')
                    if isinstance(slot.item, Consumable):
                        if action == ACTIONS['use']:
                            self.use_item(slot.item)
                        else:
                            logger.info('Action can not be done')

    def throw_item(self, item):
        """Used to throw an item

        Args:
            item (Item)
        """
        logger.info("throw %s", item)
        logger.debug("ajuster les properties")
        properties = dict()
        if isinstance(item, Weapon):
            properties['object_type'] = "weapon"
        elif isinstance(item, Armor):
            properties = {
                "object_type": "armor",
                "price": item.price,
                "weight": item.weight,
                "shield": item.shield,
                "slot": item.slot,
            }
        elif isinstance(item, Consumable):
            properties['object_type'] = "consumable"
        else:
            properties['object_type'] = "other"

        PlacableItem(
            self.player.game, vec(self.player.pos) +
            vec(randint(self.player.hit_rect.width + 50, self.player.hit_rect.width + 100),
                0).rotate(randint(0, 360)),
            item.name, properties, item.image.copy(), item.image_name)
        self.remove_item(item)

    def add_item(self, item, slot=None):
        """Add a passed item to the inventory

        Args:
            item (Item)
            slot (InventorySlot, optional): when we want a specific slot. Defaults to None.
        """
        if slot is None:
            for slots in self.slots:
                if slots.item is None:
                    item.is_moving = False
                    slots.item = item
                    logger.info("Add %s to inventory", item)
                    break
        if slot is not None:
            if slot.item is not None:
                logger.info("Add %s to inventory", item)
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
                logger.info("Remove %s from inventory", item)
                slot.item = None
                break

    def use_item(self, item):
        """Use a passed item if it's a Consumable

        Args:
            item (Item)
        """
        logger.debug(item)
        if isinstance(item, Consumable):
            logger.info("Use %s from inventory", item)
            item.use(self, self.player)

    def equip_item(self, item):
        """Equip a passed item if it's an Equipable

        Args:
            item (Item)
        """
        if isinstance(item, Equipable):
            logger.info("Equip %s from inventory", item)
            item.equip(self, self.player)

    def unequip_item(self, item):
        """unequip a passed item if it's an Equipable

        Args:
            item (Item): [description]
        """
        if isinstance(item, Equipable):
            logger.info("Unequip %s from inventory", item)
            item.unequip(self)

    def is_clicked(self, mouse_pos):
        """Check if the inventory is clicked"""
        for slot in self.get_all_slots():
            if slot.rect.collidepoint(mouse_pos):
                return True

    def draw(self, screen):
        """Used to draw the inventory

        Args:
            screen (Surface)
        """
        if self.display_inventory:
            self.player.game.draw_text(
                "Inventory", self.player.game.title_font, 48, YELLOW_LIGHT, 3 * WIDTH // 4, HEIGHT // 2 -
                ((INVENTORY_TILESIZE + INVENTORY_SLOT_GAP) * (self.rows + 2)) // 2, align="n", screen=screen)
            self.player.game.draw_text(
                "Equipment", self.player.game.title_font, 48, YELLOW_LIGHT, WIDTH // 2, HEIGHT // 2 -
                ((INVENTORY_TILESIZE + INVENTORY_SLOT_GAP) * (5 + 2)) // 2, align="n", screen=screen)
            for slot in self.get_all_slots():
                slot.draw(screen)
            for slot in self.get_all_slots():
                slot.draw_items(screen)
            self.draw_player_money()

    def draw_player_money(self):
        """Used to draw the player's money
        """
        myfont = pg.font.SysFont('Calibri', 25)
        self.coins = myfont.render(f"{self.player.gold}", False, GOLD)
        self.coinimg = pg.image.load('assets/img/coin1.png').convert_alpha()
        self.player.game.screen.blit(self.coins, (50, 175))
        self.player.game.screen.blit(self.coinimg, (0, 155))


class InventorySlot(Container):
    """A slot from the inventory"""

    def draw_items(self, screen):
        """Draw an image on an inventory slot if the image is not moving else on the mouse position

        Args:
            screen(Surface)
        """
        if self.item is not None and not self.item.is_moving:
            offset = 12
            image = pg.transform.scale(self.item.image, (self.size - offset, self.size - offset))
            image_x = image.get_width()
            image_y = image.get_height()

            pg.draw.rect(screen, (0, 255, 0), pg.Rect(self.x + offset / 2, self.y + offset / 2, image_x, image_y), 1)

            screen.blit(image, (self.x + offset / 2, self.y + offset / 2))

        if self.item is not None and self.item.is_moving:
            mouse_pos = pg.mouse.get_pos()
            image = pg.transform.scale(self.item.image, (self.size + 10, self.size + 10))
            image_x = image.get_width()
            image_y = image.get_height()

            screen.blit(image, (mouse_pos[0] - image_x // 2, mouse_pos[1] - image_y // 2))


class EquipableSlot(InventorySlot):
    """A equipable slot"""

    def __init__(self, x, y, size, bg_color, slot_type=None):
        super(EquipableSlot, self).__init__(x, y, size, bg_color)
        self.slot_type = slot_type


class Consumable(Item):
    """A consumable item"""

    def __init__(self, name,  image, image_name, price, weight, hp_gain=0, shield_gain=0):
        Item.__init__(self, name, image, image_name, price, weight)
        self.hp_gain = hp_gain
        self.shield_gain = shield_gain

    def save(self):
        return {
            self.name:
            super().save()[self.name] | {
                "object_type": "consumable",
                "heal":  self.hp_gain,
                "shield":  self.shield_gain
            }}

    def use(self, inventory, target):
        """remove the consumable from the inventory inv and uses it on the target player

        Args:
            inventory(Inventory)
            target(player)
        """
        inventory.remove_item(self)
        target.addHp(self.hp_gain)
        target.addShield(self.shield_gain)

    def __deepcopy__(self, memo):
        return Consumable(
            self.name, self.image.copy(),
            self.image_name, self.price, self.weight, self.hp_gain, self.shield_gain)


class Equipable(Item):
    """Used add equipable ability"""

    def __init__(self, name, image, image_name, price, weight):
        super(Equipable, self).__init__(name, image, image_name, price, weight)
        self.is_equipped = False
        self.equipped_to = None

    def equip(self, target):
        """equip the Equipable Item on the target

        Args:
            target(player)
        """
        self.is_equipped = True
        self.equipped_to = target

    def unequip(self):
        """Unequip the Equipable Item"""
        self.is_equipped = False
        self.equipped_to = None

    def __deepcopy__(self, memo):
        return Equipable(self.name, self.image.copy(), self.image_name, self.price, self.weight)


class Armor(Equipable):
    """Armor"""

    def __init__(self, name, image, image_name, price, weight, shield, slot):
        super(Armor, self).__init__(name, image, image_name, price, weight)
        self.shield = shield
        self.slot = slot

    def save(self):
        return {
            self.name:
            super().save()[self.name] | {
                "object_type": "armor",
                "shield": self.shield,
                "slot": self.slot
            }
        }

    def equip(self, inventory, target):
        """Equip the Armor on the right player's armor slot,
        if an Armor is already in the needed slot, it is unequipped

        Args:
            inventory(Inventory)
            target(Player):
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
            inventory(Inventory)
        """
        self.equipped_to.unequip_armor(self.slot)
        Equipable.unequip(self)
        inventory.add_item(self)
        inventory.get_equip_slot(self).item = None

    def __deepcopy__(self, memo):
        return Armor(self.name, self.image.copy(), self.image_name, self.price, self.weight, self.shield, self.slot)


class Weapon(Equipable):
    """Weapon"""

    def __init__(self, name, image, image_name, price, slot, wpn_type, weight, nb_d=1, val_d=5, scope=2):
        super(Weapon, self).__init__(name, image, image_name, price, weight)
        self.slot = slot
        self.wpn_type = wpn_type
        self.nb_d = nb_d
        self.val_d = val_d
        self.scope = scope*TILESIZE

    def save(self):
        return {
            self.name:
            super().save()[self.name] | {
                "object_type": "weapon",
                "type": self.wpn_type,
                "nb_d": self.nb_d,
                "val_d": self.val_d,
                "scope": self.scope,
                "slot": self.slot
            }
        }

    def equip(self, inventory, target):
        """Equip the weapon in the target's weapon slot
        and removes it from the inventory inventory

        Args:
            inventory(Inventory)
            target(Player)
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
            inventory(Inventory)
        """
        self.equipped_to.unequip_weapon()
        super().unequip()
        inventory.add_item(self)
        inventory.get_equip_slot(self).item = None

    def attack(self):
        dmg = 0
        for _ in range(self.nb_d):
            dmg += randint(1, self.val_d)
        return dmg

    def __deepcopy__(self, memo):
        return Weapon(
            self.name, self.image.copy(), self.image_name,
            self.price, self.slot, self.wpn_type, self.weight, self.nb_d, self.val_d, self.scope // TILESIZE)
