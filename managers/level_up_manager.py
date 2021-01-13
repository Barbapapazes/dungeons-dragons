"""Level up manager"""
from config.window import WIDTH
from config.colors import BEIGE
from logger import logger


class LevelUpManager:
    """Create a level up manager """

    def __init__(self, game):
        self.game = game

        self.active = False
        self.time = 0
        self.time_out = 3000 / 1000
        self.content = {
            "title": "",
            "content": ""
        }

    def update(self):
        if self.game.turn_manager.is_active_player() and self.game.turn_manager.active().level_up():
            # il faut faire le check ailleurs et donc ativer la notif ailleurs
            self.active = True

        if self.active:
            self.time += self.game.dt
            if self.time > self.time_out:
                self.time = 0
                self.active = False

    def draw(self, screen):
        if self.active:
            self.game.draw_text(self.content["title"], self.game.title_font, 48,
                                BEIGE, WIDTH - 48, 48, align="e", screen=screen)
