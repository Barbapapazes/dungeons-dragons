""""""

import pygame as pg
from pygame_widgets import Button, Slider, TextBox, Resize, Translate
from window import _State
from os import path
from config.window import WIDTH, HEIGHT
from config.screens import GAME, MENU, TRANSITION_OUT
from config.colors import YELLOW_LIGHT, RED, BLACK, BEIGE, GREEN_DARK, WHITE
from config.sprites import WIDTH_CHARACTER, HEIGHT_CHARACTER, USABLE_POINTS
from config.buttons import MARGIN_BUTTON, RADIUS_BUTTON, HEIGHT_SLIDER, WIDTH_SLIDER
from logger import logger


class CharacterCreation(_State):
    """Creation_player"""

    def __init__(self):
        self.name = MENU
        super(CharacterCreation, self).__init__(self.name)
        self.next = GAME

        # Background image
        image = pg.image.load(
            path.join(
                self.img_folder,
                'character_creation',
                'background.jpg')).convert()
        self.image = pg.transform.scale(image, (WIDTH, HEIGHT))

        # Buttons
        self.font_button = pg.font.Font(self.button_font, 50)
        self.fontsize = 20

        self.new()
        self.create_buttons()
        self.create_animations()
        self.create_sliders()

        self.slider_x = Slider(self.image, 100, 100, 800, 40, min=0, max=99, step=1)

        # textbox
        # self.name = TextBox(
        #     self.background,
        #     20,
        #     100,
        #     400,
        #     40,
        #     fontSize=50,
        #     borderColour=RED,
        #     textColour=(
        #         0,
        #         200,
        #         0),
        #     onSubmit=self.output,
        #     radius=10,
        #     borderThickness=4)

        """Chevaliers menant une quête,seigneurs conquérants,champions royaux, fantassins d'élite,mercenaires endurcis et rois-bandits, tous partagent une maîtrise inégalée des armes et des armures ainsi /
        qu'une connaissance approfondie des compétences de combat./
        Tous connaissent bien la mort, l'infligeant autant qu'ils lui font face."""

    def new(self):
        self.selected = 0
        self.selected_character = self.get_selected_characters()

    def create_buttons(self):
        self.confirm_creation_btn = Button(
            self.image, 500, 717, 0, 0, text='Start !',
            fontSize=20, margin=MARGIN_BUTTON,
            inactiveColour=BEIGE,
            hoverColour=YELLOW_LIGHT,
            pressedColour=GREEN_DARK, radius=RADIUS_BUTTON,
            onClick=self.next_action)

    def create_animations(self):
        self.resize_confirm_creation_btn = Resize(
            self.confirm_creation_btn, 1, 200, 30)
        self.translate_confirm_creation_btn = Translate(
            self.confirm_creation_btn, 1, 400, 700)

        self.resize_inverse_confirm_creation_btn = Resize(
            self.confirm_creation_btn, 1, 0, 0)
        self.translate_inverse_confirm_creation_btn = Translate(
            self.confirm_creation_btn, 1, 500, 717)

    def create_sliders_dict(self):
        return {
            "str": {
                "max": self.get_selected_characters()["characteristics"]["str"]["max"],
                "start": self.get_selected_characters()["characteristics"]["str"]["base"],
            },
            "dex": {
                "max": self.get_selected_characters()["characteristics"]["dex"]["max"],
                "start": self.get_selected_characters()["characteristics"]["dex"]["base"],
            },
            "con": {
                "max": self.get_selected_characters()["characteristics"]["con"]["max"],
                "start": self.get_selected_characters()["characteristics"]["con"]["base"],
            },
            "int": {
                "max": self.get_selected_characters()["characteristics"]["int"]["max"],
                "start": self.get_selected_characters()["characteristics"]["int"]["base"],
            },
            "wis": {
                "max": self.get_selected_characters()["characteristics"]["wis"]["max"],
                "start": self.get_selected_characters()["characteristics"]["wis"]["base"],
            },
            "cha": {
                "max": self.get_selected_characters()["characteristics"]["cha"]["max"],
                "start": self.get_selected_characters()["characteristics"]["cha"]["base"],
            },
        }

    def create_sliders(self):
        self.sliders = list()
        logger.info("Create all sliders from character creation")
        for index, (key, value) in enumerate(
                self.create_sliders_dict().items()):
            x = 0
            y = 350 + (index % 3) * 70
            if index in [0, 1, 2]:
                x = 700
            else:
                x = 20
            self.sliders.append(
                self.create_slider(
                    key.upper(),
                    x,
                    y,
                    WIDTH_SLIDER,
                    HEIGHT_SLIDER,
                    self.image,
                    0,
                    value["max"],
                    1,
                    value["start"]
                    ))

    @staticmethod
    def create_slider(name, x, y, width, height, surface, min, max, step,start):
        return Curseur(
            name, x, y, width, height, surface, min, max, step, start
        )

    def get_selected_characters(self):
        name = list(self.get_characters().keys())[self.selected]
        return self.get_characters()[name]

    def get_characters(self):
        return {
            "fighter": {
                "name": "fighter",
                "image": path.join(self.img_folder, "character_creation", "guerrier.png"),
                "characteristics": {
                    "str": {
                        "base": 3,
                        "max": 12
                    },
                    "dex": {
                        "base": 0,
                        "max": 4
                    },
                    "con": {
                        "base": 2,
                        "max": 12
                    },
                    "int": {
                        "base": 2,
                        "max": 12
                    },
                    "wis": {
                        "base": 2,
                        "max": 12
                    },
                    "cha": {
                        "base": 2,
                        "max": 12
                    }
                }
            },
            "mage": {
                "name": "mage",
                "image": path.join(self.img_folder, "character_creation", "mage.png"),
                "characteristics": {
                    "str": {
                        "base": 0,
                        "max": 7
                    },
                    "dex": {
                        "base": 2,
                        "max": 12
                    },
                    "con": {
                        "base": 2,
                        "max": 12
                    },
                    "int": {
                        "base": 2,
                        "max": 12
                    },
                    "wis": {
                        "base": 2,
                        "max": 12
                    },
                    "cha": {
                        "base": 2,
                        "max": 12
                    }
                }
            }
        }

    def sum_points(self):
        return sum(x.getvalue() for x in self.sliders)

    def remaining_points(self):
        return USABLE_POINTS - self.sum_points()

    def output(self):
        # Get text in the textbox
        print("ok")

    def run(self, surface, keys, mouse, dt):
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
        self.events_buttons()
        self.events_sliders()
        self.draw()

    def events_buttons(self):
        events = pg.event.get()
        self.confirm_creation_btn.listen(events)

    def events_sliders(self):
        events = pg.event.get()
        for slider in self.sliders:
            slider.listen(events)

        self.slider_x.listen(events)

    def get_events(self, event):
        """Events loop"""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                self.selected += 1
                if self.selected > len(list(self.get_characters().keys())) - 1:
                    self.selected = len(list(self.get_characters().keys())) - 1
                self.selected_character = self.get_selected_characters()
                self.create_sliders()
            if event.key == pg.K_LEFT:
                self.selected -= 1
                if self.selected < 0:
                    self.selected = 0
                self.selected_character = self.get_selected_characters()
                self.create_sliders()

    def next_action(self):
        super().set_state(TRANSITION_OUT)
        # initialisation du personnage
        # creation de la sauvegarde

    def draw(self):
        self.draw_background()
        self.draw_title()
        self.draw_characteristic()
        self.draw_sliders()
        self.draw_points()

        # # self.name.listen(events)
        # # self.name.draw()

        if self.remaining_points() == 0:
            self.draw_buttons()
            self.resize_confirm_creation_btn.start()
            self.translate_confirm_creation_btn.start()
        else:
            self.resize_inverse_confirm_creation_btn.start()
            self.translate_inverse_confirm_creation_btn.start()
        #     self.str.draw(events, stopb=True, stopval=self.str.getvalue())
        #     self.dex.draw(events, stopb=True, stopval=self.dex.getvalue())
        #     self.con.draw(events, stopb=True, stopval=self.con.getvalue())
        #     self.int.draw(events, stopb=True, stopval=self.int.getvalue())
        #     self.wis.draw(events, stopb=True, stopval=self.wis.getvalue())
        #     self.cha.draw(events, stopb=True, stopval=self.cha.getvalue())
        #     self.anim.start()
        #     self.anim2.start()
        # else:
        #     self.str.draw(events)
        #     self.dex.draw(events)
        #     self.con.draw(events)
        #     self.int.draw(events)
        #     self.wis.draw(events)
        #     self.cha.draw(events)
        #     self.anim_inv.start()
        #     self.anim2_inv.start()

    def draw_points(self):
        self.draw_text(
            f"remaining points : {USABLE_POINTS - self.sum_points()}",
            self.title_font,
            50,
            WHITE,
            20,
            150,
            align="w")

    def draw_sliders(self):
        """Draw sliders"""
        for slider in self.sliders:
            slider.draw()

        self.slider_x.draw()

    def draw_buttons(self):
        """Draw buttons"""
        self.confirm_creation_btn.draw()

    def draw_characteristic(self):
        """Draw characteristic from a character"""
        self.draw_text(
            self.selected_character["name"],
            self.title_font,
            75,
            BLACK,
            WIDTH // 2,
            165,
            align="n")

        image = pg.image.load(self.selected_character["image"]).convert_alpha()
        image = pg.transform.scale(image, (WIDTH_CHARACTER, HEIGHT_CHARACTER))
        self.screen.blit(
            image,
            (WIDTH //
             2 -
             WIDTH_CHARACTER //
             2,
             HEIGHT //
             2 -
             HEIGHT_CHARACTER //
             4))

    def draw_background(self):
        """Draw the background"""
        self.screen.blit(self.image, (0, 0))

    def draw_title(self):
        """Draw title"""
        self.draw_text("Create your character",
                       self.title_font,
                       100,
                       YELLOW_LIGHT,
                       WIDTH // 2,
                       15,
                       align="n")


class Curseur():
    def __init__(
            self,
            title,
            x,
            y,
            width,
            height,
            surface,
            min,
            max,
            step,
            start):
        # font
        self.font = pg.font.Font("./assets/fonts/Enchanted Land.otf", 100)
        self.font_bis = pg.font.Font("./assets/fonts/Enchanted Land.otf", 50)
        self.font_biss = pg.font.Font(
            "./assets/fonts/Roboto-Regular.ttf", 20)

        # definition des tailles
        self.start = start
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.surface = surface
        self.min = min

        # label et point
        # self.titre = self.font_biss.render(title, True, YELLOW_LIGHT)
        # self.output = TextBox(
        #     self.surface,
        #     self.x +
        #     self.width +
        #     20,
        #     self.y -
        #     5,
        #     65,
        #     30,
        #     fontSize=21)

        # selector
        self.slider = Slider(
            self.surface,
            x,
            y,
            width,
            height,
            min=min,
            max=max,
            step=1,
            initial=start)

    def draw(self, stopb=False, stopval=2):
        # self.surface.blit(
        #     self.titre, (self.x + self.width / 2 - 20, self.y - 30))

        # if(stopb and self.slider.getValue() >= stopval):
        #     self.slider.value = stopval


        self.slider.draw()
        # self.output.setText(str(self.min) + " + " +
        #                     str(self.slider.getValue()))
        # self.output.draw()

    def listen(self, events):
        self.slider.listen(events)

    def getvalue_tot(self):
        return self.slider.getValue() + self.min

    def getvalue(self):
        return self.slider.getValue()


# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pg.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text
