"""Game screen"""

from sprites.chest import Chest
from inventory.inventory import Consumable
from config.sprites import ASSETS_SPRITES, ITEMS
from os import path
from sprites.item import PlacableItem
from inventory.items import Item as InventoryItem
from sprites.door import Door
from versus.logs import Logs
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
from utils.turn_manager import TurnManager
# from config.sprites import WEAPONS, ARMOR
# from config.versus import MALUS_ARC, TOUCH_HAND, DMG_ANY_WEAPON
# from inventory.inventory import Armor, Weapon
from config.versus import MALUS_ARC, TOUCH_HAND, DMG_ANY_WEAPON, NUM_ACT_BEGIN
from versus.versus import VersusManager
from versus.sort import Sort
from versus.sort import collisionZoneEffect
from sprites.enemy import Enemy

vec = pg.math.Vector2


class Game(_State):
    """Game screen"""

    def __init__(self):
        self.name = GAME
        super(Game, self).__init__(self.name)
        self.next = CREDITS

        self.all_sprites = None

        self.logs = Logs(0, 0, 300, 100, self.text_font, 16,  self.draw_text)
        self.turn_manager = TurnManager()
        self.animated = pg.sprite.Group()
        self.versus_manager = VersusManager(self)

        self.press_space = False
        self.chest_open = False
        self.opened_chest = None
        self.seller = False

        self.states_dict = self.make_states_dict()

    def startup(self, dt, game_data):
        self.dt = dt
        self.game_data = game_data
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.chests = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.zoneEffect = pg.sprite.Group()

        # self.en1 = Enemy(self, 10, 4, "Boot n1")
        # self.en2 = Enemy(self, 11, 7, "Boot n2")
        self.en1 = list()
        self.en2 = list()
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
                    _class = self.game_data["game_data"]["heros"][len(self.turn_manager.players)]["class"]
                    _characteristics = self.game_data["game_data"]["heros"][
                        len(self.turn_manager.players)]["characteristics"]
                    _images = ASSETS_SPRITES[_class]
                    self.turn_manager.players.append(
                        Player(self, _x, _y, _class, _characteristics, _images))
            if tile_object.name == "enemy":
                self.turn_manager.enemies.append(
                    Enemy(self, obj_center.x, obj_center.y, "enemy_1", ASSETS_SPRITES["enemy_1"])
                )
            if tile_object.name == 'wall':
                Obstacle(
                    self,
                    tile_object.x,
                    tile_object.y,
                    tile_object.width,
                    tile_object.height)
            if tile_object.name == "door":
                wall = Obstacle(
                    self,
                    tile_object.x,
                    tile_object.y,
                    tile_object.width,
                    tile_object.height)
                Door(self, obj_center.x, obj_center.y, wall)
            if tile_object.name == "silver_key_small":
                PlacableItem(self, obj_center, tile_object.name, ITEMS["key_02c"])
            if tile_object.name == "potion_health_medium":
                PlacableItem(self, obj_center, tile_object.name, ITEMS["potion_02b"])
            if tile_object.name == "chest":
                Chest(self, obj_center.x, obj_center.y)
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
        # fireBall = Sort('fireBall', 'assets/img/items/fireBall.png', 10, 'sort', 5, 'fire', 10, 2, 4, 2)
        # self.turn_manager.active_character().inventory.add_item(fireBall)

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
                       'shop': self.shop_run,
                       'chest': self.chest_run
                       }

        return states_dict

    def get_events(self, event):
        self.press_space = False
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
            if event.key == pg.K_SPACE:
                self.press_space = True

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:

                if self.state == 'inventory':
                    if self.turn_manager.active_character().inventory.display_inventory:
                        logger.info("Select an item from the inventory")
                        self.turn_manager.active_character().inventory.move_item()

        self.event_versus(event)
        self.events_inventory(event)
        self.events_shop(event)
        self.events_chest(event)

    def event_versus(self, event):

        if event.type == pg.KEYUP:
            if event.key == pg.K_l:
                pass
                # life = {
                #     'Player': self.turn_manager.active_character().HP,
                #     'mana': self.turn_manager.active_character().MP,
                #     'en1': self.en1.HP,
                #     'en2': self.en2.HP}
                # logger.info(life)

            if event.key == pg.K_TAB:
                """Simulate begin versus"""
                if self.versus_manager.active:
                    self.versus_manager.finish_versus()
                else:
                    self.versus_manager.start_versus()

                # self.turn_manager.active_character().numberOfAction = NUM_ACT_BEGIN

                # if self.versus.active:
                #     self.versus.finish()
                # else:
                #     self.versus.start()

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                self.versus_manager.events(mouse_pos)
                # faire un fonction event pour le veruss qui regroupe tout ça

                # if self.versus.active:

                #     if Versus.is_clicked(self.versus.attack_btn, mouse_pos) and not self.versus.is_progress():
                #         self.versus.set_action("attack")

                #     if self.versus.action == "select_enemy":
                #         logger.info("Select an enemy")
                #         self.versus.selected_enemy(self.enemy, mouse_pos)

                #     if Versus.is_clicked(self.versus.move_btn, mouse_pos) and not self.versus.is_progress():
                #         self.versus.set_action("move")

                #     if self.versus.CheckMove(self.player, mouse_pos) and self.versus.action == 'move':
                #         self.versus.set_action("move_is_authorized")

                #     if self.versus.action == "pos_spell":
                #         self.versus.createZone(self.player, mouse_pos)

                #     if Versus.is_clicked(self.versus.spell_btn, mouse_pos) and not self.versus.is_progress():
                #         if self.versus.check_spell(self.player):
                #             self.versus.set_action("pos_spell")
                #         else:
                #             self.logs.add_log("No sort select OR you don't have enough mana")

    def events_inventory(self, event):
        """When the shop state is running"""
        if self.state == 'inventory':
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.turn_manager.active_character().inventory.move_item()
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.turn_manager.active_character().inventory.place_item()
                elif event.button == 3:
                    self.mouse_pos = pg.mouse.get_pos()
                    PopupMenu(self.turn_manager.active_character().inventory.menu_data)
            elif event.type == pg.USEREVENT:
                if event.code == 'MENU':
                    self.inventory_events(event)

    def inventory_events(self, event):
        """Used to manage all event"""
        if event.name == "inventory":
            self.turn_manager.active_character().inventory.check_slot(event.text, self.mouse_pos)
            if self.seller:
                if event.text in ["sell"]:
                    self.turn_manager.active_character().shop.check_slot(
                        event.text, self.screen, self.turn_manager.active_character(), self.mouse_pos)

    def events_shop(self, event):
        """When the shop state is running"""
        if self.state == 'shop':  # faudrait foutre tout ça dans une fonction du shop et de l'inventaire
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 3:
                    self.mouse_pos = pg.mouse.get_pos()
                    if self.turn_manager.active_character().shop.is_clicked(self.mouse_pos):
                        PopupMenu(self.turn_manager.active_character().shop.menu_data)
                    elif self.turn_manager.active_character().inventory.is_clicked(self.mouse_pos):
                        PopupMenu(self.turn_manager.active_character().inventory.menu_data)
                elif event.button == 1:
                    self.turn_manager.active_character().shop.place_item(self.turn_manager.active_character().inventory)
                    self.turn_manager.active_character().inventory.place_item()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.turn_manager.active_character().shop.move_item()
                    self.turn_manager.active_character().inventory.move_item()
            elif event.type == pg.USEREVENT:
                if event.code == 'MENU':
                    if event.name == 'shop' and event.text in self.turn_manager.active_character().shop.menu_data:
                        self.turn_manager.active_character().shop.check_slot(
                            event.text, self.screen, self.turn_manager.active_character(), self.mouse_pos)
                    self.inventory_events(event)

    def events_chest(self, event):
        """When the chest state is running"""
        if self.state == 'chest':  # faudrait foutre tout ça dans une fonction du shop et de l'inventaire
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 3:
                    self.mouse_pos = pg.mouse.get_pos()
                    if self.opened_chest.store.is_clicked(self.mouse_pos):
                        PopupMenu(self.opened_chest.store.menu_data)
                    elif self.turn_manager.active_character().inventory.is_clicked(self.mouse_pos):
                        PopupMenu(self.turn_manager.active_character().inventory.menu_data)
                elif event.button == 1:
                    self.opened_chest.store.place_item(self.turn_manager.active_character().inventory)
                    self.turn_manager.active_character().inventory.place_item()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.opened_chest.store.move_item()
                    self.turn_manager.active_character().inventory.move_item()
            elif event.type == pg.USEREVENT:
                if event.code == 'MENU':
                    if event.name == 'store' and event.text in self.opened_chest.store.menu_data:
                        self.opened_chest.store.check_slot(
                            event.text, self.screen, self.turn_manager.active_character(), self.mouse_pos)
                    self.inventory_events(event)

    def toggle_states(self, event):
        """Use to toggle the state of all states"""
        if key_for(self.game_data["shortcuts"]["game"]["menu"]["keys"], event):
            self.seller = False
            logger.info("Toggle the sub-menu")
            self.turn_manager.active_character().inventory.display_inventory = False
            self.turn_manager.active_character().shop.display_shop = False
            super().toggle_sub_state('menu')
        if key_for(self.game_data["shortcuts"]["game"]
                   ["inventory"]["keys"], event):
            logger.info("Toggle inventory from turn_manager.active_character()")
            self.seller = False
            self.turn_manager.active_character().shop.display_shop = False
            self.turn_manager.active_character().inventory.display_inventory = True
            super().toggle_sub_state('inventory')
        if event.key == pg.K_p:
            logger.info("Toggle the shop")
            self.seller = not self.seller
            self.turn_manager.active_character().shop.display_shop = True
            self.turn_manager.active_character().inventory.display_inventory = True
            super().toggle_sub_state('shop')
        # if event.key == pg.K_c:
        #     logger.info("Toggle the chest")
        #     self.turn_manager.active_character().shop.display_shop = True
        #     self.turn_manager.active_character().inventory.display_inventory = True
        #     super().toggle_sub_state('chest')

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
        # if self.versus.active:
        #     # self.versus_update()
        #     if (self.versus.action == "Move_autorised"):
        #         self.update()
        # else:
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
        self.turn_manager.active_character().inventory.draw(self.screen)

    def shop_run(self):
        """Run the shop state"""
        self.draw()
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.screen.blit(self.dim_screen, (0, 0))
        self.turn_manager.active_character().inventory.draw(self.screen)
        self.turn_manager.active_character().shop.draw(self.screen)

    def chest_run(self):
        self.draw()
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.screen.blit(self.dim_screen, (0, 0))
        self.turn_manager.active_character().inventory.draw(self.screen)
        self.opened_chest.store.draw(self.screen)

    # def versus_action(self):

    #     if self.turn_manager.active_character().numberOfAction > 0:
    #         self.versus.draw(self.screen)
    #         self.versus.ONE_action(self.turn_manager.active_character(), self.screen)
    #     else:
    #         self.versus.setAction("Turn_enemy")

    #     if self.versus.action == "Turn_enemy":
    #         self.versus.log("Begin turn ENEMY")
    #         self.versus.log("END turn ENEMY")
    #         self.turn_manager.active_character().numberOfAction = 5
    #         self.versus.log("vous avez de nouveau 5 actions")
    #         collisionZoneEffect(self.turn_manager.active_character(), self)
    #         self.versus.setAction(None)

    def check_for_menu(self):
        """Check if the user want to access to the menu"""

    def update(self):
        """Update all"""
        # self.all_sprites.update()
        self.items.update()
        for sprite in self.all_sprites:
            self.all_sprites.change_layer(sprite, sprite.rect.bottom)
        hits = pg.sprite.spritecollide(self.turn_manager.active_character(), self.doors, False)
        for hit in hits:
            hit.try_open(self.turn_manager.active_character())
        hits = pg.sprite.spritecollide(self.turn_manager.active_character(), self.chests, False)
        if self.press_space:
            for hit in hits:
                hit.try_open(self.turn_manager.active_character())
            self.press_space = False
        hits = pg.sprite.spritecollide(self.turn_manager.active_character(), self.items, False)
        for hit in hits:
            if hit.name == "silver_key_small":
                hit.kill()
                self.turn_manager.active_character().inventory.add_item(InventoryItem(
                    "key", hit.image.copy(), 0, False))
            if hit.name == 'potion_health_medium':
                hit.kill()
                self.turn_manager.active_character().inventory.add_item(Consumable(
                    "potion_health_medium", hit.image.copy(), 15, 10, hp_gain=15))  # il faut faire un consumable
                # ajouter à l'inventaire

        # collisionZoneEffect(self.turn_manager.active_character(), self)
        self.versus_manager.update()
        self.turn_manager.update()
        self.doors.update()
        self.chests.update()
        # if self.turn_manager.is_active_player():
        self.camera.update(self.turn_manager.active_character())
        self.minimap.update(self.turn_manager.active_character())
        self.update_game_data()
        self.check_for_chest()

    def check_for_chest(self):
        if self.chest_open:
            self.chest_open = False
            self.seller = False
            self.opened_chest.store.display_shop = True
            self.turn_manager.active_character().inventory.display_inventory = True
            super().toggle_sub_state('chest')

    def update_game_data(self):
        if self.turn_manager.is_active_player():
            self.game_data["minimap"] = self.minimap.create_minimap_data()
            self.game_data["game_data"]["heros"][self.turn_manager.get_relative_turn()]["last_pos"] = {
                "x": self.turn_manager.active_character().pos.x, "y": self.turn_manager.active_character().pos.y}

    def draw(self):
        """Draw all"""
        # self.screen.fill(BLACK)
        # self.draw_grid(self.screen)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.all_sprites.draw(self.screen)
        self.versus_manager.draw(self.screen)
        for sprite in self.all_sprites:
            if isinstance(sprite, Enemy):
                sprite.draw_health()

            self.screen.blit(sprite.image, self.camera.apply(sprite))

        for zone in self.zoneEffect:
            zone.rect = self.camera.apply_rect(zone.rect)
            # zone.draw()  ça marche pas de ouf mais c'est pas loin

        self.screen.blit(
            self.minimap.create(
                self.turn_manager.active_character(), self.turn_manager.players),
            (WIDTH -
             self.minimap.width,
             HEIGHT -
             self.minimap.height))

        # self.draw_versus()

        self.logs.draw(self.screen)

        super().transtition_active(self.screen)

    # def draw_versus(self):
    #     """Draw the hud for the versus"""
    #     if self.versus.active and self.turn_manager.numberOfAction > 0:
    #         self.versus.draw(self.screen, self.player)
