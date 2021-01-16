"""Shop"""

import pygame as pg
from logger import logger
from store.store import Store
from inventory.inventory import Consumable, EquipableSlot, InventorySlot, Equipable
from utils.container import Container
from config.store import SHOP_ACTIONS, SHOP_MENU
from config.inventory import ACTIONS as INVENTORY_ACTIONS


class Shop(Store):
    """Represent a shop"""

    def __init__(self, game, consumable=None, weapons=None, armor=None):
        """Create the shop
        """
        super(Shop, self).__init__(game, consumable, weapons, armor, menu_data=SHOP_MENU)

    def place_item(self, inventory):
        """Place a item in the inventory"""
        logger.info("Place %s from the store in the inventory", self.moving_item)
        data = None

        if self.moving_item is not None:
            data = self.get_item(self.moving_item, inventory.player)
            inventory.place_item(data, from_shop=True)
            self.moving_item.is_moving = False
            self.moving_item = None
            self.moving_item_slot = None
        else:
            pass
        if inventory.find_item(data) == None and data:
            inventory.player.gold += data.price

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
                        if action == SHOP_ACTIONS['buy']:
                            logger.info('%s bought', slot.item.name)
                            data = self.get_item(slot.item, player)
                            player.inventory.add_item(data)
                        elif action == SHOP_ACTIONS['buy_equip']:
                            if isinstance(slot.item, Equipable):
                                data = self.get_item(slot.item, player)
                                player.inventory.equip_item(data)
                            else:
                                logger.info('Action can not be done')
                        elif action == SHOP_ACTIONS['buy_use']:
                            if isinstance(slot.item, Consumable):
                                data = self.get_item(slot.item, player)
                                player.inventory.use_item(data)
                            else:
                                logger.info('Action can not be done')
                        else:
                            logger.info('Action can not be done')

        for slot in player.inventory.get_all_slots():
            if isinstance(slot, InventorySlot):
                if slot.rect.collidepoint(mouse_pos):
                    if slot.item:
                        if action == INVENTORY_ACTIONS['sell']:
                            logger.info('%s sold', slot.item.name)
                            self.sell_item(slot.item, player)
                            slot.item = None
                        elif action in list(SHOP_ACTIONS['equip']) + list(SHOP_ACTIONS['unequip'])+list(SHOP_ACTIONS['use']):
                            player.inventory.check_slot(action, screen, mouse_pos)
                        else:
                            logger.info('Action can not be done')
            elif isinstance(slot, EquipableSlot):
                if slot.rect.collidepoint(mouse_pos):
                    if slot.item is not None:
                        if action == INVENTORY_ACTIONS['sell']:
                            logger.info('%s sold', slot.item.name)
                            player.inventory.unequip_item(slot.item)
                            self.sell_item(slot.item, player)
                            slot.item = None
                    else:
                        logger.info('Action can not be done')

    def get_item(self, item, player):
        """Buy an item

        Args:
            item (Item)
            player (Player)
        """
        if item.price > player.gold:
            logger.info("You have not enough money")
            return
        else:
            player.gold -= item.price
            logger.info("Buy %s from shop", item)
            return super().get_item(item)

    def sell_item(self, item, player):
        """Sell an item

        Args:
            item (Item)
            player (Player)
        """
        if item is not None:
            logger.info("Sell %s", item)
            player.gold += item.price


class ShopSlot(Container):
    """A slot from the shop"""

    def draw_items(self, screen):
        """Draw an image on a shop slot

        Args:
            screen (Surface)
        """
        if self.item is not None:
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
