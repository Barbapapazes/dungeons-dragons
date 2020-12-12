"""Options screen"""

from os import path
import json
from sprites.animated import Chandelier
import pygame as pg
from logger import logger
from window import _Elements
from config.window import WIDTH, HEIGHT
from config.colors import BEIGE
from config.screens import MENU, OPTIONS, SHORTCUTS ,OPTIONS_MUSIC
from data.options import CUSTOM_SETTINGS_FILENAME
from data.music_data import DATA_MUSIC


class Options(_Elements):
    """Options screen"""

    def __init__(self):
        self.name = OPTIONS
        self.next = None
        super(Options, self).__init__(self.name, self.next, 'options', "background.jpg", self.create_buttons_dict())

        self.create_back_button(self.background, self.load_next_state, [MENU])

        self.animated = pg.sprite.Group()
        Chandelier(self, WIDTH // 4, 0, 200)
        Chandelier(self, 3 * WIDTH // 4, 0, 200)

        self.states_dict = self.make_states_dict()
        
        
        

    def all_events(self, events):
        for event in events:
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    self.load_next_state(MENU)

    def create_buttons_dict(self):
        """Create the dict for all buttons"""
        return {
            "shortcuts": {
                "text": "Shortcuts",
                "on_click": self.load_next_state,
                "on_click_params": [SHORTCUTS],
            },
            "screen_size": {
                "text": "Screen resolutions",
                "on_click": self.toggle_sub_state,
                "on_click_params": ['screen'],
            },
            "Music & Sounds": {
                "text": "Musics & Sounds",
                "on_click": self.load_next_state,
                "on_click_params": [OPTIONS_MUSIC],
            },
        }

    def create_settings_buttons_dict(self):
        """Create the dict for screen size buttons"""
        return {
            "small": {
                "text": "small",
                "on_click": self.save_settings,
                "on_click_params": [1024, 768],
            },
            "medium": {
                "text": "medium",
                "on_click": self.save_settings,
                "on_click_params": [1280, 720],
            },
            "large": {
                "text": "large",
                "on_click": self.save_settings,
                "on_click_params": [1920, 1080],
            },
        }
    
    def create_music_buttons_dict(self):
        """Create the dict for screen size buttons"""
        return {
            "power": {
                "text": "on/off",
                "on_click": self.status_music,
                "on_click_params": "1",
            },
            "Apply":{
                "text": "Apply",
                "on_click": self.appliquer ,
                "on_click_params": [OPTIONS],
            },
        }
    
    def status_music(self,none):
        if(DATA_MUSIC["is_enable"]):
            DATA_MUSIC["is_enable"]=False
        else:
            DATA_MUSIC["is_enable"]=True

    def appliquer(self,etat):
        self.toggle_sub_state("normal")
        self.load_next_state(etat)

    def toggle_sub_state(self, state):
        super().toggle_sub_state(state)
        pg.event.wait()
        if state == 'screen':
            self.image_screen = self.image.copy()
            self.btns_dict = self.create_settings_buttons_dict()
            self.create_back_button(self.image_screen, self.toggle_sub_state, ['normal'])
            self.btns = list()
            self.create_buttons(self.image_screen)
        elif state =="music":
            self.image_screen = self.image.copy()
            self.btns_dict = self.create_music_buttons_dict()
            self.create_back_button(self.image_screen, self.toggle_sub_state, ['normal'])
            self.btns = list()
            self.create_buttons(self.image_screen)
        else:
            self.btns_dict = self.create_buttons_dict()
            self.create_buttons(self.background)
            self.create_back_button(self.background, self.load_next_state, [MENU])

    def make_states_dict(self):
        """Make the dictionnary of state methods for the level

        Returns:
            [object: define all the possible states for a screen
        """
        previous_dict = super().make_states_dict().copy()
        add_dict = {"screen": self.screen_run}
        add_dict_music={"music":self.music_run}
        return previous_dict | add_dict | add_dict_music

    def save_settings(self, w, h):
        file_name = path.join(self.saved_settings, CUSTOM_SETTINGS_FILENAME)
        to_save = {
            "width": w,
            "height": h
        }
        with open(file_name, 'w') as _f:
            _f.write(json.dumps(to_save))
            logger.info("Saved %s in %s", CUSTOM_SETTINGS_FILENAME,  path.abspath(file_name))

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
        super().events_buttons(back=True)
        self.draw()

    def screen_run(self):
        """Run the screen state"""
        self.screen.blit(self.image_screen, (0, 0))
        super().events_buttons(back=True)
        super().draw_title("Options")
        super().draw_subtitle("Screen resolutions")
        self.back_btn.draw()
        self.draw_text(
            "Restart to enable the new window size",
            self.text_font,
            36,
            BEIGE,
            WIDTH // 2,
            HEIGHT,
            align="s")
    
    def music_run(self):
        """Run the screen state"""
        self.screen.blit(self.image_screen, (0, 0))
        super().events_buttons(back=True)
        super().draw_title("Options")
        super().draw_subtitle("Musics & Sounds")
        #self.back_btn.draw()

    def draw(self):
        """Draw content"""
        super().draw_elements("Options", back=True)
        self.animated.draw(self.screen)



    @staticmethod
    def create_slider(
            title,
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
            title (str)
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
            title,
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
