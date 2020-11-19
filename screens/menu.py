"""Menu screen"""

import pygame as pg
import pygame_widgets as pw
from window import _State
from config.window import WIDTH, HEIGHT
from config.screens import GAME, MENU, TRANSITION_OUT,CREDITS,LOAD_GAME
import config.colors as couleur


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
        self.image=pg.image.load("./img/Menu/background2.jpg").convert()
        self.image=pg.transform.scale(self.image,(WIDTH,HEIGHT))


        #titre du jeu 
        self.police=pg.font.Font("./assets/fonts/Enchanted Land.otf",150)
        self.titre=self.police.render("Le Titre Du Jeu  ",True,couleur.YELLOW_LIGHT)

        #Buttons 
        self.police_button=pg.font.Font("./assets/fonts/Enchanted Land.otf",50)
        self.New_Game = pw.Button(
                self.background, 337, 250, LARGEUR_BOUTON, HAUTEUR_BOUTON, text='New Game',
                fontSize=20, margin=20,
                inactiveColour=couleur.BEIGE,
                hoverColour=couleur.YELLOW_LIGHT,
                pressedColour=(9, 48, 22), radius=10,
                onClick=self.Change_state,
                onClickParams=[CREDITS],
                font=self.police_button,
                textVAlign="centre",
                textHAlign="centre"
            )
        self.Charge_game = pw.Button(
                self.background, 337, 350, LARGEUR_BOUTON, HAUTEUR_BOUTON, text='Charge Game ',
                fontSize=20, margin=20,
                inactiveColour=couleur.BEIGE,
                hoverColour=couleur.YELLOW_LIGHT,
                pressedColour=(9, 48, 22), radius=10,
                onClick=self.Change_state,
                onClickParams=[LOAD_GAME],
                font=self.police_button,
                textVAlign="centre",
                textHAlign="centre"
            )
        
        self.Options= pw.Button(
                self.background, 337, 450,LARGEUR_BOUTON , HAUTEUR_BOUTON, text='Options',
                fontSize=20, margin=20,
                inactiveColour=couleur.BEIGE,
                hoverColour=couleur.YELLOW_LIGHT,
                pressedColour=(9, 48, 22), radius=10,
                onClick=self.Change_state,
                onClickParams=[CREDITS],
                font=self.police_button,
                textVAlign="centre",
                textHAlign="centre"
            )

        self.Quiter= pw.Button(
                self.background, 337, 550, LARGEUR_BOUTON, HAUTEUR_BOUTON, text='Leave to desktop',
                fontSize=20, margin=20,
                inactiveColour=couleur.BEIGE,
                hoverColour=couleur.YELLOW_LIGHT,
                pressedColour=(9, 48, 22), radius=10,
                onClick=self.Stop,
                font=self.police_button,
                textVAlign="centre",
                textHAlign="centre"
            )

    def Change_state(self,*etat):
        #changement etat
        print(etat[0])
        self.next=etat[0]
        super().set_state(TRANSITION_OUT)

    def Stop(self):
        pg.quit()
        quit()


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
        events=pg.event.get()
        self.screen.blit(self.background, (0, 0))
        self.background.blit(self.image,(0,0))
        self.background.blit(self.titre,(220,50))

        self.New_Game.listen(events)
        self.New_Game.draw()

        self.Charge_game.listen(events)
        self.Charge_game.draw()

        self.Options.listen(events)
        self.Options.draw()

        self.Quiter.listen(events)
        self.Quiter.draw()

        
   