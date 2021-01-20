"""Notification manager"""
import pygame as pg
from config.colors import BEIGE
from config.window import WIDTH
from logger import logger


class NotificationManager:
    """Create a notification manager"""

    def __init__(self, game):
        self.game = game

        self.active = False
        self.time = 0
        self.time_out = 3000 / 1000
        self.content = {
            "title": "",
            "content": ""
        }
        self.size = 48
        self.notification_screen = pg.Surface((250, 100)).convert_alpha()
        self.notification_screen.fill(pg.Color(0, 0, 0, 220))
        self.notification_rect = self.notification_screen.get_rect()
        self.notification_rect.topright = (WIDTH - 12, 12)

    def update(self):
        if self.active:
            self.time += self.game.dt
            if self.time > self.time_out:
                self.time = 0
                self.active = False

    def draw(self, screen):
        if self.active:
            screen.blit(self.notification_screen, self.notification_rect)
            self.game.draw_text(self.content["title"], self.game.title_font, self.size,
                                BEIGE, WIDTH - int(self.size * 1/4), self.size, align="e", screen=screen)
            self.game.draw_text(self.content["content"], self.game.text_font, int(self.size * 1.5 / 4),
                                BEIGE, WIDTH - int(self.size * 1/4), self.size * 2, align="e", screen=screen)
