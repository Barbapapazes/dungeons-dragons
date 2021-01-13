

import pygame as pg
from sprites import player
from config.colors import YELLOW_LIGHT
from config.window import WIDTH, HEIGHT

class StatsWindow():

    def __init__(self):
        self.background = pg.image.load("assets/img/store/background.png").convert_alpha()

        
    def print_characteristics(self, target, screen):
        for index, (k, v) in enumerate(target.characteristics.items()):
            target.game.draw_text(k + ": " + str(v),
                                    target.game.title_font, 30, YELLOW_LIGHT, WIDTH // 2, HEIGHT // 10, 
                                    screen = screen)


    


