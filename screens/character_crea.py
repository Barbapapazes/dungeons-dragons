""""""

import pygame as pg
import pygame_widgets as pw
from window import _State
from config.window import WIDTH, HEIGHT
from config.screens import GAME, MENU, TRANSITION_OUT
import config.colors as couleur


class Character_crea(_State):
    """Creation_player"""

    def __init__(self):
        self.name = MENU
        super(Character_crea, self).__init__(self.name)
        self.next = GAME

        self.background = pg.Surface((WIDTH, HEIGHT))
        self.startup(0, 0)
        #Backgroud image 
        self.image=pg.image.load("./img/Character_crea/background.jpg").convert()
        self.image=pg.transform.scale(self.image,(WIDTH,HEIGHT))

        #titre du jeu 
        self.police=pg.font.Font("./assets/fonts/Enchanted Land.otf",100)
        self.titre=self.police.render("NewGame",True,couleur.YELLOW_LIGHT)

        #textbox
        self.name= pw.TextBox(self.background, 100, 100, 800, 80, fontSize=50,
                  borderColour=(255, 0, 0), textColour=(0, 200, 0),
                  onSubmit=self.output, radius=10, borderThickness=5)

        

    def output(self):
        # Get text in the textbox
        print(self.name.getText())

    def startup(self, dt, game_data):
        """Initialize data at scene start."""
        self.game_data = game_data
        self.dt = dt
        self.background.fill((0, 255, 0))
        pg.init()
        pg.display.set_mode((WIDTH,HEIGHT))
        super().setup_transition()

    def run(self, surface, keys, dt):
        """Run states"""
        self.screen = surface
        self.keys = keys
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
                self.game_data['count'] += 1
                print(self.game_data["count"])

    def draw(self):
        events=pg.event.get()
        self.screen.blit(self.background, (0, 0))
        self.background.blit(self.image,(0,0))
        self.background.blit(self.titre,(375,0))

        self.name.listen(events)
        self.name.draw()
