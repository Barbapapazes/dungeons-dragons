"""Game screen"""

from sprites.obstacle import Obstacle
from temp.enemy import Enemy
import pygame as pg
from os import path
from math import sqrt
from window import _State
from logger import logger
from sprites.player import Player
from utils.tilemap import TiledMap, Camera, Minimap
from config.window import WIDTH, HEIGHT, TILESIZE
from config.colors import LIGHTGREY, BLACK, WHITE
from config.screens import CREDITS, MENU, GAME, TRANSITION_IN, TRANSITION_OUT
from config.sprites import WEAPONS, ARMOR
from config.versus import MALUS_ARC, TOUCH_HAND
from inventory.inventory import Armor, Weapon
from utils.shortcuts import key_for
from versus.versus import Versus

vec = pg.math.Vector2


# temp


class Game(_State):
    """Game screen"""

    def __init__(self):
        self.name = GAME
        super(Game, self).__init__(self.name)
        self.next = CREDITS

        self.all_sprites = None

        #####For_versus######
        self.action = None
        self.versus = Versus()
        self.selectEnemy = None
        self.isVersus = False

        # temp
        #######END_Versus#####

        self.states_dict = self.make_states_dict()

    def startup(self, dt, game_data):
        self.dt = dt
        self.game_data = game_data
        self.walls = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()

        self.en1 = Enemy(self, 10, 4, "Boot n1")
        self.en2 = Enemy(self, 11, 7, "Boot n2")
        self.enemy = [self.en1, self.en2]

        super().setup_transition()

        # Temporaire
        # think how this will be used with the menu
        # add a logger inside the inventory (for each keys or mouse move)
        # items_folder = path.join(self.img_folder, 'items')
        # weapons = list()
        # for key, value in WEAPONS.items():
        #     data = Weapon(
        #         key, path.join(items_folder, value['image']),
        #         value['weight'],
        #         value['slot'],
        #         value['type'],
        #         value['nb_d'],
        #         value['val_d'],
        #         value['scope'])
        #     weapons.append(data)
        #     self.player.inventory.add_item(data)

        # hp_potion = Consumable('img/potionRed.png', 2, 30)
        # helmet_armor = Armor('helmet armor', 'assets/img/items/helmet.png', 10, 20, 'head')
        # chest_armor = Armor('img/chest.png', 10, 40, 'chest')
        # upg_helmet_armor = Armor('img/upg_helmet.png', 10, 40, 'head')
        # upg_chest_armor = Armor('img/upg_chest.png', 10, 80, 'chest')
        # self.player.inventory.add_item(helmet_armor)
        self.new()

    def new(self):
        """Create a new game"""
        self.map = TiledMap(path.join(self.saved_maps, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.minimap = Minimap(self.map_img, 225, self.map_rect.width / self.map_rect.height)
        self.camera = Camera(self.map.width, self.map.height)
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

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
            if key_for(self.game_data["shortcuts"]["game"]["menu"]["keys"], event):
                self.player.inventory.display_inventory = False
                super().toggle_sub_state('menu')
            if key_for(self.game_data["shortcuts"]["game"]["inventory"]["keys"], event):
                logger.info("Toggle inventory from player")
                self.player.inventory.toggle_inventory()
                super().toggle_sub_state('inventory')
            if event.key == pg.K_p:
                logger.info("Toggle the shop")
                self.player.shop.toggle_shop()
                self.player.inventory.toggle_inventory()
                super().toggle_sub_state('shop')

            if event.key == pg.K_l:
                life = {'Player': self.player.HP, 'en1': self.en1.HP, 'en2': self.en2.HP}
                logger.info(life)

            if event.key == pg.K_TAB:
                """Simulate begin versus"""
                logger.info("Begin Versus")
                if not self.isVersus:
                    self.isVersus = True
                else:
                    self.isVersus = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 3:
                if self.player.inventory.display_inventory:

                    mouse_pos = pg.mouse.get_pos()
                    if self.state == 'inventory':
                        self.player.inventory.check_slot(self.screen, mouse_pos)
                        logger.info("Auto move an item")
                    elif self.state == 'shop':
                        self.player.shop.check_slot(self.screen, self.player, mouse_pos)
            if event.button == 1:
                if self.state == 'inventory':
                    if self.player.inventory.display_inventory:
                        logger.info("Select an item from the inventory")
                        self.player.inventory.move_item(self.screen)

                if self.isVersus:  # cursor
                    mouse_pos = pg.mouse.get_pos()
                    if self.versus.isATK(mouse_pos) and self.action == None:
                        self.action = "ATK"
                    if self.action == "select_enemy":
                        self.selectEnemy = self.versus.selectEnemy(self.enemy, mouse_pos)
                        if self.selectEnemy != None:
                            self.action = None

        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                if self.state == 'inventory':
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
        if self.isVersus:
            self.versus_action()

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
        self.draw
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.screen.blit(self.dim_screen, (0, 0))
        self.player.shop.draw(self.screen)
        self.player.inventory.draw(self.screen)

    def versus_action(self):
        self.versus.draw(self.screen)

        # Choose action
        if(self.action == 'ATK'):
            logger.info("Your action is Attack")
            self.action = "select_enemy"
            logger.info("Select your cible")

        if self.selectEnemy != None:
            dmg = 0
            logger.debug(self.selectEnemy.name)
            if self.player.weapon != None:  # check if player had a weapon

                if self.player.weapon.wpn_type == "sword" and self.player.weapon.scope >= self.distance(
                        self.player, self.selectEnemy):
                    if self.player.throwDice(self.player.STR):
                        dmg = self.player.weapon.attack()
                    else:
                        logger.info("You miss your cible")

                elif self.player.weapon.wpn_type == "arc":
                    dist = self.distance(self.player, self.selectEnemy)
                    scope = self.player.weapon.scope
                    if scope < dist:
                        malus = -((dist-scope)//TILESIZE)*MALUS_ARC
                    else:
                        malus = 0
                    logger.debug("dist: %i scp: %i  malus: %i", dist, scope, malus)
                    if self.player.throwDice(self.player.DEX, malus):
                        dmg = self.player.weapon.attack()
                    else:
                        logger.info("You miss your cible")

                else:
                    logger.info("It's too far away ")
            else:
                if self.distance(self.player, self.selectEnemy)//TILESIZE <= TOUCH_HAND:
                    dmg = 2  # attack with any weapon
                else:
                    logger.info("It's too far away ")

            self.selectEnemy.HP -= dmg
            if dmg != 0:
                logger.info("The enemy %s lose %i HP", self.selectEnemy.name, dmg)

            self.selectEnemy = None

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

        self.screen.blit(self.minimap.draw(self.player), (WIDTH - self.minimap.width, HEIGHT - self.minimap.height))

        super().transtition_active(self.screen)

    def distance(self, player, enemy):
        return sqrt((enemy.x-player.rect.center[0])**2 + (enemy.y-player.rect.center[1])**2)
