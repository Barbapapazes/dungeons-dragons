"""Shop"""

from os import path
from utils.container import Container
import pygame as pg
from logger import logger
from config.window import HEIGHT, WIDTH
from config.colors import WHITE
from config.shop import SHOP_TILESIZE, SHOP_SLOT_GAP, SHOP_CATEGORIES, ACTIONS, MENU_DATA
from config.sprites import CONSUMABLE, WEAPONS, ARMOR, WEAPONS_COLS, WEAPONS_ROWS, CONSUMABLE_COLS, CONSUMABLE_ROWS, ARMOR_COLS, ARMOR_ROWS
from inventory.inventory import Consumable, Weapon, Armor, EquipableSlot, InventorySlot, Equipable
from config.inventory import ACTIONS as INVENTORY_ACTIONS
from copy import deepcopy


class Shop():
    """Represent a shop"""

    def __init__(self):
        """Create the shop
        """

        game_folder = path.dirname('.')
        assets_folder = path.join(game_folder, 'assets')
        img_folder = path.join(assets_folder, 'img')
        self.items_folder = path.join(img_folder, 'items')

        self.categories = []

        self.weapons = list()
        self.armors = list()
        self.consumables = list()

        self.weapon_slots = []
        self.armor_slots = []
        self.consumable_slots = []

        self.moving_item = None
        self.moving_item_slot = None

        self.create_all_slots()
        self.add_all_items()

        self.display_shop = False

        self.menu_data = MENU_DATA

    def set_all_categories(self):
        """Used to define the different categories of items"""
        for categorie in SHOP_CATEGORIES:
            self.categories.append(categorie)

    def get_all_slots(self):
        """Get all slots fro the shop

        Returns:
            list: All slots from an shop
        """
        return self.weapon_slots + self.armor_slots + self.consumable_slots

    def toggle_shop(self):
        """Set display_shop to True it if was False and vice versa"""
        self.display_shop = not self.display_shop

    def create_all_slots(self):
        """create the shop slots"""
        self.set_all_categories()
        self.create_weapon_slots()
        self.create_armor_slots()
        self.create_consumable_slots()

    def create_weapon_slots(self):
        """Create slots for the Weapon category"""
        step, min_x, max_x, min_y, max_y = self.create_slots(WEAPONS_COLS, WEAPONS_ROWS, 0)
        for x in range(min_x, max_x, step):
            for y in range(min_y, max_y, step):
                self.weapon_slots.append(ShopSlot(x, y, SHOP_TILESIZE, WHITE))

    def create_armor_slots(self):
        """Create slots for the Armor category"""
        step, min_x, max_x, min_y, max_y = self.create_slots(ARMOR_COLS, ARMOR_ROWS, 100)
        for x in range(min_x, max_x, step):
            for y in range(min_y, max_y, step):
                self.armor_slots.append(ShopSlot(x, y, SHOP_TILESIZE, WHITE))

    def create_consumable_slots(self):
        """Create slots for the Consumable category"""
        step, min_x, max_x, min_y, max_y = self.create_slots(CONSUMABLE_COLS, CONSUMABLE_ROWS, 200)
        for x in range(min_x, max_x, step):
            for y in range(min_y, max_y, step):
                self.consumable_slots.append(ShopSlot(x, y, SHOP_TILESIZE, WHITE))

    def add_all_items(self):
        """Add all items all category"""
        self.add_all_weapons()
        self.add_all_armors()
        self.add_all_consumables()

    def add_all_weapons(self):
        """Add all items to the weapon category
        """
        self.weapons = list()
        for key, value in WEAPONS.items():
            print(value['slot'])
            data = Weapon(
                key,
                path.join(self.items_folder, value['image']),
                value['price'],
                value['slot'],
                value['type'],
                value['weight'],
            )
            self.weapons.append(data)

        for item in self.weapons:
            for slots in self.weapon_slots:
                if slots.item is None:
                    slots.item = item
                    break
                else:
                    continue

    def add_all_armors(self):
        """Add all items to the armor category"""
        self.armors = list()
        for key, value in ARMOR.items():
            data = Armor(
                key,
                path.join(self.items_folder, value['image']),
                value['price'],
                value['weight'],
                value['armor'],
                value['slot'])
            self.armors.append(data)

        for item in self.armors:
            for slots in self.armor_slots:
                if slots.item is None:
                    slots.item = item
                    break
                else:
                    continue

    def add_all_consumables(self):
        """Add all items to the consumable category"""
        self.consumables = list()
        for key, value in CONSUMABLE.items():
            data = Consumable(
                key,
                path.join(self.items_folder, value['image']),
                value['price'],
                value['weight'])
            self.consumables.append(data)

        for item in self.consumables:
            for slots in self.consumable_slots:
                if slots.item is None:
                    slots.item = item
                    break
                else:
                    continue

    def draw(self, screen):
        """Used to draw the shop

        Args:
            screen (Surface)
        """
        if self.display_shop:
            for slot in self.get_all_slots():
                slot.draw(screen)
            for slot in self.get_all_slots():
                slot.draw_items(screen)

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

    def place_item(self, inventory, screen):
        inventory.place_item(screen, deepcopy(self.moving_item))
        print("shop: place inventory")
        if self.moving_item is not None:
            self.moving_item.is_moving = False
            self.moving_item = None
            self.moving_item_slot = None

    def check_slot(self, action, screen, player, mouse_pos):
        """Execute a passed action if it's possible

        Args:
            action(string)
            screen (Surface)
            mouse_pos (tuple):
        """
        for slot in self.get_all_slots():
            if slot.item is not None:
                if slot.draw(screen).collidepoint(mouse_pos):
                    print(slot)
                    if action == ACTIONS['buy']:
                        logger.info('%s bought', slot.item.name)
                        self.buy_item(slot.item, player)
                    elif action == ACTIONS['buy_equip']:
                        print("buy-equip")
                        if isinstance(slot.item, Equipable):
                            self.buy_item(slot.item, player, INVENTORY_ACTIONS['equip'])
                        else:
                            logger.info('Action can not be done')
                    elif action == ACTIONS['buy_use']:
                        if isinstance(slot.item, Consumable):
                            self.buy_item(slot.item, player, INVENTORY_ACTIONS['use'])
                        else:
                            logger.info('Action can not be done')
                    else:
                        logger.info('Action can not be done')

        for slot in player.inventory.get_all_slots():
            if isinstance(slot, InventorySlot):
                if slot.draw(screen).collidepoint(mouse_pos):
                    if action == INVENTORY_ACTIONS['sell']:
                        logger.info('%s sold', slot.item.name)
                        self.sell_item(slot.item, player)
                        slot.item = None
                    elif action in list(ACTIONS['equip']) + list(ACTIONS['unequip'])+list(ACTIONS['use']):
                        player.inventory.check_slot(action, screen, mouse_pos)
                    else:
                        logger.info('Action can not be done')
            elif isinstance(slot, EquipableSlot):
                if slot.draw(screen).collidepoint(mouse_pos):
                    if slot.item is not None:
                        if action == INVENTORY_ACTIONS['sell']:
                            logger.info('%s sold', slot.item.name)
                            player.inventory.unequip_item(slot.item)
                            self.sell_item(slot.item, player)
                            slot.item = None
                    else:
                        logger.info('Action can not be done')

    def buy_item(self, item, player, second_action=None):
        """Buy an item

        Args:
            item (Item)
            player (Player)
            second_action (String, optional): Defaults to None.
        """
        if item.price > player.gold:
            print("You're homeless")
            return
        else:
            data = deepcopy(item)
        player.inventory.add_item(data)
        if second_action == INVENTORY_ACTIONS['equip']:
            print(player.inventory.find_item(data).item)
            player.inventory.equip_item(player.inventory.find_item(data).item)
        if second_action == INVENTORY_ACTIONS['use']:
            player.inventory.use_item(player.inventory.find_item(data).item)

    def sell_item(self, item, player):
        """Sell an item

        Args:
            item (Item)
            player (Player)
        """
        if item is not None:
            player.gold += item.price

    def find_item(self, item):
        """Find the slot in which a passed item is contained,
            None if no slot contains thi sitem

        Args:
            item(Item)
        """
        for slot in self.get_all_slots():
            if slot.item == item:
                return slot
        return None

    @staticmethod
    def create_slots(cols, rows, offset_y):
        """Create value to place data

        Args:
            cols (int)
            rows (int)
            offset_y (int)

        Returns:
            tuple: step, min_x, max_x, min_y, max_y
        """
        step = SHOP_TILESIZE + SHOP_SLOT_GAP
        min_x = WIDTH // 4 - (step * cols) // 2 + SHOP_SLOT_GAP
        max_x = WIDTH // 4 + (step * cols) // 2
        min_y = HEIGHT // 3 - (step * rows) // 2 + SHOP_SLOT_GAP + offset_y
        max_y = HEIGHT // 3 + (step * rows) // 2 + offset_y
        return (step, min_x, max_x, min_y, max_y)

    def is_clicked(self, mouse_pos):
        for slot in self.get_all_slots():
            if slot.rect.collidepoint(mouse_pos):
                return True


class ShopSlot(Container):
    """A slot from the shop"""

    def draw_items(self, screen):
        """Draw an image on a shop slot

        Args:
            screen (Surface)
        """
        if self.item is not None:
            image = pg.image.load(self.item.img).convert_alpha()
            image = pg.transform.scale(image, (self.size, self.size))
            image_x = image.get_width()
            image_y = image.get_height()

            pg.draw.rect(screen, (0, 255, 0), pg.Rect(self.x, self.y, image_x, image_y), 1)

            screen.blit(image, (self.x, self.y))

        if self.item is not None and self.item.is_moving:
            mouse_pos = pg.mouse.get_pos()
            image = pg.image.load(self.item.img).convert_alpha()
            image = pg.transform.scale(image, (self.size + 10, self.size + 10))
            image_x = image.get_width()
            image_y = image.get_height()

            screen.blit(image, (mouse_pos[0] - image_x // 2, mouse_pos[1] - image_y // 2))
