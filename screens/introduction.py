"""Introcution screen"""

from config.sprites import ASSETS_BOOK_NEXT
from config.colors import BEIGE, BLACK
from itertools import cycle
from sprites.animated import Book
import pygame as pg
from config.screens import BACKGROUND_INTRODUCTION, GAME, MENU, TRANSITION_OUT
from config.window import HEIGHT, WIDTH
from window import _Elements
from logger import logger


class Introduction(_Elements):
    """Introduction screen"""

    def __init__(self):
        self.name = MENU
        self.next = GAME
        super(Introduction, self).__init__(self.name, self.next, 'introduction', '0001.png', {})

        self.new()

    def new(self):
        """Create a fresh screen"""
        self.frames = list()
        for frame in BACKGROUND_INTRODUCTION:
            self.frames.append(pg.transform.scale(frame, (WIDTH, HEIGHT)))

        self.frames = cycle(self.frames)
        self.background = next(self.frames)

        self.frame_time = 80 / 1000
        self.frame_timer = 0

        self.pages = 2

        self.animated = pg.sprite.Group()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.book = Book(self, WIDTH // 2, HEIGHT // 2, 2 * WIDTH // 4)

        self.win = pg.Surface((WIDTH, HEIGHT)).convert_alpha()

    def run(self, surface, keys, mouse, dt):
        """Run states"""
        self.screen = surface
        self.keys = keys
        self.mouse = mouse
        self.dt = dt
        update_level = self.states_dict[self.state]
        if self.state != 'normal':
            self.draw()
        update_level()

    def normal_run(self):
        """Run the normal state"""
        self.update_background()
        if self.book.frame_count // self.book.frame_per_image < len(self.book.frames) - 1:
            self.animated.update()
        super().events_buttons()
        self.draw()

    def get_events(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                self._next()

    def _next(self):
        self.pages -= 1
        if self.pages == 0:
            self.set_state(TRANSITION_OUT)
        self.book.set_frames(ASSETS_BOOK_NEXT)

    def update_background(self):
        """Used to update the background"""
        self.frame_timer += self.dt
        if self.frame_timer >= self.frame_time:
            self.frame_timer -= self.frame_time
            self.background = next(self.frames)

    def draw(self):
        """Draw content"""
        super().draw_elements("Once upon a time")
        self.win.fill((0, 0, 0, 0))
        self.animated.draw(self.win)
        self.draw_text("Press SPACE to continue", self.button_font, 48,
                       BEIGE, WIDTH // 2, HEIGHT, align="s", screen=self.win)
        self.screen.blit(self.win, (0, 0))
