import pygame
import pygame_widgets as pw

pygame.init()
police=pygame.font.Font("Pixeled.ttf",40)
police2=pygame.font.Font("Sindentosa.ttf",40)
police_small=pygame.font.Font("Pixeled.ttf",20)

HAUTEUR_BOUTON=50
LARGEUR_BOUTON=350

surface= pygame.display.set_mode((1024,768))
class classe_Menu_prin():

    def __init__(self):
        self.New_Game = pw.Button(
                surface, 337, 250, LARGEUR_BOUTON, HAUTEUR_BOUTON, text='New Game',
                fontSize=50, margin=20,
                inactiveColour=(13, 71, 32),
                hoverColour=(9,48,22),
                pressedColour=(9, 48, 22), radius=20,
                onClick=lambda: print('Click'),
                font=police2,
                textVAlign="centre",
                textHAlign="centre"
            )

        self.Charge_game = pw.Button(
                surface, 337, 350, LARGEUR_BOUTON, HAUTEUR_BOUTON, text='Charge Game ',
                fontSize=50, margin=20,
                inactiveColour=(13, 71, 32),
                hoverColour=(9,48,22),
                pressedColour=(9, 48, 22), radius=20,
                onClick=lambda: print('Click'),
                font=police2,
                textVAlign="centre",
                textHAlign="centre"
            )

        self.Options= pw.Button(
                surface, 337, 450,LARGEUR_BOUTON , HAUTEUR_BOUTON, text='Options',
                fontSize=50, margin=20,
                inactiveColour=(13, 71, 32),
                hoverColour=(9,48,22),
                pressedColour=(9, 48, 22), radius=20,
                onClick=lambda: print('Click'),
                font=police2,
                textVAlign="centre",
                textHAlign="centre"
            )

        self.Quiter= pw.Button(
                surface, 337, 550, LARGEUR_BOUTON, HAUTEUR_BOUTON, text='Leave to desktop',
                fontSize=50, margin=20,
                inactiveColour=(13, 71, 32),
                hoverColour=(9,48,22),
                pressedColour=(9, 48, 22), radius=20,
                onClick=lambda: print('Click'),
                font=police2,
                textVAlign="centre",
                textHAlign="centre"
            )
        self.enable=True

    def affichage(self,event):
        if self.enable : 
            self.New_Game.listen(event)
            self.New_Game.draw()

            self.Charge_game.listen(event)
            self.Charge_game.draw()

            self.Options.listen(event)
            self.Options.draw()

            self.Quiter.listen(event)
            self.Quiter.draw()
