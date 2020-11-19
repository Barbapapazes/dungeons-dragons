"""Menu screen"""

import pygame as pg
import pygame_widgets as pw
from os import path
from window import _State
from config.window import WIDTH, HEIGHT
from config.screens import GAME, MENU, TRANSITION_OUT


HAUTEUR_BOUTON=50
LARGEUR_BOUTON=350
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')


class Menu(_State):
    """Menu screen"""

    def __init__(self):
        self.name = MENU
        super(Menu, self).__init__(self.name)
        self.next = GAME
        self.background = pg.Surface((WIDTH, HEIGHT))
        self.startup(0, 0)

        #Backgroud image 
        self.image=pg.image.load("./img/Menu/background.jpg").convert()
        self.image=pg.transform.scale(self.image,(WIDTH,HEIGHT))




        #Buttons 
        self.New_Game = pw.Button(
                self.background, 337, 250, LARGEUR_BOUTON, HAUTEUR_BOUTON, text='New Game',
                fontSize=50, margin=20,
                inactiveColour=(13, 71, 32),
                hoverColour=(9,48,22),
                pressedColour=(9, 48, 22), radius=20,
                onClick=self.Change_state,
                textVAlign="centre",
                textHAlign="centre"
            )
        
    def Change_state(self):
        #changement etat
        super().set_state(TRANSITION_OUT)


    def startup(self, dt, game_data):
        """Initialize data at scene start."""
        self.game_data = game_data
        self.dt = dt
        self.background.fill((0, 255, 0))
        pg.init()
        pg.display.set_mode((WIDTH,HEIGHT))
        super().setup_transition()

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
        self.draw()

    def get_events(self, event):
        """Events loop"""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                super().set_state(TRANSITION_OUT)
            if event.key == pg.K_p:
                self.game_data['game_data']['count'] += 1


    def affiche(self):
        print('coucou')


    def draw(self):
        """Draw content"""
        self.screen.blit(self.background, (0, 0))
        self.background.blit(self.image,(0,0))
        self.New_Game.listen(pg.event.get())
        self.New_Game.draw()
        
   