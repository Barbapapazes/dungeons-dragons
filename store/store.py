"""Used to create the chest store"""

from os import path
from copy import deepcopy
from random import randint, choice
import pygame as pg
from logger import logger
from inventory.inventory import Consumable, Weapon, Armor, EquipableSlot, InventorySlot, Equipable
from utils.container import Container
from config.window import HEIGHT, WIDTH
from config.colors import WHITE, YELLOW_LIGHT
from config.store import STORE_TILESIZE, STORE_SLOT_GAP, STORE_CATEGORIES, STORE_ACTIONS, STORE_MENU
from config.sprites import CONSUMABLE, ITEMS, WEAPONS, ARMOR, WEAPONS_COLS,  CONSUMABLE_COLS,  ARMOR_COLS
from config.inventory import ACTIONS as INVENTORY_ACTIONS


class Store:
    """Represent a store"""

    def __init__(self, game, consumable, weapons, armor, menu_data=STORE_MENU):
        """Create the store
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

        if weapons is not None:
            weapons = weapons.items()
        if armor is not None:
            armor = armor.items()
        if consumable is not None:
            consumable = consumable.items()

        self.chosen_weapons = [choice(list(WEAPONS.items())) for _ in range(
            randint(0, 5))] if weapons is None else weapons
        self.chosen_armor = [choice(list(ARMOR.items())) for _ in range(randint(0, 5))] if armor is None else armor
        self.chosen_consumables = [choice(list(CONSUMABLE.items()))
                                   for _ in range(randint(0, 5))] if consumable is None else consumable

        self.moving_item = None
        self.moving_item_slot = None

        self.menu_data = menu_data
        self.game = game

        self.create_all_slots()
        self.add_all_items()

        self.display_shop = False

    def save(self):
        """Used to save the store

        Returns:
            dict
        """
        slots = {
            "weapons": dict(),
            "armor": dict(),
            "consumable": dict()
        }
        for slot in self.weapon_slots:
            if slot.item:
                key, value = list(slot.item.save().items())[0]
                slots["weapons"][key] = value
        for slot in self.armor_slots:
            if slot.item:
                key, value = list(slot.item.save().items())[0]
                slots["armor"][key] = value
        for slot in self.consumable_slots:
            if slot.item:
                key, value = list(slot.item.save().items())[0]
                slots["consumable"][key] = value
        return slots

    def set_all_categories(self):
        """Used to define the different categories of items"""
        for categorie in STORE_CATEGORIES:
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
        step, min_x, max_x, min_y, max_y = self.create_slots(
            WEAPONS_COLS, (len(self.chosen_weapons) - 1) // WEAPONS_COLS + 1, 0)
        for x in range(min_x, max_x, step):
            for y in range(min_y, max_y, step):
                self.weapon_slots.append(StoreSlot(x, y, STORE_TILESIZE, WHITE))

    def create_armor_slots(self):
        """Create slots for the Armor category"""
        step, min_x, max_x, min_y, max_y = self.create_slots(
            ARMOR_COLS, (len(self.chosen_armor) - 1) // ARMOR_COLS + 1, 100)
        for x in range(min_x, max_x, step):
            for y in range(min_y, max_y, step):
                self.armor_slots.append(StoreSlot(x, y, STORE_TILESIZE, WHITE))

    def create_consumable_slots(self):
        """Create slots for the Consumable category"""
        step, min_x, max_x, min_y, max_y = self.create_slots(
            CONSUMABLE_COLS, (len(self.chosen_consumables) - 1) // CONSUMABLE_COLS + 1, 200)
        for x in range(min_x, max_x, step):
            for y in range(min_y, max_y, step):
                self.consumable_slots.append(StoreSlot(x, y, STORE_TILESIZE, WHITE))

    def add_all_items(self):
        """Add all items all category"""
        self.add_all_weapons()
        self.add_all_armors()
        self.add_all_consumables()

    def add_all_weapons(self):
        """Add all items to the weapon category
        """
        self.weapons = list()
        for key, value in self.chosen_weapons:
            data = Weapon(
                key,
                ITEMS[value['image_name']],
                value['image_name'],
                value['price'],
                value['slot'],
                value['type'],
                value['weight'],
                value['number_dice'],
                value['dice_value'],
                value['scope']
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
        for key, value in self.chosen_armor:
            data = Armor(
                key,
                ITEMS[value['image_name']],
                value['image_name'],
                value['price'],
                value['weight'],
                value['shield'],
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
        for key, value in self.chosen_consumables:
            data = Consumable(
                key,
                ITEMS[value['image_name']],
                value['image_name'],
                value['price'],
                value['weight'],
                value["heal"],
                value["shield"])
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
            self.draw_title(screen)
            for slot in self.get_all_slots():
                slot.draw(screen)
            slot_moving = None
            for slot in self.get_all_slots():
                if slot.item and not slot.item.is_moving:
                    slot.draw_items(screen)
                elif slot.item:
                    slot_moving = slot
            if slot_moving:
                slot_moving.draw_items(screen)

    def draw_title(self, screen):
        """Used to draw title

        Args:
            screen (Surface)
        """
        self.game.draw_text(
            "Items", self.game.title_font, 48, YELLOW_LIGHT, 1 * WIDTH // 4, HEIGHT // 3 -
            ((STORE_TILESIZE + STORE_SLOT_GAP) * 3) // 2 + STORE_SLOT_GAP, align="n", screen=screen)

    def move_item(self):
        """Drag function, makes an item following the mouse

        Args:
            screen (Surface)
        """
        mouse_pos = pg.mouse.get_pos()

        for slot in self.get_all_slots():
            if slot.rect.collidepoint(
                    mouse_pos) and slot.item is not None and self.moving_item is None:
                logger.info("Move %s from the shop", slot.item)
                slot.item.is_moving = True
                self.moving_item = slot.item
                self.moving_item_slot = slot
                break

    def place_item(self, inventory):
        """Place a item in the inventory"""
        logger.info("Place %s from the store in the inventory", self.moving_item)
        data = None

        if self.moving_item is not None:
            data = self.get_item(self.moving_item)
            inventory.place_item(data)
            self.moving_item_slot.item = None
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
                if slot.rect.collidepoint(mouse_pos):
                    if slot.item:
                        if action == STORE_ACTIONS['get']:
                            logger.info('%s bought', slot.item.name)
                            data = self.get_item(slot.item)
                            slot.item = None
                            player.inventory.add_item(data)
                        elif action == STORE_ACTIONS['get_equip']:
                            if isinstance(slot.item, Equipable):
                                data = self.get_item(slot.item)
                                slot.item = None
                                player.inventory.equip_item(data)
                            else:
                                logger.info('Action can not be done')
                        elif action == STORE_ACTIONS['get_use']:
                            if isinstance(slot.item, Consumable):
                                data = self.get_item(slot.item)
                                slot.item = None
                                player.inventory.use_item(data)
                            else:
                                logger.info('Action can not be done')
                        else:
                            logger.info('Action can not be done')

    def get_item(self, item):
        """Buy an item

        Args:
            item (Item)
        """
        logger.info("Get %s from store", item)
        data = deepcopy(item)
        return data

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

    def is_clicked(self, mouse_pos):
        """Check if the shop is clicked"""
        for slot in self.get_all_slots():
            if slot.rect.collidepoint(mouse_pos):
                return True

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
        step = STORE_TILESIZE + STORE_SLOT_GAP
        min_x = WIDTH // 4 - (step * cols) // 2 + STORE_SLOT_GAP
        max_x = WIDTH // 4 + (step * cols) // 2
        min_y = HEIGHT // 3 - (step * rows) // 2 + STORE_SLOT_GAP + offset_y
        max_y = HEIGHT // 3 + (step * rows) // 2 + offset_y
        return (step, min_x, max_x, min_y, max_y)


class StoreSlot(Container):
    """A slot from the shop"""

    def draw_items(self, screen):
        """Draw an image on a shop slot

        Args:
            screen (Surface)
        """
        if self.item is not None and not self.item.is_moving:
            offset = 12
            image = pg.transform.scale(self.item.image, (self.size - offset, self.size - offset))
            image_x = image.get_width()
            image_y = image.get_height()

            # pg.draw.rect(screen, (0, 255, 0), pg.Rect(self.x + offset / 2, self.y + offset / 2, image_x, image_y), 1)

            screen.blit(image, (self.x + offset / 2, self.y + offset / 2))

        if self.item is not None and self.item.is_moving:
            mouse_pos = pg.mouse.get_pos()
            image = pg.transform.scale(self.item.image, (self.size, self.size))
            image_x = image.get_width()
            image_y = image.get_height()

            screen.blit(image, (mouse_pos[0] - image_x // 2, mouse_pos[1] - image_y // 2))
