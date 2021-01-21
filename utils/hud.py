import pygame as pg
from os import path
from sprites.player import Player
from config.window import WIDTH, HEIGHT
from config.colors import RED, GREEN, CYAN, DARKGREY, GOLD, BLACK
from config.sprites import PLAYER_MAX_HP, PLAYER_MAX_MP
from utils.container import Container


class Hud:
    """Create the hud"""

    def __init__(self, game):
        self.game = game
        self.imgs = game.img_folder
        self.button_dict = self.create_buttons_dict()
        self.buttons = list()
        self._size = WIDTH // 20 + WIDTH // 100
        self.create_buttons()

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
                "state": "menu",
                "on_click": None,
                "image": path.join(self.imgs, "items/book_01g.png"),
                "rect": None
            },
            "inventory": {
                "state": "inventory",
                "on_click": None,
                "image": path.join(self.game.assets_folder, "sprites/chest/3.png"),
                "rect": None
            },
            "stats": {
                "state": "stats",
                "on_click": None,
                "image": path.join(self.imgs, "items/cotton_01a.png"),
                "rect": None

            },
            "map": {
                "state": "map",
                "on_click": None,
                "image": path.join(self.imgs, "location.png"),
                "rect": None
            }
        }

    def create_buttons(self):
        max_x = WIDTH
        min_x = WIDTH - self._size*len(self.button_dict)
        min_y = 00
        max_y = self._size
        for _x in range(min_x, max_x, self._size):
            self.buttons.append(HudButton(_x, 0, self._size, BLACK))
        for i, (k, v) in enumerate(self.button_dict.items()):
            self.buttons[i].item = pg.image.load(self.button_dict[k]["image"]).convert_alpha()
            self.buttons[i].set_name(k)

    def get_all_buttons(self):
        return self.buttons

    def draw_all_buttons(self, screen):
        for b in self.get_all_buttons():
            b.draw(screen)
            b.draw_image(screen)
    
    def get_relate_button_state(self, mouse_pos):
        for button in self.get_all_buttons():
            if button.rect.collidepoint(mouse_pos):
                return button.name

    def draw(self, screen):
        """Draw the whole HUD
        """
        self.draw_healthbars(screen)
        self.draw_manabars(screen)
        self.draw_xpbar(screen)
        self.draw_all_buttons(screen)
        self.draw_shapes(screen)

class HudButton(Container):

    def set_name(self, name):
        self.name = name
    
    def draw_image(self, screen):
        if self.item:
            offset = 12
            image = pg.transform.scale(self.item, (self.size, self.size))
            _x = image.get_width()
            _y = image.get_height()
            pg.draw.rect(screen, (0, 255, 0), pg.Rect(self.x, self.y, _x, _y), 1)

            screen.blit(image, (self.x, self.y))
