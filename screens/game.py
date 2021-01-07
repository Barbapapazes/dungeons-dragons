"""Game screen"""

from managers.map_viewer_manager import MapViewerManager
from sprites.effects_zone import EffectsZone
from sprites.merchant import Merchant
from sprites.animated import CampFire
from sprites.chest import Chest
from inventory.inventory import Armor, Consumable, Inventory, Spell, Weapon
from config.sprites import ASSETS_SPRITES, ITEMS, ITEMS_NAMES, ITEMS_PROPERTIES
from os import path
from sprites.item import PlacableItem
from inventory.items import Item as InventoryItem
from sprites.door import Door
from managers.logs_manager import LogsManager
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
from managers.turn_manager import TurnManager
# from config.sprites import WEAPONS, ARMOR
# from config.versus import MALUS_ARC, TOUCH_HAND, DMG_ANY_WEAPON
# from inventory.inventory import Armor, Weapon
from config.versus import MALUS_ARC, TOUCH_HAND, DMG_ANY_WEAPON, NUM_ACT_BEGIN
from managers.versus_manager import VersusManager
from sprites.enemy import Enemy, Boss
from random import choice  # very temporary (just to create multiple type of enemies)

vec = pg.math.Vector2


class Game(_State):
    """Game screen"""

    def __init__(self):
        self.name = GAME
        super(Game, self).__init__(self.name)
        self.next = CREDITS

        self.all_sprites = None

        self.logs = LogsManager(0, 0, 300, 100, self.text_font, 16,  self.draw_text)
        self.turn_manager = TurnManager()
        self.animated = pg.sprite.Group()
        self.versus_manager = VersusManager(self)

        self.press_space = False
        self.chest_open = False
        self.opened_chest = None
        self.merchant_open = False
        self.opened_merchant = None
        self.seller = False

        self.states_dict = self.make_states_dict()

    def startup(self, dt, game_data):
        self.dt = dt
        self.game_data = game_data
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.merchants = pg.sprite.Group()
        self.chests = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.spells = pg.sprite.Group()
        self.effects_zones = pg.sprite.Group()

        EffectsZone(self, 500, 300, "heal", 2, 2, 20)
        EffectsZone(self, 800, 300, "attack", 2, 2, 20)

        # self.en1 = Enemy(self, 10, 4, "Boot n1")
        # self.en2 = Enemy(self, 11, 7, "Boot n2")
        self.en1 = list()
        self.en2 = list()
        self.enemy = [self.en1, self.en2]

        super().setup_transition()

        self.new()

    def new(self):
        """Create a new game"""
        self.map = TiledMap(
            path.join(
                self.assets_folder, self.game_data["game_data"]["map"]["folder"],
                self.game_data["game_data"]["map"]["filename"]))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.map_viewer_manager = MapViewerManager(
            path.join(self.assets_folder, self.game_data["game_data"]["map"]["folder"]),
            self.game_data["game_data"]["map"]["filename"], self)
        self.minimap = Minimap(
            self.map_img,
            225,
            self.map_rect.width /
            self.map_rect.height, self.game_data["minimap"]["fog"], self.game_data["minimap"]["cover"])
        self.camera = Camera(self.map.width, self.map.height)

        if self.game_data["loaded"]:
            logger.info("Load from a file")
            for hero in self.game_data["game_data"]["heros"]:
                player = Player(
                    self, hero["pos"]["x"],
                    hero["pos"]["y"],
                    hero["class"],
                    hero["characteristics"],
                    hero["health"],
                    hero["xp"],
                    hero["gold"],
                    ASSETS_SPRITES[hero["class"]])
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
                    enemy["class"])
                for item in Inventory.create_inventory(enemy["inventory"]):
                    print(item.name)
                    enemy_obj.inventory.add_item(item)
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
                if tile_object.name == 'wall':
                    Obstacle(
                        self,
                        tile_object.x,
                        tile_object.y,
                        tile_object.width,
                        tile_object.height)
                if tile_object.name == "camp_fire":
                    CampFire(self, tile_object.x, tile_object.y, int(TILESIZE * 1.8))
        else:
            logger.info("Load a new game")
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
                            Player(self, _x, _y, _class, _characteristics, 100, 0, 100, _images))
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
            self.save_data()
            self.save_data_in_file()

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
        #         value['number_dice'],
        #         value['dice_value'],
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
                       'chest': self.chest_run,
                       'merchant': self.merchant_run,
                       'map': self.map_run,
                       }

        return states_dict

    def get_events(self, event):
        self.press_space = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                super().toggle_sub_state(self.state)

        if event.type == pg.KEYUP:
            if self.turn_manager.is_active_player():
                self.toggle_states(event)
            if event.key == pg.K_t:
                if self.versus_manager.active:
                    self.logs.add_log("Manual next turn")
                    self.versus_manager.add_turn()
            if event.key == pg.K_SPACE:
                self.press_space = True
            if event.key == pg.K_v:
                logger.info("Change the vision")
                self.turn_manager.add_vision()
            if event.key == pg.K_c:
                if not self.versus_manager.active:
                    logger.info("Change the playable")
                    self.turn_manager.add_playable()
                    self.turn_manager.vision = self.turn_manager.playable

            if event.key == pg.K_u:
                # il va falloir le déplacer pour le mettre dans les toggle
                self.seller = False
                self.map_viewer_manager.active = not self.map_viewer_manager.active
                super().toggle_sub_state('map')

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:

                if self.state == 'inventory':
                    if self.turn_manager.active_character().inventory.display_inventory:
                        logger.info("Select an item from the inventory")
                        self.turn_manager.active_character().inventory.move_item()

        if self.map_viewer_manager.active:
            self.map_viewer_manager.event(event)
        self.event_versus(event)
        if self.turn_manager.is_active_player:
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
        if self.state == 'merchant':  # faudrait foutre tout ça dans une fonction du shop et de l'inventaire
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 3:
                    self.mouse_pos = pg.mouse.get_pos()
                    if self.opened_merchant.shop.is_clicked(self.mouse_pos):
                        PopupMenu(self.opened_merchant.shop.menu_data)
                    elif self.turn_manager.active_character().inventory.is_clicked(self.mouse_pos):
                        PopupMenu(self.turn_manager.active_character().inventory.menu_data)
                elif event.button == 1:
                    self.opened_merchant.shop.place_item(self.turn_manager.active_character().inventory)
                    self.turn_manager.active_character().inventory.place_item()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.opened_merchant.shop.move_item()
                    self.turn_manager.active_character().inventory.move_item()
            elif event.type == pg.USEREVENT:
                if event.code == 'MENU':
                    if event.name == 'shop' and event.text in self.opened_merchant.shop.menu_data:
                        self.opened_merchant.shop.check_slot(
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
            self.map_viewer_manager.active = False
            logger.info("Toggle the sub-menu")
            self.turn_manager.active_character().inventory.display_inventory = False
            self.turn_manager.active_character().shop.display_shop = False
            super().toggle_sub_state('menu')
        if key_for(self.game_data["shortcuts"]["game"]
                   ["inventory"]["keys"], event):
            logger.info("Toggle inventory from turn_manager.active_character()")
            self.seller = False
            self.map_viewer_manager.active = False
            # self.turn_manager.active_character().shop.display_shop = False
            self.turn_manager.active_character().inventory.display_inventory = True
            super().toggle_sub_state('inventory')
        # if event.key == pg.K_p:
        #     logger.info("Toggle the shop")
        #     self.seller = not self.seller
        #     self.turn_manager.active_character().shop.display_shop = True
        #     self.turn_manager.active_character().inventory.display_inventory = True
        #     super().toggle_sub_state('shop')

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
        self.versus_manager.check_for_versus()
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

    def merchant_run(self):
        self.draw()
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.screen.blit(self.dim_screen, (0, 0))
        self.turn_manager.active_character().inventory.draw(self.screen)
        self.opened_merchant.shop.draw(self.screen)

    def map_run(self):
        self.draw()
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.screen.blit(self.dim_screen, (0, 0))
        self.map_viewer_manager.update()
        self.map_viewer_manager.draw(self.screen)

    def check_for_menu(self):
        """Check if the user want to access to the menu"""

    def save_data_in_file(self):
        self.logs.add_log("Save the game")
        save_event = pg.event.Event(pg.USEREVENT, code="_State", name="save")
        pg.event.post(save_event)

    def update(self):
        """Update all"""
        self.items.update()
        for sprite in self.all_sprites:
            self.all_sprites.change_layer(sprite, sprite.rect.bottom)

        self.check_hits()
        self.update_sprites()
        # if self.turn_manager.is_active_player():
        self.camera.update(self.turn_manager.get_vision_character())
        self.minimap.update(self.turn_manager.players)
        self.check_for_chest_open()
        self.check_for_merchant_open()

    def update_sprites(self):
        self.versus_manager.update()
        self.turn_manager.update(self.versus_manager.active)
        self.doors.update()
        self.chests.update()
        self.merchants.update()
        self.effects_zones.update()
        for animated in self.animated:
            if isinstance(animated, CampFire):
                animated.update()

    def check_hits(self):
        self.hit_chests()
        self.hit_doors()
        self.hit_merchants()
        self.hit_animated()
        self.hit_items()

    def hit_chests(self):
        hits = pg.sprite.spritecollide(self.turn_manager.active_character(), self.chests, False)
        if self.press_space and hits:
            for hit in hits:
                hit.try_open(self.turn_manager.active_character())
            self.press_space = False

    def hit_doors(self):
        hits = pg.sprite.spritecollide(
            self.turn_manager.active_character(),
            self.doors, False)
        if self.press_space and hits:
            for hit in hits:
                hit.try_open(self.turn_manager.active_character())
            self.press_space = False

    def hit_merchants(self):
        hits = pg.sprite.spritecollide(self.turn_manager.active_character(), self.merchants, False)
        if self.press_space and hits:
            for hit in hits:
                hit.try_open()
            self.press_space = False

    def hit_animated(self):
        hits = pg.sprite.spritecollide(self.turn_manager.active_character(), self.animated, False)
        if self.press_space and hits:
            for hit in hits:
                if isinstance(hit, CampFire):
                    # restore the health of the player
                    self.turn_manager.active_character().addHp(100)
                    self.logs.add_log("Restore the player health")
                    self.save_data()
                    self.save_data_in_file()
                    self.press_space = False

    def hit_items(self):
        hits = pg.sprite.spritecollide(self.turn_manager.active_character(), self.items, False)
        for hit in hits:
            if hit.properties["object_type"] == "other":
                hit.kill()
                self.turn_manager.active_character().inventory.add_item(InventoryItem(
                    hit.name, hit.image.copy(), hit.image_name, hit.properties["price"], hit.properties["weight"]
                )
                )
            if hit.properties["object_type"] == "consumable":
                hit.kill()
                self.turn_manager.active_character().inventory.add_item(
                    Consumable(
                        hit.name, hit.image.copy(),
                        hit.image_name, hit.properties["price"],
                        hit.properties["weight"],
                        hit.properties["heal"],
                        hit.properties["shield"])
                )
            if hit.properties["object_type"] == "weapon":
                hit.kill()
                self.turn_manager.active_character().inventory.add_item(
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
                self.turn_manager.active_character().inventory.add_item(
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
                self.turn_manager.active_character().inventory.add_item(
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
            self.turn_manager.active_character().inventory.display_inventory = True
            super().toggle_sub_state('chest')

    def check_for_merchant_open(self):
        if self.merchant_open:
            self.merchant_open = False
            self.seller = False
            self.opened_merchant.shop.display_shop = True
            self.turn_manager.active_character().inventory.display_inventory = True
            super().toggle_sub_state('merchant')

    def save_data(self):
        self.game_data["minimap"] = self.minimap.create_minimap_data()
        self.game_data["game_data"]["heros"] = self.save_players()
        self.game_data["game_data"]["items"] = self.save_items()
        self.game_data["game_data"]["enemies"] = self.save_enemies()
        self.game_data["game_data"]["chests"] = self.save_chests()
        self.game_data["game_data"]["doors"] = self.save_doors()
        self.game_data["game_data"]["merchants"] = self.save_merchants()
        self.game_data["game_data"]["turns"] = self.save_turns()

    def save_turns(self):
        """Save the footprint of all characters to save turns

        Returns:
            list: a list a tuple using the x and the y
        """
        return [(int(character.x), int(character.y)) for character in self.turn_manager.get_characters()]

    def save_merchants(self):
        merchants_list = list()
        for merchant in self.merchants:
            merchants_list.append(merchant.save())

        return merchants_list

    def save_doors(self):
        doors_list = list()
        for door in self.doors:
            doors_list.append(door.save())

        return doors_list

    def save_chests(self):
        chests_list = list()
        for chest in self.chests:
            chests_list.append(chest.save())

        return chests_list

    def save_players(self):
        players_list = list()
        for character in self.all_sprites:
            if isinstance(character, Player):
                players_list.append(character.save())

        return players_list

    def save_enemies(self):
        enemies_list = list()
        for character in self.all_sprites:
            if isinstance(character, Enemy):
                enemies_list.append(character.save())

        return enemies_list

    def save_items(self):
        """Save all the placable items on the map

        Returns:
            object
        """
        items_list = list()
        for item in self.items:
            items_list.append(item.save())

        return items_list

    def draw(self):
        """Draw all"""
        # self.screen.fill(BLACK)
        # self.draw_grid(self.screen)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.all_sprites.draw(self.screen)
        self.versus_manager.draw(self.screen)
        for animated in self.animated:
            if isinstance(animated, CampFire):
                self.screen.blit(animated.image, self.camera.apply(animated))

        for sprite in self.all_sprites:
            if isinstance(sprite, Enemy):
                sprite.draw_health()

            self.screen.blit(sprite.image, self.camera.apply(sprite))

        # for zone in self.zoneEffect:
        #     zone.rect = self.camera.apply_rect(zone.rect)
        #     # zone.draw()  ça marche pas de ouf mais c'est pas loin

        self.screen.blit(
            self.minimap.create(
                self.turn_manager.get_vision_character(), self.turn_manager.players, self.turn_manager.enemies),
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
