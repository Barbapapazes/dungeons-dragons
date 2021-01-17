"""Create a character screen"""

from datetime import datetime
from os import path

import pygame as pg
from config.buttons import (HEIGHT_BUTTON, HEIGHT_SLIDER, MARGIN_BUTTON,
                            RADIUS_BUTTON, WIDTH_BUTTON, WIDTH_SLIDER)
from config.colors import (BEIGE, BLACK, GREEN_DARK, LIGHTGREY, WHITE,
                           YELLOW_LIGHT)
from config.screens import (CHARACTER_CREATION, CHOOSE_MAP, NEW_GAME,
                            TRANSITION_OUT)
from config.sprites import HEIGHT_CHARACTER, USABLE_POINTS, WIDTH_CHARACTER
from config.window import HEIGHT, WIDTH
from data.game_data import create_game_data
from logger import logger
from pygame_widgets import Button
from sprites.animated import Flames, IdleCharacter
from utils.shortcuts import key_for
from window import _Elements


class CharacterCreation(_Elements):
    """Creation_player"""

    def __init__(self):
        self.name = CHARACTER_CREATION
        self.next = CHOOSE_MAP
        super(CharacterCreation, self).__init__(self.name, self.next, "character_creation", "background.jpg", {})

        # Background image
        # used to avoid a persistence on the screen with the slider
        self.background = pg.Surface((WIDTH, HEIGHT))
        image = pg.image.load(
            path.join(
                self.img_folder,
                'character_creation',
                'background.jpg')).convert()
        self.image = pg.transform.scale(image, (WIDTH, HEIGHT))

        self.remaining_heros_to_create = 0

        self.animated = pg.sprite.Group()
        self.all_sprites = pg.sprite.LayeredUpdates()
        Flames(self, 1 * WIDTH // 20, 4 * HEIGHT // 10, 150)
        Flames(self, 19 * WIDTH // 20, 4 * HEIGHT // 10, 150)

        self.new()

    def startup(self, dt, game_data):
        game_data["loaded"] = False
        game_data["next"] = False
        game_data["game_data"] = create_game_data()
        game_data["minimap"] = {
            "fog": None,
            "cover": None
        }
        self.remaining_heros_to_create = game_data["num_heros"]
        super().startup(dt, game_data)

    def new(self):
        """Create new variables"""
        self.selected = 0
        self.selected_character = self.get_selected_character()
        self.create_confirm_button()
        self.create_animations()
        self.create_sliders()
        self.create_back_button(self.background, self.load_next_state, [NEW_GAME])
        self.idle = IdleCharacter(
            self, 6, self.selected_character["images"],
            0, WIDTH // 2, 7 * HEIGHT / 10, WIDTH_CHARACTER)

    def all_events(self, events):
        for event in events:
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    self.load_next_state(NEW_GAME)

    def create_confirm_button(self):
        """Create buttons from this screen"""
        self.confirm_creation_btn = Button(
            self.background,
            20 * WIDTH // 20 - WIDTH_BUTTON // 2 - 20,
            20 * HEIGHT // 20 - HEIGHT_BUTTON // 2 - 20,
            WIDTH_BUTTON // 2,
            HEIGHT_BUTTON // 2,
            text='continue'.upper(),
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
                "name": "str",
                "max": self.get_selected_character()["characteristics"]["str"]["max"],
                "start": self.get_selected_character()["characteristics"]["str"]["base"],
            },
            "dexterity": {
                "name": "dex",
                "max": self.get_selected_character()["characteristics"]["dex"]["max"],
                "start": self.get_selected_character()["characteristics"]["dex"]["base"],
            },
            "constitution": {
                "name": "con",
                "max": self.get_selected_character()["characteristics"]["con"]["max"],
                "start": self.get_selected_character()["characteristics"]["con"]["base"],
            },
            "intelligence": {
                "name": "int",
                "max": self.get_selected_character()["characteristics"]["int"]["max"],
                "start": self.get_selected_character()["characteristics"]["int"]["base"],
            },
            "wisdom": {
                "name": "wis",
                "max": self.get_selected_character()["characteristics"]["wis"]["max"],
                "start": self.get_selected_character()["characteristics"]["wis"]["base"],
            },
            "charisme": {
                "name": "cha",
                "max": self.get_selected_character()["characteristics"]["cha"]["max"],
                "start": self.get_selected_character()["characteristics"]["cha"]["base"],
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
                    value["name"],
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

    def get_selected_character(self):
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
            value in self.get_selected_character()["characteristics"].items())

    def get_characters(self):
        """Dict with all characters

        Returns:
            dict
        """
        # logger.debug("[sofiane] il faut ajuster les valeurs par default dans les personnages")
        return {
            "soldier": {
                "name": "soldier",
                "images": [pg.image.load(path.join(self.sprites_folder, "soldier", "idle", f"{i}.png")) for i in range(3)],
                "description": "Chevaliers menant une quête, seigneurs conquérants, champions royaux, fantassins d'élite,\n mercenaires endurcis et rois-bandits,tous partagent une maîtrise inégalée des armes\n et des armures ainsi qu'une connaissance approfondie des compétences de combat.\nTous connaissent bien la mort, l'infligeant autant qu'ils lui font face.",
                "characteristics": {
                    "str": {
                        "base": 30,
                        "max": 100},
                    "dex": {
                        "base": 20,
                        "max": 100},
                    "con": {
                        "base": 40,
                        "max": 100},
                    "int": {
                        "base": 15,
                        "max": 100},
                    "wis": {
                        "base": 15,
                        "max": 100},
                    "cha": {
                        "base": 10,
                        "max": 100}}},
            "wizard": {
                "name": "wizard",
                "images": [pg.image.load(path.join(self.sprites_folder, "wizard", "idle", f"{i}.png")) for i in range(3)],
                "description": "Fort de ses pouvoirs en magies, le sorcier a une maîtrise sans précédent de ce pouvoir ! \nGrâce à un entrainement intensif, il est désormais capable de lancer des boules de feu et des sorts de soin, \nlui conféreant un atout sans comparaison sur le champ de battaille !",
                "characteristics": {
                    "str": {
                        "base": 10,
                        "max": 100},
                    "dex": {
                        "base": 20,
                        "max": 100},
                    "con": {
                        "base": 15,
                        "max": 100},
                    "int": {
                        "base": 35,
                        "max": 100},
                    "wis": {
                        "base": 30,
                        "max": 100},
                    "cha": {
                        "base": 20,
                        "max": 100}}},
            "thief": {
                "name": "thief",
                "images": [pg.image.load(path.join(self.sprites_folder, "thief", "idle", f"{i}.png")) for i in range(3)],
                "description": "Possédant une agilité hors norme, il est capable de commencer les combats à tous les coups, \nlui conférant un avantage certain sur le champ de bataille !",
                "characteristics": {
                    "str": {
                        "base": 25,
                        "max": 100},
                    "dex": {
                        "base": 30,
                        "max": 100},
                    "con": {
                        "base": 15,
                        "max": 100},
                    "int": {
                        "base": 20,
                        "max": 100},
                    "wis": {
                        "base": 15,
                        "max": 100},
                    "cha": {
                        "base": 25,
                        "max": 100}}}}

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
        self.animated.update()

    def events_buttons(self):
        """Events for buttons"""
        events = pg.event.get()
        if self.remaining_points() <= 0:
            self.confirm_creation_btn.listen(events)
        self.back_btn.listen(events)

    def events_sliders(self):
        """Events for sliders"""
        events = pg.event.get()
        for slider in self.sliders:
            slider.listen(events)

    def get_events(self, event):
        """Events loop"""
        if event.type == pg.KEYDOWN:
            if key_for(self.game_data["shortcuts"]["character creation"]["class_r"]["keys"], event):
                self.selected += 1
                if self.selected > len(list(self.get_characters().keys())) - 1:
                    self.selected = len(list(self.get_characters().keys())) - 1
                self.selected_character = self.get_selected_character()
                self.idle.set_frames(self.selected_character["images"])
                logger.info("Select the %s in the %s", self.selected_character["name"], CHARACTER_CREATION)
                self.create_sliders()
            if key_for(self.game_data["shortcuts"]["character creation"]["class_l"]["keys"], event):
                self.selected -= 1
                if self.selected < 0:
                    self.selected = 0
                self.selected_character = self.get_selected_character()
                self.idle.set_frames(self.selected_character["images"])
                logger.info("Select the %s in the %s", self.selected_character["name"], CHARACTER_CREATION)
                self.create_sliders()

    def draw(self):
        """Draw all contents"""
        self.draw_background()
        self.draw_title()
        self.draw_characteristic()
        self.draw_sliders()
        self.draw_points()
        self.animated.draw(self.screen)
        self.back_btn.draw()

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
                           7 * HEIGHT // 20 + 20 * index,
                           align="n")

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
        self.draw_text(
            f"Remaining hero to create {self.remaining_heros_to_create}",
            self.text_font,
            24,
            BEIGE,
            19 * WIDTH // 20,
            2 * HEIGHT // 10,
            align="e")

    def draw_title(self):
        """Draw title"""
        self.draw_text("Create your hero",
                       self.title_font,
                       100,
                       YELLOW_LIGHT,
                       WIDTH // 2,
                       15,
                       align="n")

    def create_file_name(self):
        """Create the file name

        Returns:
            str: the file name
        """
        now = datetime.now()
        date = now.strftime("%Y-%b-%d")
        timestamp = datetime.timestamp(now)
        return f"{date}-{int(timestamp)}.json"

    def register_hero(self):
        """Used to save data to the game_data"""
        characteristics = {
            "str": 0,
            "dex": 0,
            "con": 0,
            "int": 0,
            "wis": 0,
            "cha": 0
        }
        for slider in self.sliders:
            characteristics[slider.name] = slider.getValue()

        self.game_data["game_data"]["heros"].append({
            "class": self.get_selected_character()["name"],
            "characteristics": characteristics
        })

    def next_action(self):
        """Pass to the next screen or create a new hero"""
        self.game_data["music"]["sound"]["click"] = True
        logger.info("Save data to game_data")
        # pour chaque perso à faire, il faut le faire, valider, sauvegarder, décrémenter le nombre restant de perso à faire
        # si le nombre est > 0 alors on renvoie sur le même screen pour faire les autres
        # si le nombre est = 0 alors on peut quitter et commencer la parties
        # afficher le nombre de charactère restant

        self.remaining_heros_to_create -= 1
        self.game_data['num_heros'] = self.remaining_heros_to_create

        if self.remaining_heros_to_create > 0:
            self.register_hero()
            # show a saved message (like the shortcuts)
            # then, add a way to add the good number of Player, but always add 3 heros on the tmx map
            self.new()
            logger.info("Create a new hero")
        else:
            self.register_hero()
            self.update_file_name()
            self.next = CHOOSE_MAP
            super().set_state(TRANSITION_OUT)
            logger.info("Start a new game")

    def update_file_name(self):
        if not self.game_data['file_name'] or self.game_data['file_name'] == '.json':
            self.game_data['file_name'] = self.create_file_name()
            logger.info("Update filename to %s", self.game_data["file_name"])
