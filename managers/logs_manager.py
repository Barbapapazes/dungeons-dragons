"""Create the game logger"""

import time

import pygame as pg
from config.colors import WHITE
from logger import logger


class LogsManager:
    """Used to create an in-game logger"""

    def __init__(self, x, y, width, height, font, fontsize, draw_text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.font = font
        self.fontsize = fontsize
        self.draw_text = draw_text

        self.messages = []

        self.visible = True

        self.offset = 0

        self.create_screen()

    def create_screen(self):
        """Create the log screen"""
        self.screen_logs = pg.Surface((self.width, self.height)).convert_alpha()
        self.screen_logs.fill((0, 0, 0, 180))

    def event(self, event):
        """Event

        Args:

            event (Event)
        """
        if event.type == pg.KEYUP:
            if event.key == pg.K_k:
                self.visible = not self.visible
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:
                logger.debug('up')
                self.offset += 6
                if self.offset > len(self.messages) * self.fontsize:
                    self.offset = len(self.messages) * self.fontsize
            elif event.button == 5:
                logger.debug('down')
                self.offset -= 6
                logger.debug("%s, %s", self.offset, len(self.messages) * self.fontsize)
                if self.offset < - self.height:
                    self.offset = - self.height

    def draw(self, screen):
        """Draw the logger 

        Args:
            screen (Surface)
        """
        screen.blit(self.screen_logs, (self.x, self.y))
        for index, message in enumerate(self.messages):
            _y = self.height - (index * self.fontsize) + self.offset
            if 0 < _y <= self.height:
                self.draw_text(message, self.font, self.fontsize, WHITE, 0, _y, screen=screen, align="sw")

    def add_log(self, message):
        """Add a message to the logger

        Args:
            message (str)
        """
        named_tuple = time.localtime()
        time_string = time.strftime("%H:%M:%S", named_tuple)
        message = f"{time_string} - {message}"
        logger.info("Logs: %s", message)
        self.messages.insert(0, message)
