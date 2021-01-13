import pygame as pg
from os import path
from sprites.player import Player
from config.window import WIDTH, HEIGHT
from config.colors import RED, GREEN, CYAN, DARKGREY, GOLD
from config.sprites import PLAYER_MAX_HP, PLAYER_MAX_MP


class Hud:
    """Create the hud"""

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.imgs = game.img_folder

        self.button_dict = self.create_buttons_dict()
        self.buttons = list()


    def draw_healthbars(self, screen):
        """Draw a healthbar for each player of the game"""
        pg.draw.rect(screen, RED, 
                (WIDTH // 3, 15*HEIGHT // 16, WIDTH //3, HEIGHT // 32))
        pg.draw.rect(screen, GREEN, (WIDTH // 3, 15*HEIGHT // 16, 
                    ((WIDTH // 3)*self.game.turn_manager.get_vision_character().health) // PLAYER_MAX_HP, HEIGHT // 32))
        for i in range(1, len(self.game.turn_manager.players)):
            pg.draw.rect(screen, RED, 
                (21.5*WIDTH // 24, (10 + i)*HEIGHT // 16, WIDTH // 12, HEIGHT // 64))
        i = 1
        for p in self.game.turn_manager.players:
            if p != self.game.turn_manager.get_vision_character():
                pg.draw.rect(screen, GREEN, (21.5*WIDTH // 24, (10 + i)*HEIGHT // 16, 
                    ((WIDTH // 12)*p.health) // PLAYER_MAX_HP, HEIGHT // 64))
                i += 1
    def draw_manabars(self, screen):
        pg.draw.rect(screen, DARKGREY, 
                (WIDTH // 3, 15.5*HEIGHT // 16, WIDTH //3, HEIGHT // 64))
        pg.draw.rect(screen, CYAN, (WIDTH // 3, 15.5*HEIGHT // 16, 
                    ((WIDTH // 3)*self.game.turn_manager.get_vision_character().health) // PLAYER_MAX_HP, HEIGHT // 64))
        for i in range(1, len(self.game.turn_manager.players)):
            pg.draw.rect(screen, DARKGREY, 
                (21.5*WIDTH // 24, (10.25 + i)*HEIGHT // 16, WIDTH // 12, HEIGHT // 128))
        i = 1
        for p in self.game.turn_manager.players:
            if p != self.game.turn_manager.get_vision_character():
                pg.draw.rect(screen, CYAN, (21.5*WIDTH // 24, (10.25 + i)*HEIGHT // 16, 
                    ((WIDTH // 12)*p.MP) // PLAYER_MAX_MP, HEIGHT // 128))
                i += 1
    def draw_xpbar(self, screen):
        pg.draw.rect(screen, DARKGREY, 
                (WIDTH // 3, 14.75*HEIGHT // 16, WIDTH //3, HEIGHT // 128))
        pg.draw.rect(screen, GOLD, (WIDTH // 3, 14.5*HEIGHT // 16, 
                    ((WIDTH // 3)*self.game.turn_manager.get_vision_character().xp) // 100, HEIGHT // 128))
        for i in range(1, len(self.game.turn_manager.players)):
            pg.draw.rect(screen, DARKGREY, 
                (21.5*WIDTH // 24, (9.9 + i)*HEIGHT // 16, WIDTH // 12, HEIGHT // 254))
        i = 1
        for p in self.game.turn_manager.players:
            if p != self.game.turn_manager.get_vision_character():
                pg.draw.rect(screen, GOLD, (21.5*WIDTH // 24, (10 + i)*HEIGHT // 16, 
                    ((WIDTH // 12)*p.xp) // 100, HEIGHT // 64))
                i += 1

    def draw_shapes(self, screen):
        bar_img = pg.image.load('assets/img/bar.png').convert_alpha()
        bar_img = pg.transform.scale(bar_img, (3*WIDTH // 8, 7*HEIGHT // 128))
        screen.blit(bar_img, (15*WIDTH // 48, 14.925*HEIGHT // 16))

    def create_buttons_dict(self):
        return {
            "quests": {
                "text": "Quests",
                "on_click": None,
                "image": path.join(self.imgs, "items/book_01g.png"),
                "rect": None
            },
            "inventory": {
                "text": "Inventory",
                "on_click": print("inventory"),
                "image": path.join(self.game.assets_folder, "sprites/chest/3.png"),
                "rect": None
            },
            "stats": {
                "text": "Stats",
                "on_click": None,
                "image": path.join(self.imgs, "items/cotton_01a.png"),
                "rect": None

            },
            "map": {
                "text": "Map",
                "on_click": None,
                "image": path.join(self.imgs, "location.png"),
                "rect": None
            }
        }

    def draw_buttons(self, screen):
        l = len(self.button_dict)
        circle_size = WIDTH // 20
        step = WIDTH // 100
        size = circle_size + step
        offset = 6

        circle_img = pg.image.load(path.join(self.imgs, "store/background.png")).convert_alpha()
        circle_img = pg.transform.scale(circle_img, (size, size))

        for i in range(l + 1):
            screen.blit(circle_img, (WIDTH - (i*size), HEIGHT // 200))
        i = 1
        for b in self.button_dict.keys():
            print(b)
            b_img = pg.image.load(self.button_dict[b]["image"]).convert_alpha()
            b_img = pg.transform.scale(b_img, (circle_size, circle_size))
            screen.blit(b_img, (WIDTH + offset - (i*size), offset + HEIGHT // 200))
            # self.button_dict[b]["rect"] = b_img.get_rect()
            i += 1

    # def is_clicked(self, mouse_pos):
    #     for button in self.button_dict:
    #         if self.button_dict[button]["rect"].collidepoint(mouse_pos):
    #             return True

    # def get_clicked_event(self, mouse_pos):
    #     for button in self.button_dict.keys():
    #         if self.button_dict[button]["rect"].collidepoint(mouse_pos):
    #             return self.button_dict[button]["on_click"]

    def hud_event(self, mouse_pos):
        if is_clicked():
            get_clicked_event(mouse_pos)



    def draw(self, screen):
        """Draw the whole HUD
        """
        self.draw_healthbars(screen)
        self.draw_manabars(screen)
        self.draw_xpbar(screen)
        # self.draw_shapes(screen)
        self.draw_buttons(screen)