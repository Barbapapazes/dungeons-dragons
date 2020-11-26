"""Game screen"""

import pygame as pg
from os import path
from window import _State
from logger import logger
from sprites.player import Player
from config.window import WIDTH, HEIGHT, TILESIZE
from config.colors import LIGHTGREY, BLACK, WHITE
from config.screens import CREDITS, MENU, GAME, TRANSITION_IN, TRANSITION_OUT
from config.sprites import WEAPONS, ARMOR
from inventory.inventory import Armor, Weapon

from popup_menu import PopupMenu, NonBlockingPopupMenu


class Game(_State):
    """Game screen"""

    def __init__(self):
        self.name = GAME
        super(Game, self).__init__(self.name)
        self.next = None

        self.all_sprites = None

        self.states_dict = self.make_states_dict()

    def startup(self, dt, game_data):
        self.dt = dt
        self.game_data = game_data
        self.all_sprites = pg.sprite.Group()

        self.player = Player(self, 2, 4)
        super().setup_transition()




    def make_states_dict(self):
        """Make the dictionary of state methods for the level.


        Returns:
            object: define all the possible states for a screen
        """
        states_dict = {TRANSITION_IN: self.transition_in,
                       TRANSITION_OUT: self.transition_out,
                       'normal': self.normal_run,
                       'menu': self.menu_run,
                       'inventory': self.inventory_run,
                       'shop': self.shop_run
                       }

        return states_dict

    def get_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.next = MENU
                super().set_state(TRANSITION_OUT)
            if event.key == pg.K_RIGHT:
                self.next = CREDITS
                super().set_state(TRANSITION_OUT)

        if event.type == pg.KEYUP:
            if event.key == pg.K_m:
                self.player.inventory.display_inventory = False
                super().toggle_sub_state('menu')
            if event.key == pg.K_i:
                logger.info("Toggle inventory from player")
                self.player.shop.display_shop = False
                self.player.inventory.display_inventory = False
                self.player.inventory.toggle_inventory()
                super().toggle_sub_state('inventory')
            if event.key == pg.K_p:
                logger.info("Toggle the shop")
                self.player.inventory.display_inventory = False 
                self.player.shop.toggle_shop()
                self.player.inventory.toggle_inventory()
                super().toggle_sub_state('shop')
                
        """When the inventory state is running"""
        if self.state == 'inventory':
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    logger.info("Select an item from the inventory")
                    self.player.inventory.move_item(self.screen)
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    logger.info("Place an item")
                    self.player.inventory.place_item(self.screen)
                elif event.button == 3:
                    self.mouse_pos = pg.mouse.get_pos()
                    PopupMenu(self.player.inventory.menu_data)
            elif event.type == pg.USEREVENT:
                # print ('menu event: %s.%d: %s' % (event.name,event.item_id,event.text))
                if event.code == 'MENU':
                    if (event.name, event.text) == ('Inventory', 'Equip'):
                        self.player.inventory.check_slot('Equip', self.screen, self.mouse_pos)
                    if (event.name, event.text) == ('Inventory', 'Unequip'):
                        self.player.inventory.check_slot('Unequip', self.screen, self.mouse_pos)
                    if (event.name, event.text) == ('Inventory', 'Use'):
                        self.player.inventory.check_slot('Use', self.screen, self.mouse_pos)
                    if (event.name, event.text) == ('Inventory', 'Throw'):
                        self.player.inventory.check_slot('Throw', self.screen, self.mouse_pos)

        """When the shop state is running"""
        if self.state == 'shop':
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 3:
                    self.mouse_pos = pg.mouse.get_pos()
                    PopupMenu(self.player.shop.menu_data)
                elif event.button == 1:
                    logger.info("Place an item")
                    self.player.inventory.place_item(self.screen)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    logger.info("Select an item from the inventory")
                    self.player.inventory.move_item(self.screen)
            elif event.type == pg.USEREVENT:
                # print ('menu event: %s.%d: %s' % (event.name,event.item_id,event.text))
                if event.code == 'MENU':
                    if event.name == 'Shop' and event.text in self.player.shop.menu_data:
                        self.player.shop.check_slot(event.text, self.screen, self.player, self.mouse_pos)


    def run(self, surface, keys, mouse, dt):
        """Run states"""
        self.screen = surface
        self.dt = dt
        update_level = self.states_dict[self.state]
        if self.state != 'normal':
            self.draw()
        update_level()

    def normal_run(self):
        """Run the normal state"""
        self.update()
        self.draw()
        self.check_for_menu()

    def menu_run(self):
        """Run the menu state"""
        self.draw()
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.screen.blit(self.dim_screen, (0, 0))
        self.draw_text("C'est un sub-state ! Un menu dans l'écran game",
                       self.title_font, 15, WHITE, WIDTH // 2, HEIGHT // 2, 'center')

    def inventory_run(self):
        """Run the inventory state"""
        self.draw()
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.screen.blit(self.dim_screen, (0, 0))
        self.player.inventory.draw(self.screen)

    def shop_run(self):
        """Run the shop state"""
        self.draw
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.screen.blit(self.dim_screen, (0, 0))
        self.player.shop.draw(self.screen)
        self.player.inventory.draw(self.screen)

    def check_for_menu(self):
        """Check if the user want to access to the menu"""

    @staticmethod
    def draw_grid(surface):
        """Draw a grid in the background"""
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(surface, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(surface, LIGHTGREY, (0, y), (WIDTH, y))

    def update(self):
        """Update all"""
        self.all_sprites.update()

    def draw(self):
        """Draw all"""
        self.screen.fill(BLACK)
        self.draw_grid(self.screen)
        self.all_sprites.draw(self.screen)

        super().transtition_active(self.screen)
