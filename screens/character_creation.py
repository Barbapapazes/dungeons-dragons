""""""

from os import path
import pygame as pg
from pygame_widgets import Button, Slider, TextBox, Resize, Translate
from window import _State
from logger import logger
from components.cursor import Cursor
from config.window import WIDTH, HEIGHT
from config.screens import CHARACTER_CREATION, GAME, TRANSITION_OUT
from config.colors import LIGHTGREY, YELLOW_LIGHT, BLACK, BEIGE, GREEN_DARK, WHITE
from config.sprites import WIDTH_CHARACTER, HEIGHT_CHARACTER, USABLE_POINTS
from config.buttons import HEIGHT_BUTTON, MARGIN_BUTTON, RADIUS_BUTTON, HEIGHT_SLIDER, WIDTH_BUTTON, WIDTH_SLIDER


class CharacterCreation(_State):
    """Creation_player"""

    def __init__(self):
        self.name = CHARACTER_CREATION
        super(CharacterCreation, self).__init__(self.name)
        self.next = GAME

        # Background image
        # used to avoid a persistence on the screen with the slider
        self.background = pg.Surface((WIDTH, HEIGHT))
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

    def new(self):
        """Create new variables"""
        self.selected = 0
        self.selected_character = self.get_selected_characters()

    def create_buttons(self):
        """Create buttons from this screen"""
        self.confirm_creation_btn = Button(
            self.background,
            20 * WIDTH // 20 - WIDTH_BUTTON // 2 - 20,
            20 * HEIGHT // 20 - HEIGHT_BUTTON // 2 - 20,
            WIDTH_BUTTON // 2,
            HEIGHT_BUTTON // 2,
            text='start'.upper(),
            fontSize=20,
            margin=MARGIN_BUTTON,
            radius=RADIUS_BUTTON,
            inactiveColour=BEIGE,
            hoverColour=YELLOW_LIGHT,
            pressedColour=GREEN_DARK,
            onClick=self.next_action)

    def create_animations(self):
        """Used to create animations"""
        # too many time for not a real result
        # self.resize_confirm_creation_btn = Resize(
        #     self.confirm_creation_btn, 1, WIDTH_BUTTON // 2, HEIGHT_BUTTON // 2)
        # self.translate_confirm_creation_btn = Translate(
        # self.confirm_creation_btn, 1, 20 * WIDTH // 20 - WIDTH_BUTTON - 20,
        # 20 * HEIGHT // 20 - HEIGHT_BUTTON // 2 - 20)

    def create_sliders_dict(self):
        """Create the dict for all sliders

        Returns:
            dict
        """
        return {
            "strength": {
                "max": self.get_selected_characters()["characteristics"]["str"]["max"],
                "start": self.get_selected_characters()["characteristics"]["str"]["base"],
            },
            "dexterity": {
                "max": self.get_selected_characters()["characteristics"]["dex"]["max"],
                "start": self.get_selected_characters()["characteristics"]["dex"]["base"],
            },
            "constitution": {
                "max": self.get_selected_characters()["characteristics"]["con"]["max"],
                "start": self.get_selected_characters()["characteristics"]["con"]["base"],
            },
            "intelligence": {
                "max": self.get_selected_characters()["characteristics"]["int"]["max"],
                "start": self.get_selected_characters()["characteristics"]["int"]["base"],
            },
            "wisdom": {
                "max": self.get_selected_characters()["characteristics"]["wis"]["max"],
                "start": self.get_selected_characters()["characteristics"]["wis"]["base"],
            },
            "charisme": {
                "max": self.get_selected_characters()["characteristics"]["cha"]["max"],
                "start": self.get_selected_characters()["characteristics"]["cha"]["base"],
            },
        }

    def create_sliders(self):
        """Create sliders"""
        self.sliders = list()
        logger.info("Create all sliders from character creation")
        for index, (key, value) in enumerate(
                self.create_sliders_dict().items()):
            x = 0
            y = 6 * HEIGHT // 10 + (index % 3) * 70
            if index in [0, 1, 2]:
                x = 13 * WIDTH // 20
            else:
                x = 1 * WIDTH // 20
            self.sliders.append(
                self.create_slider(
                    key.upper(),
                    x,
                    y,
                    WIDTH_SLIDER,
                    HEIGHT_SLIDER,
                    self.background,
                    0,
                    value["max"],
                    1,
                    value["start"],
                    self.text_font,
                    self.draw_text, BLACK, LIGHTGREY

                ))

    def get_selected_characters(self):
        """Get the selected character

        Returns:
            dict: the character
        """
        name = list(self.get_characters().keys())[self.selected]
        return self.get_characters()[name]

    def get_default_points(self):
        """Get the default number of points

        Returns:
            int
        """
        return sum(
            value["base"] for key,
            value in self.get_selected_characters()["characteristics"].items())

    def get_characters(self):
        """Dict with all characters

        Returns:
            dict
        """
        return {
            "fighter": {
                "name": "fighter",
                "image": path.join(
                    self.img_folder,
                    "character_creation",
                    "guerrier.png"),
                "description": "Chevaliers menant une quête, seigneurs conquérants, champions royaux, fantassins d'élite, mercenaires endurcis et rois-bandits,\ntous partagent une maîtrise inégalée des armes et des armures ainsi qu'une connaissance approfondie des compétences de combat.\nTous connaissent bien la mort, l'infligeant autant qu'ils lui font face.",
                "characteristics": {
                    "str": {
                        "base": 3,
                        "max": 12},
                    "dex": {
                        "base": 0,
                        "max": 4},
                    "con": {
                        "base": 2,
                        "max": 12},
                    "int": {
                        "base": 2,
                        "max": 12},
                    "wis": {
                        "base": 2,
                        "max": 12},
                    "cha": {
                        "base": 2,
                        "max": 12}}},
            "mage": {
                "name": "mage",
                "image": path.join(
                    self.img_folder,
                    "character_creation",
                    "mage.png"),
                "description": "",
                "characteristics": {
                    "str": {
                        "base": 0,
                        "max": 7},
                    "dex": {
                        "base": 2,
                        "max": 12},
                    "con": {
                        "base": 2,
                        "max": 12},
                    "int": {
                        "base": 2,
                        "max": 12},
                    "wis": {
                        "base": 2,
                        "max": 12},
                    "cha": {
                        "base": 2,
                        "max": 12}}}}

    def sum_points(self):
        """Sum off the added points, remove the offset (start points)


        Returns:
            int
        """
        return sum(x.getValue()
                   for x in self.sliders) - self.get_default_points()

    def remaining_points(self):
        """Get the remaining point

        Returns:
            int
        """
        return USABLE_POINTS - self.sum_points()

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
        self.update()
        self.draw()

    def update(self):
        """Update the content"""
        for slider in self.sliders:
            if self.remaining_points() < 0:
                slider.update(stop_count=True)
            else:
                slider.update()

    def events_buttons(self):
        """Events for buttons"""
        if self.remaining_points() <= 0:
            events = pg.event.get()
            self.confirm_creation_btn.listen(events)

    def events_sliders(self):
        """Events for sliders"""
        events = pg.event.get()
        for slider in self.sliders:
            slider.listen(events)

    def get_events(self, event):
        """Events loop"""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                self.selected += 1
                if self.selected > len(list(self.get_characters().keys())) - 1:
                    self.selected = len(list(self.get_characters().keys())) - 1
                self.selected_character = self.get_selected_characters()
                logger.info("Select the %s in the %s", self.selected_character["name"], CHARACTER_CREATION)
                self.create_sliders()
            if event.key == pg.K_LEFT:
                self.selected -= 1
                if self.selected < 0:
                    self.selected = 0
                self.selected_character = self.get_selected_characters()
                logger.info("Select the %s in the %s", self.selected_character["name"], CHARACTER_CREATION)
                self.create_sliders()

    def draw(self):
        """Draw all contents"""
        self.draw_background()
        self.draw_title()
        self.draw_characteristic()
        self.draw_sliders()
        self.draw_points()

        # # self.name.listen(events)
        # # self.name.draw()

        if self.remaining_points() <= 0:
            self.draw_buttons()

    def draw_points(self):
        """Draw the remaining points"""
        self.draw_text(
            f"Remaining points to attributs : {self.remaining_points()}",
            self.text_font,
            25,
            WHITE,
            1 * WIDTH // 20,
            18 * HEIGHT // 20,
            align="w")

    def draw_sliders(self):
        """Draw sliders"""
        for slider in self.sliders:
            slider.draw()

    def draw_buttons(self):
        """Draw buttons"""
        self.confirm_creation_btn.draw()

    def draw_characteristic(self):
        """Draw characteristic from a character"""
        self.draw_text(
            self.selected_character["name"].upper(),
            self.title_font,
            75,
            BLACK,
            WIDTH // 2,
            2 * HEIGHT // 10,
            align="n")

        for index, text in enumerate(
                self.selected_character["description"].split("\n")):
            self.draw_text(text, self.text_font,
                           15,
                           WHITE,
                           WIDTH // 2,
                           7 * HEIGHT // 20 + 20 * index ,
                           align="n")

        image = pg.image.load(self.selected_character["image"]).convert_alpha()
        image = pg.transform.scale(image, (WIDTH_CHARACTER, HEIGHT_CHARACTER))
        self.screen.blit(
            image,
            (WIDTH //
             2 -
             WIDTH_CHARACTER //
             2,
             14 * HEIGHT //
             20 -
             HEIGHT_CHARACTER //
             2))

    def draw_background(self):
        """Draw the background"""
        self.screen.blit(self.background, (0, 0))
        self.background.blit(self.image, (0, 0))
        self.draw_text(
            "Use your arrow to select another hero",
            self.text_font,
            15,
            WHITE,
            WIDTH // 2,
            HEIGHT - 20,
            align="s")

    def draw_title(self):
        """Draw title"""
        self.draw_text("Create your hero",
                       self.title_font,
                       100,
                       YELLOW_LIGHT,
                       WIDTH // 2,
                       15,
                       align="n")

    def next_action(self):
        """Pass to the next screen"""
        super().set_state(TRANSITION_OUT)
        logger.debug("Save data")

    def output(self):
        # Get text in the textbox
        print("ok")

    @staticmethod
    def create_slider(
            name,
            x,
            y,
            width,
            height,
            surface,
            min,
            max,
            step,
            start,
            font,
            draw_text, color, handle_color):
        """Create a slider

        Args:
            name (str)
            x (int)
            y (int)
            width (int)
            height (int)
            surface (Surface)
            min (int)
            max (int)
            step (int)
            start (int)
            font (str)
            draw_text (func)
            color (tuple)
            handle_color (tuple)

        Returns:
            Cursor
        """
        return Cursor(
            name,
            x,
            y,
            width,
            height,
            surface,
            min,
            max,
            step,
            start,
            font,
            draw_text, color, handle_color)


# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
# def drawText(surface, text, color, rect, font, aa=False, bkg=None):
#     rect = pg.Rect(rect)
#     y = rect.top
#     lineSpacing = -2

#     # get the height of the font
#     fontHeight = font.size("Tg")[1]

#     while text:
#         i = 1

#         # determine if the row of text will be outside our area
#         if y + fontHeight > rect.bottom:
#             break

#         # determine maximum width of line
#         while font.size(text[:i])[0] < rect.width and i < len(text):
#             i += 1

#         # if we've wrapped the text, then adjust the wrap to the last word
#         if i < len(text):
#             i = text.rfind(" ", 0, i) + 1

#         # render the line and blit it to the surface
#         if bkg:
#             image = font.render(text[:i], 1, color, bkg)
#             image.set_colorkey(bkg)
#         else:
#             image = font.render(text[:i], aa, color)

#         surface.blit(image, (rect.left, y))
#         y += fontHeight + lineSpacing

#         # remove the text we just blitted
#         text = text[i:]

#     return text
