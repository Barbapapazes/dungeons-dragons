"""Options screen"""

from os import path
import json
import pygame as pg
from logger import logger
from window import _Elements
from config.window import WIDTH, HEIGHT
from config.colors import BEIGE
from config.screens import MENU, OPTIONS, SHORTCUTS
from data.options import CUSTOM_SETTINGS_FILENAME
from data.music_data import DATA_MUSIC
from config.buttons import HEIGHT_BUTTON, MARGIN_BUTTON, RADIUS_BUTTON, HEIGHT_SLIDER, WIDTH_BUTTON, WIDTH_SLIDER
from config.colors import BLACK, BEIGE, GREEN_DARK, YELLOW_LIGHT,LIGHTGREY
from components.cursor import Cursor


class Options(_Elements):
    """Options screen"""

    def __init__(self):
        self.name = OPTIONS
        self.next = None
        super(Options, self).__init__(self.name, self.next, 'options', "background.jpg", self.create_buttons_dict())

        self.create_back_button(self.background, self.load_next_state, [MENU])

        self.states_dict = self.make_states_dict()
        
        
        

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
            "music":{
                "text": "Musics & Sounds",
                "on_click": self.toggle_sub_state,
                "on_click_params": ['music'],
            }
        }

    
    
    def create_music_buttons_dict(self):
        """Create the dict for screen size buttons"""
        return {
            "song": {
                "text": "Song : "+str(DATA_MUSIC["is_enable"]),
                "on_click": self.status_music,
                "on_click_params": "1",
            },
            "sound": {
                "text": "Sound : "+str(DATA_MUSIC["is_enable"]),
                "on_click": self.status_music,
                "on_click_params": "1",
            },
        }
    
    def status_music(self,none):
        if(DATA_MUSIC["is_enable"]):
            DATA_MUSIC["is_enable"]=False
            DATA_MUSIC["current_playing"]=None
            logger.info("Musique false")
        else:
            DATA_MUSIC["is_enable"]=True
            DATA_MUSIC["current_playing"]=None
            logger.info("Musique true")

        self.btns_dict = self.create_music_buttons_dict()
        self.load_next_state(OPTIONS)
        self.toggle_sub_state("music")
        
    def appliquer(self,etat,sub_state="normal"):
        self.toggle_sub_state("normal")
        self.load_next_state(etat)
        
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
            self.apply=self.create_button(
                    self.image_screen,
                    WIDTH // 2 - WIDTH_BUTTON // 2,
                    600,
                    WIDTH_BUTTON,
                    HEIGHT_BUTTON,
                    "Apply",
                    self.button_font,
                    self.fontsize,
                    MARGIN_BUTTON,
                    RADIUS_BUTTON,
                    BEIGE,
                    YELLOW_LIGHT,
                    GREEN_DARK,
                    self.appliquer,
                    [OPTIONS],
                )
            self.slider=self.create_slider(
                    "Volume",
                    "Volume",
                    WIDTH // 2 - WIDTH_BUTTON // 2,
                    500,
                    400,
                    20,
                    self.image_screen,
                    0,
                    100,
                    1,
                    50,
                    self.button_font,
                    self.draw_text, BLACK, LIGHTGREY
                )
            self.create_back_button(self.image_screen, self.toggle_sub_state, ['normal'])
            self.btns = list()
            self.create_buttons(self.image_screen)

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
        events = pg.event.get()
        self.apply.listen(events)
        self.apply.draw()
        self.slider.listen(events)
        self.slider.draw()
        super().draw_title("Options")
        super().draw_subtitle("Musics & Sounds")
        self.back_btn.draw()
        super().draw_title("Options")
        super().draw_subtitle("Musics & Sounds")
        #self.back_btn.draw()

    def draw(self):
        """Draw content"""
        super().draw_elements("Options", back=True)



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
