"""Create the game logger"""

from config.colors import WHITE
import pygame as pg
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

        self.create_screen()

    def create_screen(self):
        """Create the log screen"""
        self.screen_logs = pg.Surface((self.width, self.height)).convert_alpha()
        self.screen_logs.fill((0, 0, 0, 180))

    def draw(self, screen):
        """Draw the logger 

        Args:
            screen (Surface)
        """
        screen.blit(self.screen_logs, (self.x, self.y))
        for index, message in enumerate(self.messages):
            self.draw_text(message, self.font, self.fontsize, WHITE, 0,
                           self.height - (index * self.fontsize), screen=screen, align="sw")

    def add_log(self, message):
        """Add a message to the logger

        Args:
            message (str)
        """
        if len(self.messages) > 5:
            self.messages.pop()
        logger.info("Logs: %s", message)
        self.messages.insert(0, message)

    def update(self):
        pass
