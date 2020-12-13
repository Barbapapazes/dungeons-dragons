"""Game screen"""

from math import sqrt
from os import path
import pygame as pg
from components.popup_menu import PopupMenu
from window import _State
from logger import logger
from sprites.player import Player
from sprites.obstacle import Obstacle
from utils.tilemap import TiledMap, Camera, Minimap
from utils.shortcuts import key_for
from config.window import WIDTH, HEIGHT, TILESIZE
from config.colors import LIGHTGREY, WHITE
from config.screens import CREDITS, MENU, GAME, TRANSITION_IN, TRANSITION_OUT
from config.shop import ACTIONS
from utils.turn_manager import TurnManager
# from config.sprites import WEAPONS, ARMOR
# from config.versus import MALUS_ARC, TOUCH_HAND, DMG_ANY_WEAPON
# from inventory.inventory import Armor, Weapon
from config.versus import MALUS_ARC, TOUCH_HAND, DMG_ANY_WEAPON, NUM_ACT_BEGIN
from temp.enemy import Enemy
from versus.versus import Versus
from versus.sort import Sort
from versus.sort import collisionZoneEffect

vec = pg.math.Vector2


class Game(_State):
    """Game screen"""

    def __init__(self):
        self.name = GAME
        super(Game, self).__init__(self.name)
        self.next = CREDITS

        self.all_sprites = None
        self.versus = Versus(self)

        self.turn_manager = TurnManager()

        self.states_dict = self.make_states_dict()

    def startup(self, dt, game_data):
        self.dt = dt
        self.game_data = game_data
        self.walls = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.zoneEffect = pg.sprite.Group()

        self.en1 = Enemy(self, 10, 4, "Boot n1")
        self.en2 = Enemy(self, 11, 7, "Boot n2")
        self.enemy = [self.en1, self.en2]

        super().setup_transition()

        self.new()

    def new(self):
        """Create a new game"""
        self.map = TiledMap(path.join(self.saved_maps, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.minimap = Minimap(
            self.map_img,
            225,
            self.map_rect.width /
            self.map_rect.height, self.game_data["minimap"]["fog"], self.game_data["minimap"]["cover"])
        self.camera = Camera(self.map.width, self.map.height)
        self.versus.setCamera(self.camera)

        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(
                tile_object.x + tile_object.width / 2,
                tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                if len(self.turn_manager.players) < len(self.game_data["game_data"]["heros"]):
                    _x = obj_center.x if not ("last_pos" in self.game_data["game_data"]["heros"][
                        len(self.turn_manager.players)].keys()) else self.game_data["game_data"]["heros"][
                        len(self.turn_manager.players)]["last_pos"]["x"]
                    _y = obj_center.y if not ("last_pos" in self.game_data["game_data"]["heros"][
                        len(self.turn_manager.players)].keys()) else self.game_data["game_data"]["heros"][
                        len(self.turn_manager.players)]["last_pos"]["y"]
                    self.turn_manager.players.append(
                        Player(
                            self, self.game_data["game_data"]["heros"][len(self.turn_manager.players)]["class"],
                            _x, _y))
            if tile_object.name == 'wall':
                Obstacle(
                    self,
                    tile_object.x,
                    tile_object.y,
                    tile_object.width,
                    tile_object.height)

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
        fireBall = Sort('fireBall', 'assets/img/items/fireBall.png', 10, 'sort', 5, 'fire', 10, 2, 4, 2)
        self.turn_manager.active_player().inventory.add_item(fireBall)

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
            self.toggle_states(event)
            if event.key == pg.K_t:
                self.turn_manager.add_turn()

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:

                if self.state == 'inventory':
                    if self.turn_manager.active_player().inventory.display_inventory:
                        logger.info("Select an item from the inventory")
                        self.turn_manager.active_player().inventory.move_item()

        self.event_versus(event)
        self.events_inventory(event)
        self.events_shop(event)

    def event_versus(self, event):

        if event.type == pg.KEYUP:
            if event.key == pg.K_l:
                life = {
                    'Player': self.turn_manager.active_player().HP,
                    'mana': self.turn_manager.active_player().MP,
                    'en1': self.en1.HP,
                    'en2': self.en2.HP}
                logger.info(life)

            if event.key == pg.K_TAB:
                """Simulate begin versus"""
                self.versus.log("Begin Versus")
                self.turn_manager.active_player().numberOfAction = NUM_ACT_BEGIN

                if not self.versus.isVersus:
                    self.versus.begin()
                else:
                    self.versus.end()

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:

                if self.versus.isVersus:
                    mouse_pos = pg.mouse.get_pos()
                    self.versus.setMouse(mouse_pos)
                    if self.versus.isATK() and not self.versus.isProgress():
                        self.versus.setAction("ATK")
                    if self.versus.action == "select_enemy":
                        self.versus.selectedEnemy(self.enemy)
                        if self.versus.selectEnemy is not None:
                            self.versus.setAction(None)
                    if self.versus.isMOV() and not self.versus.isProgress():
                        self.versus.setAction("Move")
                    if self.versus.CheckMove(self.turn_manager.active_player()) and self.versus.action == 'Move':
                        self.versus.setAction("Move_autorised")
                    if self.versus.action == "Select_pos_sort":
                        self.versus.createZone(self.turn_manager.active_player())
                    if self.versus.isSRT() and not self.versus.isProgress():
                        if self.versus.CheckSort(self.turn_manager.active_player()):
                            self.versus.setAction("Select_pos_sort")
                        else:
                            self.versus.log("No sort select OR you don't have enough mana")

    def events_inventory(self, event):
        """When the shop state is running"""
        if self.state == 'inventory':
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.turn_manager.active_player().inventory.move_item()
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.turn_manager.active_player().inventory.place_item()
                elif event.button == 3:
                    self.mouse_pos = pg.mouse.get_pos()
                    PopupMenu(self.turn_manager.active_player().inventory.menu_data)
            elif event.type == pg.USEREVENT:
                if event.code == 'MENU':
                    self.inventory_events(event)

    def inventory_events(self, event):
        """Used to manage all event"""
        if event.name == "inventory":
            self.turn_manager.active_player().inventory.check_slot(event.text, self.mouse_pos)
            if event.text in ["sell"]:
                self.turn_manager.active_player().shop.check_slot(
                    event.text, self.screen, self.turn_manager.active_player(), self.mouse_pos)

    def events_shop(self, event):
        """When the shop state is running"""
        if self.state == 'shop':
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 3:
                    self.mouse_pos = pg.mouse.get_pos()
                    if self.turn_manager.active_player().shop.is_clicked(self.mouse_pos):
                        PopupMenu(self.turn_manager.active_player().shop.menu_data)
                    elif self.turn_manager.active_player().inventory.is_clicked(self.mouse_pos):
                        PopupMenu(self.turn_manager.active_player().inventory.menu_data)
                elif event.button == 1:
                    self.turn_manager.active_player().shop.place_item(self.turn_manager.active_player().inventory)
                    self.turn_manager.active_player().inventory.place_item()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.turn_manager.active_player().shop.move_item()
                    self.turn_manager.active_player().inventory.move_item()
            elif event.type == pg.USEREVENT:
                if event.code == 'MENU':
                    if event.name == 'shop' and event.text in self.turn_manager.active_player().shop.menu_data:
                        self.turn_manager.active_player().shop.check_slot(
                            event.text, self.screen, self.turn_manager.active_player(), self.mouse_pos)
                    self.inventory_events(event)

    def toggle_states(self, event):
        """Use to toggle the state of all states"""
        if key_for(self.game_data["shortcuts"]["game"]["menu"]["keys"], event):
            logger.info("Toggle the sub-menu")
            self.turn_manager.active_player().inventory.display_inventory = False
            self.turn_manager.active_player().shop.display_shop = False
            super().toggle_sub_state('menu')
        if key_for(self.game_data["shortcuts"]["game"]
                   ["inventory"]["keys"], event):
            logger.info("Toggle inventory from turn_manager.active_player()")
            self.turn_manager.active_player().shop.display_shop = False
            self.turn_manager.active_player().inventory.display_inventory = True
            super().toggle_sub_state('inventory')
        if event.key == pg.K_p:
            logger.info("Toggle the shop")
            self.turn_manager.active_player().shop.display_shop = True
            self.turn_manager.active_player().inventory.display_inventory = True
            super().toggle_sub_state('shop')

    def run(self, surface, keys, mouse, dt):
        """Run states"""
        self.screen = surface
        self.versus.setSurface(self.screen)
        self.dt = dt
        update_level = self.states_dict[self.state]
        if self.state != 'normal':
            self.draw()
        update_level()

    def normal_run(self):
        """Run the normal state"""
        if self.versus.isVersus:
            self.draw()
            self.versus_action()
            if (self.versus.action == "Move_autorised"):
                self.update()
        else:
            self.update()
            self.draw()

        self.check_for_menu()

    def menu_run(self):
        """Run the menu state"""
        self.draw()
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.screen.blit(self.dim_screen, (0, 0))
        self.draw_text(
            "C'est un sub-state ! Un menu dans l'écran game",
            self.title_font,
            15,
            WHITE,
            WIDTH // 2,
            HEIGHT // 2,
            'center')

    def inventory_run(self):
        """Run the inventory state"""
        self.draw()
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.screen.blit(self.dim_screen, (0, 0))
        self.turn_manager.active_player().inventory.draw(self.screen)

    def shop_run(self):
        """Run the shop state"""
        self.draw()
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.screen.blit(self.dim_screen, (0, 0))
        self.turn_manager.active_player().inventory.draw(self.screen)
        self.turn_manager.active_player().shop.draw(self.screen)

    def versus_action(self):

        if self.turn_manager.active_player().numberOfAction > 0:
            self.versus.draw(self.screen)
            self.versus.ONE_action(self.turn_manager.active_player(), self.screen)
        else:
            self.versus.setAction("Turn_enemy")

        if self.versus.action == "Turn_enemy":
            self.versus.log("Begin turn ENEMY")
            self.versus.log("END turn ENEMY")
            self.turn_manager.active_player().numberOfAction = 5
            self.versus.log("vous avez de nouveau 5 actions")
            collisionZoneEffect(self.turn_manager.active_player(), self)
            self.versus.setAction(None)

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
        # self.all_sprites.update()
        collisionZoneEffect(self.turn_manager.active_player(), self)
        self.turn_manager.update()
        self.camera.update(self.turn_manager.active_player())
        self.minimap.update(self.turn_manager.active_player())
        self.update_game_data()

    def update_game_data(self):
        self.game_data["minimap"] = self.minimap.create_minimap_data()
        self.game_data["game_data"]["heros"][self.turn_manager.turn]["last_pos"] = {
            "x": self.turn_manager.active_player().pos.x, "y": self.turn_manager.active_player().pos.y}

    def draw(self):
        """Draw all"""
        # self.screen.fill(BLACK)
        # self.draw_grid(self.screen)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        for zone in self.zoneEffect:
            zone.draw()

        self.screen.blit(
            self.minimap.create(
                self.turn_manager.active_player(), self.turn_manager.players),
            (WIDTH -
             self.minimap.width,
             HEIGHT -
             self.minimap.height))

        super().transtition_active(self.screen)
