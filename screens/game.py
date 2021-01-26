"""Game screen"""

from managers.notification_manager import NotificationManager
from sprites.map_check import MapCheck
from managers.map_viewer_manager import MapViewerManager
from sprites.effects_zone import EffectsZone
from sprites.merchant import Merchant
from sprites.animated import CampFire, Circle, Confetti
from sprites.chest import Chest
from inventory.inventory import Armor, Consumable, Inventory, Spell, Weapon
from config.sprites import ASSETS_SPRITES, ITEMS, ITEMS_NAMES, ITEMS_PROPERTIES, TRAP_DAMAGE
from os import kill, path
from sprites.item import PlacableItem
from inventory.items import Item as InventoryItem
from sprites.door import Door
from managers.logs_manager import LogsManager
import pygame as pg
from components.popup_menu import PopupMenu
from window import _State, _Elements
from logger import logger
from sprites.player import Player
from sprites.obstacle import Obstacle
from utils.hud import Hud
from utils.tilemap import TiledMap, Camera, Minimap, collide_hit_rect
from utils.shortcuts import key_for
from config.window import WIDTH, HEIGHT, TILESIZE
from config.colors import BEIGE, LIGHTGREY, WHITE
from sprites.trap import Trap
from config.screens import CREDITS, MENU, GAME, TRANSITION_IN, TRANSITION_OUT
from managers.turn_manager import TurnManager
# from config.sprites import WEAPONS, ARMOR
# from config.versus import MALUS_ARC, TOUCH_HAND, DMG_ANY_WEAPON
# from inventory.inventory import Armor, Weapon
from config.versus import MALUS_ARC, TOUCH_HAND, DMG_ANY_WEAPON, NUM_ACT_BEGIN
from managers.versus_manager import VersusManager
from sprites.enemy import Enemy, Boss
from random import choice  # very temporary (just to create multiple type of enemies)
from sprites.character import players, enemies

from utils.stats_window import StatsWindow
vec = pg.math.Vector2


class Game(_Elements):
    """Game screen"""

    def __init__(self):
        self.name = GAME
        self.next = CREDITS
        super(Game, self).__init__(self.name, self.next, "menu",  '0.png', {})

        self.all_sprites = None

        self.logs = LogsManager(0, 0, 525, 6 * 16, self.text_font, 16,  self.draw_text, self)
        self.turn_manager = TurnManager(self)
        self.animated = pg.sprite.Group()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.versus_manager = VersusManager(self)
        self.notification_manager = NotificationManager(self)

        self.confetti = Confetti(self, WIDTH // 2, 0)

        self.press_space = False
        self.chest_open = False
        self.opened_chest = None
        self.merchant_open = False
        self.opened_merchant = None
        self.seller = False

        self.debug = False
        self.previous_screen = None

        self.action_message = ""

        self.states_dict = self.make_states_dict()

    def startup(self, dt, game_data):
        self.dt = dt
        self.game_data = game_data

        super().setup_transition()

        reset_event = pg.event.Event(pg.USEREVENT, code="_State", name="reset")
        pg.event.post(reset_event)

        self.new()

    def new(self):
        """Create a new game"""
        self.difficulty = self.game_data["game_data"]["difficulty"]

        players = pg.sprite.Group()
        enemies = pg.sprite.Group()
        self.animated.empty()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.merchants = pg.sprite.Group()
        self.chests = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.spells = pg.sprite.Group()
        self.effects_zones = pg.sprite.Group()
        self.map_checks = pg.sprite.Group()
        self.traps = pg.sprite.Group()
        self.turn_manager.new()
        self.versus_manager.new(self)

        self.map = TiledMap(
            path.join(
                self.assets_folder, self.game_data["game_data"]["map"]["folder"],
                self.game_data["game_data"]["map"]["filename"]))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.map_viewer_manager = MapViewerManager(
            path.join(self.assets_folder, self.game_data["game_data"]["map"]["folder"]),
            self.game_data["game_data"]["map"]["filename"], self)
        self.minimap = Minimap(self.map_img, 225, self.map_rect.width / self.map_rect.height, self.turn_manager,
                               fog=self.game_data["minimap"]["fog"], cover=self.game_data["minimap"]["cover"])
        self.camera = Camera(self.map.width, self.map.height)

        if not self.game_data["loaded"] or self.game_data["next"]:
            for tile_object in self.map.tmxdata.objects:
                obj_center = vec(
                    tile_object.x + tile_object.width / 2,
                    tile_object.y + tile_object.height / 2)
                if tile_object.name.startswith("map"):
                    MapCheck(self, obj_center.x, obj_center.y, tile_object.name)
                if tile_object.name == "skeleton":
                    self.turn_manager.enemies.append(
                        Enemy(
                            self, obj_center.x, obj_center.y, "skeleton",
                            choice(["skeleton_F", "skeleton_R", "skeleton_W"])))
                if tile_object.name == "goblin":
                    self.turn_manager.enemies.append(
                        Enemy(self, obj_center.x, obj_center.y, "goblin", choice(["goblin_F", "goblin_R", "goblin_W"]))
                    )
                if tile_object.name == "phantom":
                    self.turn_manager.enemies.append(
                        Enemy(
                            self, obj_center.x, obj_center.y, "phantom",
                            choice(["phantom_F", "phantom_R", "phantom_W"])))
                if tile_object.name == "boss":
                    self.turn_manager.enemies.append(
                        Boss(self, obj_center.x, obj_center.y, "boss", "boss")
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
                if tile_object.name == "chest":
                    Chest(self, obj_center.x, obj_center.y)
                    Obstacle(
                        self,
                        tile_object.x,
                        tile_object.y,
                        TILESIZE * 0.4,
                        TILESIZE * 0.4)
                if tile_object.name == "trap":
                    Trap(self, obj_center.x, obj_center.y)
                if tile_object.name == "camp_fire":
                    CampFire(self, tile_object.x, tile_object.y, int(TILESIZE * 1.8))
                if tile_object.name == "merchant":
                    Merchant(self, obj_center.x, obj_center.y, TILESIZE)
                if tile_object.name in ITEMS_NAMES:
                    properties = {key: value for key, value in ITEMS_PROPERTIES[tile_object.name].items() if not (key in [
                        "image_name"])}
                    properties["object_type"] = ITEMS_PROPERTIES[tile_object.name]["object_type"]
                    PlacableItem(self, obj_center, tile_object.name, properties,
                                 ITEMS[ITEMS_PROPERTIES[tile_object.name]["image_name"]],
                                 ITEMS_PROPERTIES[tile_object.name]["image_name"])

        if self.game_data["loaded"]:
            logger.info("Load from a file")
            for hero in self.game_data["game_data"]["heros"]:
                player = Player(
                    self, hero["pos"]["x"],
                    hero["pos"]["y"],
                    hero["class"],
                    hero["characteristics"],
                    ASSETS_SPRITES[hero["class"]],
                    health=hero["health"],
                    xp=hero["xp"],
                    gold=hero["gold"])
                for item in Inventory.create_inventory(hero["inventory"]):
                    player.inventory.add_item(item)
                for value in hero["equipments"]["armor"].values():
                    if value is None:
                        continue
                    item = Inventory.create_inventory(value)[0]
                    player.inventory.equip_item(item)
                if hero["equipments"]["weapon"] is not None:
                    player.inventory.equip_item(Inventory.create_inventory(hero["equipments"]["weapon"])[0])
                if hero["equipments"]["spell"] is not None:
                    player.inventory.equip_item(Inventory.create_inventory(hero["equipments"]["spell"])[0])

                self.turn_manager.players.append(player)
            for item in self.game_data["game_data"]["items"]:
                PlacableItem(self, vec(item["pos"]["x"], item["pos"]["y"]), item["name"], item["properties"],
                             ITEMS[item["image_name"]], item["image_name"])
            for enemy in self.game_data["game_data"]["enemies"]:
                enemy_obj = Enemy(
                    self, enemy["pos"]["x"],
                    enemy["pos"]["y"],
                    enemy["type"],
                    enemy["class"], equipments=True)
                for item in Inventory.create_inventory(enemy["inventory"]):
                    enemy_obj.inventory.add_item(item)
                for value in enemy["equipments"]["armor"].values():
                    if value is None:
                        continue
                    item = Inventory.create_inventory(value)[0]
                    enemy_obj.inventory.equip_item(item)
                self.turn_manager.enemies.append(
                    enemy_obj)
            for chest in self.game_data["game_data"]["chests"]:
                Chest(
                    self, chest["pos"]["x"],
                    chest["pos"]["y"],
                    consumable=chest["store"]["consumable"],
                    weapons=chest["store"]["weapons"],
                    armor=chest["store"]["armor"],
                    is_open=chest["is_open"])
                border = TILESIZE * 0.4
                Obstacle(
                    self,
                    chest["pos"]["x"] - border // 2,
                    chest["pos"]["y"] - border,
                    border,
                    border)
            for door in self.game_data["game_data"]["doors"]:
                border = TILESIZE * 0.4
                wall = None
                if not door["is_open"]:
                    wall = Obstacle(
                        self,
                        door["pos"]["x"] - border // 2,
                        door["pos"]["y"] - border,
                        border,
                        border)
                Door(self, door["pos"]["x"], door["pos"]["y"], wall, is_open=door["is_open"])
            for merchant in self.game_data["game_data"]["merchants"]:
                Merchant(
                    self, merchant["pos"]["x"],
                    merchant["pos"]["y"],
                    TILESIZE, consumable=merchant["shop"]["consumable"],
                    weapons=merchant["shop"]["weapons"],
                    armor=merchant["shop"]["armor"])
            for tile_object in self.map.tmxdata.objects:
                obj_center = vec(
                    tile_object.x + tile_object.width / 2,
                    tile_object.y + tile_object.height / 2)
                if tile_object.name == 'wall':
                    Obstacle(
                        self,
                        tile_object.x,
                        tile_object.y,
                        tile_object.width,
                        tile_object.height)
                if tile_object.name == "camp_fire":
                    CampFire(self, obj_center.x, obj_center.y, int(TILESIZE * 1.8))
                if tile_object.name.startswith("map"):
                    MapCheck(self, obj_center.x, obj_center.y, tile_object.name)
                if tile_object.name == "trap":
                    Trap(self, obj_center.x, obj_center.y)
        elif self.game_data["next"]:
            logger.info("Load the next game")
            for tile_object in self.map.tmxdata.objects:
                obj_center = vec(
                    tile_object.x + tile_object.width / 2,
                    tile_object.y + tile_object.height / 2)
                if tile_object.name == 'player':
                    if len(self.turn_manager.players) < len(self.game_data["game_data"]["heros"]):
                        _x = obj_center.x
                        _y = obj_center.y
                        _class = self.game_data["game_data"]["heros"][len(self.turn_manager.players)]["class"]
                        _characteristics = self.game_data["game_data"]["heros"][
                            len(self.turn_manager.players)]["characteristics"]
                        _images = ASSETS_SPRITES[_class]
                        p = Player(self, _x, _y, _class, _characteristics, _images)
                        p.health = self.game_data["game_data"]["heros"][len(self.turn_manager.players)]["health"]
                        p.xp = self.game_data["game_data"]["heros"][len(self.turn_manager.players)]["xp"]
                        p.gold = self.game_data["game_data"]["heros"][len(self.turn_manager.players)]["gold"]
                        for item in Inventory.create_inventory(
                                self.game_data["game_data"]["heros"][len(self.turn_manager.players)]["inventory"]):
                            p.inventory.add_item(item)
                        for value in self.game_data["game_data"]["heros"][
                                len(self.turn_manager.players)]["equipments"]["armor"].values():
                            if value is None:
                                continue
                            item = Inventory.create_inventory(value)[0]
                            p.inventory.equip_item(item)
                        if self.game_data["game_data"]["heros"][
                                len(self.turn_manager.players)]["equipments"]["weapon"] is not None:
                            p.inventory.equip_item(
                                Inventory.create_inventory(
                                    self.game_data["game_data"]["heros"][len(self.turn_manager.players)]
                                    ["equipments"]["weapon"])[0])
                        if self.game_data["game_data"]["heros"][
                                len(self.turn_manager.players)]["equipments"]["spell"] is not None:
                            p.inventory.equip_item(
                                Inventory.create_inventory(
                                    self.game_data["game_data"]["heros"][len(self.turn_manager.players)]
                                    ["equipments"]["spell"])[0])
                        self.turn_manager.players.append(p)
        else:
            logger.info("Load a new game")
            for tile_object in self.map.tmxdata.objects:
                obj_center = vec(
                    tile_object.x + tile_object.width / 2,
                    tile_object.y + tile_object.height / 2)
                if tile_object.name == 'player':
                    if len(self.turn_manager.players) < len(self.game_data["game_data"]["heros"]):
                        _x = obj_center.x if not ("pos" in self.game_data["game_data"]["heros"][
                            len(self.turn_manager.players)].keys()) else self.game_data["game_data"]["heros"][
                            len(self.turn_manager.players)]["pos"]["x"]
                        _y = obj_center.y if not ("pos" in self.game_data["game_data"]["heros"][
                            len(self.turn_manager.players)].keys()) else self.game_data["game_data"]["heros"][
                            len(self.turn_manager.players)]["pos"]["y"]
                        _class = self.game_data["game_data"]["heros"][len(self.turn_manager.players)]["class"]
                        _characteristics = self.game_data["game_data"]["heros"][
                            len(self.turn_manager.players)]["characteristics"]
                        _images = ASSETS_SPRITES[_class]
                        self.turn_manager.players.append(
                            Player(self, _x, _y, _class, _characteristics, _images))

            self.save_data()
            self.save_data_in_file()

        self.hud = Hud(self)
        self.stats = StatsWindow(self)

    def make_states_dict(self):
        """Make the dictionary of state methods for the level.


        Returns:
            object: define all the possible states for a screen
        """
        previous_dict = super().make_states_dict().copy()
        add_dict = {
            'inventory': self.inventory_run,
            'chest': self.chest_run,
            'merchant': self.merchant_run,
            'map': self.map_run,
            'finish': self.finish_run,
            'game_over': self.game_over_run,
            'menu': self.menu_run,
            'stats': self.stats_run
        }

        return previous_dict | add_dict

    def get_events(self, event):
        self.press_space = False
        if event.type == pg.KEYDOWN:
            if self.state == "normal":
                if event.key == pg.K_ESCAPE:
                    self.create_dim()
                    self.btns_dict = self.create_buttons_dict("menu")
                    self.create_buttons(self.screen, start_y_offset=8 * HEIGHT / 10)
                    self.toggle_sub_state('menu')
            elif key_for(self.game_data["shortcuts"]["game"]["return"]["keys"], event):
                super().toggle_sub_state(self.state)

        if event.type == pg.KEYUP:
            if event.key == pg.K_a:
                self.turn_manager.get_playable_character().xp += 10
                logger.debug(self.turn_manager.get_playable_character().xp)
                logger.debug(type(self.turn_manager.get_playable_character()))
            if event.key == pg.K_l:
                logger.debug(self.turn_manager.get_playable_character().health)
            if event.key == pg.K_EQUALS:
                self.debug = not self.debug
            if self.turn_manager.is_active_player():
                self.toggle_states(event)
            if event.key == pg.K_t:
                if self.versus_manager.active:
                    self.logs.add_log("Manual next turn")
                    self.versus_manager.add_turn()
            if key_for(self.game_data["shortcuts"]["game"]["environment"]["keys"], event):
                self.press_space = True
            if key_for(self.game_data["shortcuts"]["game"]["view"]["keys"], event):
                logger.info("Change the vision")
                self.turn_manager.add_vision()
            if key_for(self.game_data["shortcuts"]["game"]["playable"]["keys"], event):
                if not self.versus_manager.active:
                    logger.info("Change the playable")
                    self.turn_manager.add_playable()
                    self.turn_manager.vision = self.turn_manager.playable

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.state == 'inventory':
                    if self.turn_manager.active().inventory.display_inventory:
                        logger.info("Select an item from the inventory")
                        self.turn_manager.active().inventory.move_item()
        self.versus_manager.event(event)
        self.logs.event(event)
        if self.turn_manager.is_active_player:
            self.events_inventory(event)
            self.events_shop(event)
            self.events_chest(event)
            self.events_hud(event)
        if self.map_viewer_manager.active:
            self.map_viewer_manager.event(event)

    # def events_versus(self, event):

    #     if event.type == pg.KEYUP:

    #         if event.key == pg.K_TAB:
    #             """Simulate begin versus"""
    #             if self.versus_manager.active:
    #                 self.versus_manager.finish_versus()
    #             else:
    #                 self.versus_manager.start_versus()

    #         if self.turn_manager.is_active_player():
    #             if key_for(self.game_data["shortcuts"]["game"]["attack"]["keys"], event):
    #                 self.versus_manager.action_attack()
    #             if key_for(self.game_data["shortcuts"]["game"]["move"]["keys"], event):
    #                 self.versus_manager.action_move()
    #             if key_for(self.game_data["shortcuts"]["game"]["spell"]["keys"],
    #                        event) and not self.turn_manager.get_active_spell() is None:
    #                 self.versus_manager.action_spell()

    #             if key_for(self.game_data["shortcuts"]["game"]["validate"]["keys"], event):
    #                 self.versus_manager.validate()

    #     if event.type == pg.MOUSEBUTTONDOWN:
    #         if event.button == 1:
    #             mouse_pos = pg.mouse.get_pos()
    #             self.versus_manager.events(mouse_pos)

    def events_hud(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                state = self.hud.get_relate_button_state(pg.mouse.get_pos())
                if state == 'inventory':
                    if self.turn_manager.is_active_player():
                        logger.info("Toggle inventory from %s", self.turn_manager.active())
                        self.seller = False
                        self.map_viewer_manager.active = False
                        self.turn_manager.active().inventory.display_inventory = True
                        self.create_dim()
                        super().toggle_sub_state('inventory')
                if state == 'map':
                    self.seller = False
                    self.map_viewer_manager.active = not self.map_viewer_manager.active
                    self.turn_manager.active().inventory.display_inventory = False
                    self.create_dim()
                    super().toggle_sub_state('map')
                if state == 'quests':
                    pass
                if state == 'stats':
                    logger.info("Toggle stats from %s", self.turn_manager.active())
                    self.stats.view_stats = True
                    self.seller = False
                    self.map_viewer_manager.active = False
                    self.turn_manager.active().inventory.display_inventory = False
                    self.create_dim()
                    super().toggle_sub_state('stats')

    def events_inventory(self, event):
        """When the shop state is running"""
        if self.state == 'inventory':
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.turn_manager.active().inventory.move_item()
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.turn_manager.active().inventory.place_item()
                elif event.button == 3:
                    self.mouse_pos = pg.mouse.get_pos()
                    PopupMenu(self.turn_manager.active().inventory.menu_data)
            elif event.type == pg.USEREVENT:
                if event.code == 'MENU':
                    self.inventory_events(event)

    def inventory_events(self, event):
        """Used to manage all event"""
        if event.name == "inventory":
            self.turn_manager.active().inventory.check_slot(event.text, self.mouse_pos)
            if self.seller:
                if event.text in ["sell"]:
                    self.turn_manager.active().shop.check_slot(
                        event.text, self.screen, self.turn_manager.active(), self.mouse_pos)

    def events_shop(self, event):
        """When the shop state is running"""
        if self.state == 'merchant':  # faudrait foutre tout ça dans une fonction du shop et de l'inventaire
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 3:
                    self.mouse_pos = pg.mouse.get_pos()
                    if self.opened_merchant.shop.is_clicked(self.mouse_pos):
                        PopupMenu(self.opened_merchant.shop.menu_data)
                    elif self.turn_manager.active().inventory.is_clicked(self.mouse_pos):
                        PopupMenu(self.turn_manager.active().inventory.menu_data)
                elif event.button == 1:
                    self.opened_merchant.shop.place_item(self.turn_manager.active().inventory)
                    self.turn_manager.active().inventory.place_item()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.opened_merchant.shop.move_item()
                    self.turn_manager.active().inventory.move_item()
            elif event.type == pg.USEREVENT:
                if event.code == 'MENU':
                    if event.name == 'shop' and event.text in self.opened_merchant.shop.menu_data:
                        self.opened_merchant.shop.check_slot(
                            event.text, self.screen, self.turn_manager.active(), self.mouse_pos)
                    self.inventory_events(event)

    def events_chest(self, event):
        """When the chest state is running"""
        if self.state == 'chest':  # faudrait foutre tout ça dans une fonction du shop et de l'inventaire
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 3:
                    self.mouse_pos = pg.mouse.get_pos()
                    if self.opened_chest.store.is_clicked(self.mouse_pos):
                        PopupMenu(self.opened_chest.store.menu_data)
                    elif self.turn_manager.active().inventory.is_clicked(self.mouse_pos):
                        PopupMenu(self.turn_manager.active().inventory.menu_data)
                elif event.button == 1:
                    self.opened_chest.store.place_item(self.turn_manager.active().inventory)
                    self.turn_manager.active().inventory.place_item()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.opened_chest.store.move_item()
                    self.turn_manager.active().inventory.move_item()
            elif event.type == pg.USEREVENT:
                if event.code == 'MENU':
                    if event.name == 'store' and event.text in self.opened_chest.store.menu_data:
                        self.opened_chest.store.check_slot(
                            event.text, self.screen, self.turn_manager.active(), self.mouse_pos)
                    self.inventory_events(event)

    def toggle_states(self, event):
        """Use to toggle the state of all states"""
        if key_for(self.game_data["shortcuts"]["game"]
                   ["inventory"]["keys"], event):
            logger.info("Toggle inventory from %s", self.turn_manager.active())
            self.seller = False
            self.map_viewer_manager.active = False
            self.turn_manager.active().inventory.display_inventory = True
            self.create_dim()
            super().toggle_sub_state('inventory')
        if key_for(self.game_data["shortcuts"]["game"]["map"]["keys"], event):
            self.seller = False
            self.map_viewer_manager.active = not self.map_viewer_manager.active
            self.turn_manager.active().inventory.display_inventory = False
            self.create_dim()
            super().toggle_sub_state('map')

    def create_dim(self):
        self.draw()
        self.previous_screen = self.screen.copy()
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.previous_screen.blit(self.dim_screen, (0, 0))

    def run(self, surface, keys, mouse, dt):
        """Run states"""
        self.screen = surface
        self.dt = dt
        update_level = self.states_dict[self.state]
        update_level()

    def normal_run(self):
        """Run the normal state"""
        self.update()
        self.draw()

    def menu_run(self):
        """Run the inventory state"""
        self.screen.blit(self.previous_screen, (0, 0))
        super().events_buttons()
        self.draw_text("Quit the game ?", self.title_font, 128, BEIGE, WIDTH // 2, HEIGHT // 2, align="center")
        super().draw_buttons()

    def inventory_run(self):
        """Run the inventory state"""
        self.screen.blit(self.previous_screen, (0, 0))

        self.turn_manager.active().inventory.draw(self.screen)

    def chest_run(self):
        self.screen.blit(self.previous_screen, (0, 0))

        self.turn_manager.active().inventory.draw(self.screen)
        self.opened_chest.store.draw(self.screen)

    def merchant_run(self):
        self.screen.blit(self.previous_screen, (0, 0))

        self.turn_manager.active().inventory.draw(self.screen)
        self.opened_merchant.shop.draw(self.screen)

    def map_run(self):
        self.screen.blit(self.previous_screen, (0, 0))

        self.map_viewer_manager.update()
        self.map_viewer_manager.draw(self.screen)
        super().draw_action(self.action_message)

    def finish_run(self):
        """Run the finish state"""
        self.finish_update()
        self.finish_draw()

    def finish_update(self):
        """Update the finish state"""
        super().events_buttons()
        self.confetti.update()

    def finish_draw(self):
        """Draw the finish state"""
        self.screen.blit(self.previous_screen, (0, 0))

        self.draw_text("You win", self.title_font, 128, BEIGE, WIDTH // 2, HEIGHT // 2, align="center")
        super().draw_buttons()
        self.screen.blit(self.confetti.image, self.confetti.rect)

    def game_over_run(self):
        """Run the game over state"""
        self.game_over_update()
        self.game_over_draw()

    def game_over_update(self):
        """Update the finish state"""
        super().events_buttons()

    def game_over_draw(self):
        """Draw the game_over state"""
        self.screen.blit(self.previous_screen, (0, 0))

        self.draw_text("Game over", self.title_font, 128, BEIGE, WIDTH // 2, HEIGHT // 2, align="center")
        super().draw_buttons()

    def stats_run(self):
        self.screen.blit(self.previous_screen, (0, 0))
        self.stats.draw(self.screen)

    def create_buttons_dict(self, state):
        """Create the dict for all buttons


        Returns:
            dict
        """
        if state == "finish":
            return {
                "credit": {
                    "text": "Credits",
                    "on_click": self.load_next_state,
                    "on_click_params": [CREDITS]
                }
            }
        elif state == "game over":
            return {
                "menu": {
                    "text": "Menu",
                    "on_click": self.load_next_state,
                    "on_click_params": [MENU]
                }
            }
        elif state == "menu":
            return {
                "menu": {
                    "text": "Menu",
                    "on_click": self.load_next_state,
                    "on_click_params": [MENU]
                }
            }
        else:
            return {}

    def save_data_in_file(self):
        self.action = True
        self.action_message = "Save game in file"
        self.logs.add_log("Save the game in file")
        save_event = pg.event.Event(pg.USEREVENT, code="_State", name="save")
        pg.event.post(save_event)

    def update(self):
        """Update all"""
        self.update_layers()
        self.update_camera()

        self.update_sprites()
        self.items.update()

        self.check_hits()
        self.check_for_chest_open()
        self.check_for_merchant_open()

        self.minimap.update()
        self.versus_manager.update()
        self.turn_manager.update(self.versus_manager.active)
        self.notification_manager.update()

    def update_camera(self):
        if self.turn_manager.get_vision_character():
            self.camera.update(self.turn_manager.get_vision_character())

    def update_layers(self):
        for sprite in self.all_sprites:
            if not isinstance(sprite, MapCheck) and not isinstance(sprite, Circle) and not isinstance(sprite, Trap):
                self.all_sprites.change_layer(sprite, sprite.rect.bottom)

    def update_sprites(self):
        self.doors.update()
        self.chests.update()
        self.merchants.update()
        self.effects_zones.update()
        self.traps.update()
        for animated in self.animated:
            if isinstance(animated, CampFire):
                animated.update()

    def check_hits(self):
        """Check all hit in the game"""
        self.hit_chests()
        self.hit_map_checks()
        self.hit_doors()
        self.hit_merchants()
        self.hit_animated()
        self.hit_items()
        self.hit_traps()

    def hit_traps(self):
        hits = pg.sprite.spritecollide(self.turn_manager.active(), self.traps, False, collide_hit_rect)
        for hit in hits:
            if not hit.to_open:
                self.turn_manager.active().subHp(TRAP_DAMAGE)
                if (self.turn_manager.is_active_enemy() and self.turn_manager.active().health <= 0):
                    self.versus_manager.kill_enemy(self.turn_manager.active())
            hit.to_open = True

    def hit_map_checks(self):
        hits = pg.sprite.spritecollide(self.turn_manager.active(), self.map_checks, False)
        if self.press_space and hits:
            for hit in hits:
                hit.collide()
            self.press_space = False

    def hit_chests(self):
        hits = pg.sprite.spritecollide(self.turn_manager.active(), self.chests, False)
        if self.press_space and hits:
            for hit in hits:
                hit.try_open(self.turn_manager.active())
            self.press_space = False

    def hit_doors(self):
        hits = pg.sprite.spritecollide(
            self.turn_manager.active(),
            self.doors, False)
        if self.press_space and hits:
            for hit in hits:
                hit.try_open(self.turn_manager.active())
            self.press_space = False

    def hit_merchants(self):
        hits = pg.sprite.spritecollide(self.turn_manager.active(), self.merchants, False)
        if self.press_space and hits:
            for hit in hits:
                hit.try_open()
            self.press_space = False

    def hit_animated(self):
        hits = pg.sprite.spritecollide(self.turn_manager.active(), self.animated, False)
        if self.press_space and hits:
            for hit in hits:
                if isinstance(hit, CampFire):
                    if not self.versus_manager.active:
                        # restore the health of the player
                        self.turn_manager.active().addHp(100)
                        self.logs.add_log("Restore the player health")
                        self.save_data()
                        self.save_data_in_file()
                        self.press_space = False
                    else:
                        self.logs.add_log("Unable to save because versus is active")
            self.press_space = False

    def hit_items(self):
        for sprite in self.turn_manager.players + self.turn_manager.enemies:
            hits = pg.sprite.spritecollide(sprite, self.items, False)
            for hit in hits:
                if hit.properties["object_type"] == "other":
                    if isinstance(sprite, Player):
                        hit.kill()
                        sprite.inventory.add_item(
                            InventoryItem(
                                hit.name, hit.image.copy(),
                                hit.image_name, hit.properties["price"],
                                hit.properties["weight"]))
                if hit.properties["object_type"] == "consumable":
                    hit.kill()
                    sprite.inventory.add_item(
                        Consumable(
                            hit.name, hit.image.copy(),
                            hit.image_name, hit.properties["price"],
                            hit.properties["weight"],
                            hit.properties["heal"],
                            hit.properties["shield"])
                    )
                if hit.properties["object_type"] == "weapon":
                    hit.kill()
                    sprite.inventory.add_item(
                        Weapon(
                            hit.name, hit.image.copy(),
                            hit.image_name, hit.properties["price"],
                            hit.properties["slot"],
                            hit.properties["type"],
                            hit.properties["type"],
                            hit.properties["weight"],
                            hit.properties["dice_value"],
                            hit.properties["scope"]
                        )
                    )
                if hit.properties["object_type"] == "armor":
                    hit.kill()
                    sprite.inventory.add_item(
                        Armor(
                            hit.name, hit.image.copy(),
                            hit.image_name, hit.properties["price"],
                            hit.properties["weight"],
                            hit.properties["shield"],
                            hit.properties["slot"]
                        )
                    )
                if hit.properties["object_type"] == "spell":
                    hit.kill()
                    sprite.inventory.add_item(
                        Spell(
                            hit.name, hit.image.copy(),
                            hit.image_name,
                            hit.properties["slot"],
                            hit.properties["type"],
                            hit.properties["scope"],
                            hit.properties["time_to_live"],
                            hit.properties["number_dice"],
                            hit.properties["dice_value"]))

    def check_for_chest_open(self):
        if self.chest_open:
            self.chest_open = False
            self.seller = False
            self.opened_chest.store.display_shop = True
            self.turn_manager.active().inventory.display_inventory = True
            super().toggle_sub_state('chest')

    def check_for_merchant_open(self):
        if self.merchant_open:
            self.merchant_open = False
            self.seller = False
            self.opened_merchant.shop.display_shop = True
            self.turn_manager.active().inventory.display_inventory = True
            super().toggle_sub_state('merchant')

    def save_data(self):
        self.logs.add_log("Save data in memory")
        self.game_data["minimap"] = self.minimap.create_minimap_data()
        self.game_data["game_data"]["heros"] = self.save_list(self.turn_manager.players)
        self.game_data["game_data"]["items"] = self.save_list(self.items)
        self.game_data["game_data"]["enemies"] = self.save_list(self.turn_manager.enemies)
        self.game_data["game_data"]["chests"] = self.save_list(self.chests)
        self.game_data["game_data"]["doors"] = self.save_list(self.doors)
        self.game_data["game_data"]["merchants"] = self.save_list(self.merchants)
        #  no more needed because we can only save if the versus is disable
        # self.game_data["game_data"]["turns"] = self.save_turns()

    def save_turns(self):
        """Save the footprint of all characters to save turns

        Returns:
            list: a list a tuple using the x and the y
        """
        return [(int(character.x), int(character.y)) for character in self.turn_manager.get_characters()]

    def save_list(self, values):
        data = list()
        for value in values:
            data.append(value.save())

        return data

    def draw(self):
        """Draw all"""
        self.draw_map()
        self.draw_all_sprites()

        self.versus_manager.draw(self.screen)
        self.minimap.draw(self.screen)
        self.logs.draw(self.screen)
        self.hud.draw(self.screen)
        self.notification_manager.draw(self.screen)
        super().draw_action(self.action_message)

        self.draw_debug()

        super().transtition_active(self.screen)

    def draw_map(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

    def draw_all_sprites(self):
        for sprite in self.all_sprites:
            if isinstance(sprite, Enemy):
                sprite.draw_health()
            if not isinstance(sprite, Circle):
                self.screen.blit(sprite.image, self.camera.apply(sprite))
            if isinstance(sprite, Circle):
                self.versus_manager.draw_range(self.screen)

    def draw_debug(self):
        if self.debug:
            for sprite in self.turn_manager.players:
                pg.draw.rect(self.screen, (0, 255, 0), self.camera.apply_rect(sprite.hit_rect), 1)
            for sprite in self.turn_manager.enemies:
                pg.draw.rect(self.screen, (0, 255, 0), self.camera.apply_rect(sprite.hit_rect), 1)
            for wall in self.walls:
                pg.draw.rect(self.screen, (255, 0, 0), self.camera.apply(wall), 1)
            for trap in self.traps:
                pg.draw.rect(self.screen, (0, 0, 255), self.camera.apply(trap), 1)
            for map_check in self.map_checks:
                pg.draw.rect(self.screen, (0, 0, 255), self.camera.apply(map_check), 1)
