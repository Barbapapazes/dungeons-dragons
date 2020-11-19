"""Game screen"""

import pygame as pg
from os import path
from window import _State
from logger import logger
from sprites.player import Player
from config.window import WIDTH, HEIGHT, TILESIZE
from config.colors import LIGHTGREY, BLACK, WHITE
from config.screens import CREDITS, MENU, GAME, TRANSITION_IN, TRANSITION_OUT
from inventory.inventory import *


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

        self.player1 = Player(self, 2, 4)
        super().setup_transition()

        #Temporaire
        sword_steel = Weapon('img/sword.png', 20, 'weapon', 'sword')
        sword_wood = Weapon('img/swordWood.png', 10, 'weapon', 'sword')
        hp_potion = Consumable('img/potionRed.png', 2, 30)
        helmet_armor = Armor('img/helmet.png', 10, 20, 'head')
        chest_armor = Armor('img/chest.png', 10, 40, 'chest')
        upg_helmet_armor = Armor('img/upg_helmet.png', 10, 40, 'head')
        upg_chest_armor = Armor('img/upg_chest.png', 10, 80, 'chest')
        self.player1.inventory.addItemInv(helmet_armor)
        self.player1.inventory.addItemInv(hp_potion)
        self.player1.inventory.addItemInv(sword_steel)
        self.player1.inventory.addItemInv(sword_wood)
        self.player1.inventory.addItemInv(chest_armor)
        self.player1.inventory.addItemInv(upg_helmet_armor)
        self.player1.inventory.addItemInv(upg_chest_armor)


    def make_states_dict(self):
        """Make the dictionary of state methods for the level.


        Returns:
            object: define all the possible states for a screen
        """
        states_dict = {TRANSITION_IN: self.transition_in,
                       TRANSITION_OUT: self.transition_out,
                       'normal': self.normal_run,
                       'menu': self.menu_run
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
            if event.key == pg.K_b:
                self.player1.inventory.toggleInventory()

        if event.type == pg.KEYUP:
            if event.key == pg.K_m:
                sub_state = 'normal' if self.state == 'menu' else 'menu'
                logger.info('Start sub-state %s in %s', sub_state, self.name)
                super().set_state(sub_state)

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 3:
                if self.player1.inventory.display_inventory:
                    mouse_pos = pg.mouse.get_pos()
                    self.player1.inventory.checkSlot(self.screen, mouse_pos)
            if event.button == 1 :
                if self.player1.inventory.display_inventory:
                    self.player1.inventory.moveItem(self.screen)
        if event.type == pg.MOUSEBUTTONUP :
            if event.button == 1:
                if self.player1.inventory.display_inventory:
                    self.player1.inventory.placeItem(self.screen)



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
        self.screen.fill(BLACK)
        self.draw_text("C'est un sub-state ! Un menu dans l'écran game",
                       self.title_font, 15, WHITE, WIDTH // 2, HEIGHT // 2, 'center')

    def check_for_menu(self):
        """Check if the user want to access to the menu"""

    @staticmethod
    def draw_grid(surface):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(surface, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(surface, LIGHTGREY, (0, y), (WIDTH, y))

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid(self.screen)
        self.all_sprites.draw(self.screen)
        self.player1.inventory.draw(self.screen)

        super().transtition_active(self.screen)
