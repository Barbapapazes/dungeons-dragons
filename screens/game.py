"""Game screen"""

import pygame as pg
from os import path
from window import _State
from logger import logger
from sprites.player import Player
from utils.tilemap import TiledMap, Camera
from config.window import WIDTH, HEIGHT, TILESIZE
from config.colors import LIGHTGREY, BLACK, WHITE, CYAN
from config.screens import CREDITS, MENU, GAME, TRANSITION_IN, TRANSITION_OUT
from config.sprites import WEAPONS
from inventory.inventory import Armor, Weapon
from utils.shortcuts import key_for


class Game(_State):
    """Game screen"""

    def __init__(self):
        self.name = GAME
        super(Game, self).__init__(self.name)
        self.next = None

        self.all_sprites = None
        self.action = None

        self.states_dict = self.make_states_dict()

    def startup(self, dt, game_data):
        self.dt = dt
        self.game_data = game_data
        self.all_sprites = pg.sprite.Group()

        self.player = Player(self, 2, 4)
        super().setup_transition()

        # Temporaire
        # think how this will be used with the menu
        # add a logger inside the inventory (for each keys or mouse move)
        items_folder = path.join(self.img_folder, 'items')
        weapons = list()
        for key, value in WEAPONS.items():
            data = Weapon(
                key, path.join(items_folder, value['image']),
                value['weight'],
                value['slot'],
                value['type'])
            weapons.append(data)
            self.player.inventory.add_item(data)

        # hp_potion = Consumable('img/potionRed.png', 2, 30)
        helmet_armor = Armor('helmet armor', 'assets/img/items/helmet.png', 10, 20, 'head')
        # chest_armor = Armor('img/chest.png', 10, 40, 'chest')
        # upg_helmet_armor = Armor('img/upg_helmet.png', 10, 40, 'head')
        # upg_chest_armor = Armor('img/upg_chest.png', 10, 80, 'chest')
        self.player.inventory.add_item(helmet_armor)
        self.new()

    def new(self):
        """Create a new game"""
        self.map = TiledMap(path.join(self.saved_maps, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.camera = Camera(self.map.width, self.map.height)

    def make_states_dict(self):
        """Make the dictionary of state methods for the level.


        Returns:
            object: define all the possible states for a screen
        """
        states_dict = {TRANSITION_IN: self.transition_in,
                       TRANSITION_OUT: self.transition_out,
                       'normal': self.normal_run,
                       'menu': self.menu_run,
                       'inventory': self.inventory_run
                       'mode_combat':self.mode_combat
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
            if key_for(self.game_data["shortcuts"]["game"]["menu"]["keys"], event):
                self.player.inventory.display_inventory = False
                super().toggle_sub_state('menu')
            if key_for(self.game_data["shortcuts"]["game"]["inventory"]["keys"], event):
                logger.info("Toggle inventory from player")
                self.player.inventory.toggle_inventory()
                super().toggle_sub_state('inventory')

            if event.key== pg.K_TAB:
                """Simulate begin versus"""
                logger.info("Begin Versus")
                sub_state ='normal' if self.state == 'mode_combat' else 'mode_combat'
                super().set_state(sub_state)

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 3:
                if self.player.inventory.display_inventory:
                    logger.info("Auto move an item")
                    mouse_pos = pg.mouse.get_pos()
                    self.player.inventory.check_slot(self.screen, mouse_pos)
            if event.button == 1:
                if self.player.inventory.display_inventory:
                    logger.info("Select an item from the inventory")
                    self.player.inventory.move_item(self.screen)
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                if self.player.inventory.display_inventory:
                    logger.info("Place an item")
                    self.player.inventory.place_item(self.screen)

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

    def mode_combat(self):
        self.draw_text("GO",self.title_font,35,CYAN,WIDTH // 2, HEIGHT // 2, 'top')

        #Choose action
        if(self.action=='ATK'):
            logger.critical("cc")
        
        
        


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
        self.camera.update(self.player)

    def draw(self):
        """Draw all"""
        # self.screen.fill(BLACK)
        # self.draw_grid(self.screen)
        # self.all_sprites.draw(self.screen)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        super().transtition_active(self.screen)

