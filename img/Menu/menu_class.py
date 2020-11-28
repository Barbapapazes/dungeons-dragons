import pygame
import pygame_widgets as pw



pygame.init()
police=pygame.font.Font("None",40)
police2=pygame.font.Font("Sindentosa.ttf",40)
police_small=pygame.font.Font("Pixeled.ttf",20)

HEIGHT_BUTTON=50
WIDTH_BUTTON=350
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

surface= pygame.display.set_mode((1024,768))
class classe_Menu_prin():

    def __init__(self):
        self.New_Game = pw.Button(
                surface, 337, 250, WIDTH_BUTTON, HEIGHT_BUTTON, text='New Game',
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
                surface, 337, 350, WIDTH_BUTTON, HEIGHT_BUTTON, text='Charge Game ',
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
                surface, 337, 450,WIDTH_BUTTON , HEIGHT_BUTTON, text='Options',
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
                surface, 337, 550, WIDTH_BUTTON, HEIGHT_BUTTON, text='Leave to desktop',
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



class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

