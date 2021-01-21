

import pygame as pg
from sprites import player
from config.colors import YELLOW_LIGHT
from config.window import WIDTH, HEIGHT
from config.inventory import INVENTORY_TILESIZE, INVENTORY_SLOT_GAP

class StatsWindow():

    def __init__(self, game):
        self.game = game
        self.background = pg.image.load("assets/img/store/background.png").convert_alpha()
        self.background = pg.transform.scale(self.background, (2*WIDTH // 3, 12*HEIGHT // 20))
        
        self.view_stats = False

    def draw_active_player_stats(self, screen):
        p = self.game.turn_manager.get_vision_character()
        
        for index, (k, v) in enumerate(p.characteristics.items()):
            self.game.draw_text(k + ": " + str(v),
                                    self.game.title_font, 40, YELLOW_LIGHT, 7*WIDTH // 12, (6 + index)*HEIGHT // 20, 
                                    screen = screen)
            
        self.game.draw_text("HP : " + str(p.health)  + "/" + str(p.max_HP),
                        self.game.title_font, 40, YELLOW_LIGHT, WIDTH // 3, 8*HEIGHT // 20, 
                        screen = screen)
        self.game.draw_text("Mana : " + str(p.MP) + "/" + str(p.max_MP),
                        self.game.title_font, 40, YELLOW_LIGHT, WIDTH // 3, 9*HEIGHT // 20, 
                        screen = screen)
        self.game.draw_text("Xp : " + str(p.xp) + "/ 100",
                        self.game.title_font, 40, YELLOW_LIGHT, WIDTH // 3, 10*HEIGHT // 20, 
                        screen = screen)
        self.game.draw_text("Gold : " + str(p.gold),
                        self.game.title_font, 40, YELLOW_LIGHT, WIDTH // 3, 11*HEIGHT // 20, 
                        screen = screen)
        screen.blit(p.image, (WIDTH //3, 5*HEIGHT //20))

    def draw(self, screen):
        screen.blit(self.background, (WIDTH //6, 3*HEIGHT //20))
        if self.view_stats:
            self.game.draw_text(
                "Stats", self.game.title_font, 60, YELLOW_LIGHT, WIDTH // 2, 0, align="n", screen=screen)
            self.draw_active_player_stats(screen)
