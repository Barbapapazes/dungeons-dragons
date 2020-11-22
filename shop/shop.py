"""Shop"""

import pygame as pg
from config.window import HEIGHT, WIDTH
from config.colors import WHITE
from config.shop import SHOP_TILESIZE, SHOP_SLOT_GAP, SHOP_CATEGORIES
from config.sprites import CONSUMABLE, WEAPONS, ARMOR, WEAPONS_COLS, WEAPONS_ROWS, CONSUMABLE_COLS, CONSUMABLE_ROWS, ARMOR_COLS, ARMOR_ROWS
from inventory.inventory import Consumable, Weapon, Armor
from os import path

class Shop():

    def __init__(self):

        game_folder = path.dirname('.')
        assets_folder = path.join(game_folder, 'assets')
        img_folder = path.join(assets_folder, 'img')
        self.items_folder = path.join(img_folder, 'items')

        self.categories = []

        self.weapon_slots = []
        self.armor_slots = []
        self.consumable_slots = []

        self.create_slots()
        self.add_all_items()

        self.display_shop = False



    def create_slots(self):
        self.set_all_categories()
        self.create_weapon_slots()
        self.create_armor_slots()
        self.create_consumable_slots()

    def set_all_categories(self):
        """Used to define the different categories of items
        """
        for cat in SHOP_CATEGORIES:
            self.categories.append(cat)

    def create_weapon_slots(self):
        step = SHOP_TILESIZE + SHOP_SLOT_GAP
        print(WEAPONS_COLS, WEAPONS_ROWS)
        min_x = WIDTH // 4 - (step * WEAPONS_COLS) // 2 + SHOP_SLOT_GAP 
        max_x = WIDTH // 4 + (step * WEAPONS_COLS) // 2 
        min_y = HEIGHT // 3 - (step * WEAPONS_ROWS) // 2 + SHOP_SLOT_GAP
        max_y = HEIGHT // 3 + (step * WEAPONS_ROWS) // 2
        # inventory is 1/4 in width
        print(min_x, max_x, min_y, max_y, step)
        for x in range(min_x, max_x, step):
            # inventory is center in height
            for y in range(min_y, max_y, step):
                self.weapon_slots.append(ShopSlot(x, y))

    def create_armor_slots(self):
        step = SHOP_TILESIZE + SHOP_SLOT_GAP
        print(ARMOR_COLS, ARMOR_ROWS)
        min_x = WIDTH // 4 - (step * ARMOR_COLS) // 2 + SHOP_SLOT_GAP
        max_x = WIDTH // 4 + (step * ARMOR_COLS) // 2
        min_y = HEIGHT // 3 - (step * ARMOR_ROWS) // 2 + SHOP_SLOT_GAP + 100
        max_y = HEIGHT // 3 + (step * ARMOR_ROWS) // 2 + 100
        # inventory is 1/4 in width
        print(min_x, max_x, min_y, max_y, step)
        for x in range(min_x,max_x, step):
            # inventory is center in height
            for y in range(min_y, max_y, step):
                self.armor_slots.append(ShopSlot(x, y))

    def create_consumable_slots(self):
        step = SHOP_TILESIZE + SHOP_SLOT_GAP
        print(CONSUMABLE_COLS, CONSUMABLE_ROWS)
        min_x = WIDTH // 4 - (step * CONSUMABLE_COLS) // 2 + SHOP_SLOT_GAP 
        max_x = WIDTH // 4 + (step * CONSUMABLE_COLS) // 2
        min_y = HEIGHT // 3 - (step * CONSUMABLE_ROWS) // 2 + SHOP_SLOT_GAP + 200
        max_y = HEIGHT // 3 + (step * CONSUMABLE_ROWS) // 2 + 200
        # inventory is 1/4 in width
        print(min_x, max_x, min_y, max_y, step)
        for x in range(min_x, max_x, step):
            # inventory is center in height
            for y in range(min_y, max_y, step):
                self.weapon_slots.append(ShopSlot(x, y))


    def get_all_slots(self):
        """Get all slots fro the shop

        Returns:
            list: All slots from an shop
        """
        return self.weapon_slots + self.armor_slots + self.consumable_slots

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

    def toggle_shop(self):
        """Set display_shop to True it if was False and vice versa"""
        self.display_shop = not self.display_shop

    def add_all_items(self):
        self.add_all_weapons()
        self.add_all_armors()
        self.add_all_consumables()

    def add_all_weapons(self):
        """Add all items to the related category
        """
        self.weapons = list()
        for key, value in WEAPONS.items():
            data = Weapon(
                key, path.join(self.items_folder, value['image']),
                value['price'],
                value['weight'],
                value['slot'],
                value['type'])
            self.weapons.append(data)

        for item in self.weapons:
            for slots in self.weapon_slots:
                if slots.item is None:
                    slots.item = item
                    break
                else :
                    continue

    def add_all_armors(self):
        """Add all items to the related category
        """
        self.armors = list()
        for key, value in ARMOR.items():
            data = Armor(
                key, path.join(self.items_folder, value['image']),
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
                else :
                    continue

    def add_all_consumables(self):
        """Add all items to the related category
        """
        self.consumables = list()
        for key, value in CONSUMABLE.items():
            data = Consumable(
                key, path.join(self.items_folder, value['image']),
                value['price'],
                value['weight'])
            self.consumables.append(data)

        for item in self.consumables:
            for slots in self.consumable_slots:
                if slots.item is None:
                    slots.item = item
                    break
                else :
                    continue



class ShopSlot:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.item = None

    def draw(self, screen):
        """Return the drawing of a shopslot

        Args:
            screen (surface)

        Returns:
            Rect: the slot
        """
        return pg.draw.rect(
            screen, WHITE, (self.x, self.y, SHOP_TILESIZE, SHOP_TILESIZE))

    def draw_items(self, screen):
        """Draw an image on a shop slot

        Args:
            screen (Surface)
        """
        if self.item is not None:
            image = pg.image.load(self.item.img).convert_alpha()
            image = pg.transform.scale(image, (SHOP_TILESIZE, SHOP_TILESIZE))
            image_x = image.get_width()
            image_y = image.get_height()

            pg.draw.rect(screen, (0, 255, 0), pg.Rect(self.x, self.y, image_x, image_y), 1)

            screen.blit(image, (self.x, self.y))

