import pygame as pg
from os import path
from sprites.player import Player
from config.window import TILESIZE, WIDTH, HEIGHT
from config.colors import RED, GREEN, CYAN, DARKGREY, GOLD, BLACK
from config.sprites import ITEMS, PLAYER_MAX_HP, PLAYER_MAX_MP
from utils.container import Container


class Hud:
    """Create the hud"""

    def __init__(self, game):
        self.game = game
        self.button_dict = self.create_buttons_dict()
        self.buttons = list()
        self._size = WIDTH // 20 + WIDTH // 100
        self.create_buttons()

    def draw_healthbars(self, screen):
        """Draw health bars for all players

        Args:
            screen (Surface)
        """
        player = self.game.turn_manager.get_vision_character()
        health = player.health if player is not None else 0
        pg.draw.rect(screen, RED,
                     (WIDTH // 3, 15*HEIGHT // 16, WIDTH // 3, HEIGHT // 36))
        pg.draw.rect(screen, GREEN, (WIDTH // 3, 15 * HEIGHT // 16, ((WIDTH // 3)
                                                                     * health) // PLAYER_MAX_HP, HEIGHT // 36))
        for i in range(1, len(self.game.turn_manager.players)):
            pg.draw.rect(screen, RED,
                         (21.5*WIDTH // 24, (10 + i) * HEIGHT // 16, WIDTH // 12, HEIGHT // 64))
        i = 1
        for p in self.game.turn_manager.players:
            if p != self.game.turn_manager.get_vision_character():
                pg.draw.rect(screen, GREEN, (21.5 * WIDTH // 24, (10 + i) * HEIGHT // 16,
                                             ((WIDTH // 12) * p.health) // PLAYER_MAX_HP, HEIGHT // 64))
                i += 1

    def draw_manabars(self, screen):
        """Draw the mana bar

        Args:
            screen (Surface)
        """
        player = self.game.turn_manager.get_vision_character()
        mana = player.MP if player is not None else 0
        pg.draw.rect(screen, DARKGREY,
                     (WIDTH // 3, 15.5*HEIGHT // 16, WIDTH // 3, HEIGHT // 66))
        pg.draw.rect(screen, CYAN, (WIDTH // 3, 15.5*HEIGHT // 16, ((WIDTH // 3)
                                                                    * mana) // PLAYER_MAX_MP, HEIGHT // 68))
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
        """Draw the xp bar

        Args:
            screen (Surface)
        """
        player = self.game.turn_manager.get_vision_character()
        xp = player.xp if player is not None else 0
        pg.draw.rect(screen, DARKGREY,
                     (WIDTH // 3, 14.75*HEIGHT // 16, WIDTH // 3, HEIGHT // 128))
        pg.draw.rect(screen, GOLD, (WIDTH // 3, 14.5*HEIGHT // 16, ((WIDTH // 3)
                                                                    * xp) // 100, HEIGHT // 128))
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
        """Draw the background health bar

        Args:
            screen (Surface)
        """
        bar_img = pg.image.load(path.join("assets", "img", "bar.png")).convert_alpha()
        bar_img = pg.transform.scale(bar_img, (3 * WIDTH // 8, 7 * HEIGHT // 128))
        screen.blit(bar_img, (15*WIDTH // 48, 14.90 * HEIGHT // 16))

    def create_buttons_dict(self):
        return {
            "quests": {
                "state": "menu",
                "on_click": None,
                "image": path.join(self.game.img_folder, "items", "book_01g.png"),
                "rect": None
            },
            "inventory": {
                "state": "inventory",
                "on_click": None,
                "image": path.join(self.game.assets_folder, "sprites", "chest", "3.png"),
                "rect": None
            },
            "stats": {
                "state": "stats",
                "on_click": None,
                "image": path.join(self.game.img_folder, "items", "cotton_01a.png"),
                "rect": None

            },
            "map": {
                "state": "map",
                "on_click": None,
                "image": path.join(self.game.img_folder, "location.png"),
                "rect": None
            }
        }

    def create_buttons(self):
        max_x = WIDTH
        min_x = WIDTH - self._size*len(self.button_dict)
        for _x in range(min_x, max_x, self._size):
            self.buttons.append(HudButton(_x, 0, self._size, BLACK))
        for i, (k, _) in enumerate(self.button_dict.items()):
            self.buttons[i].item = pg.image.load(self.button_dict[k]["image"]).convert_alpha()
            self.buttons[i].set_name(k)

    def get_all_buttons(self):
        return self.buttons

    def draw_all_buttons(self, screen):
        """Draw"""
        for b in self.get_all_buttons():
            b.draw(screen)
            b.draw_image(screen)

    def get_relate_button_state(self, mouse_pos):
        """Get the pressed button

        Args:
            mouse_pos (typle): x, y

        Returns:
            str: the button pressed button
        """
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
        """Draw the image"""
        self.offset = 14
        if self.item:
            image = pg.transform.scale(self.item, (self.size - self.offset, self.size - self.offset))
            _x = image.get_width()
            _y = image.get_height()
            # pg.draw.rect(screen, (0, 255, 0), pg.Rect(self.x, self.y, _x, _y), 1)

            screen.blit(image, (self.x + self.offset // 2, self.y + self.offset // 2))
