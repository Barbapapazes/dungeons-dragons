"""Menu screen"""

import pygame as pg
from window import _Elements
from config.screens import GAME, MENU, NEW_GAME, OPTIONS, LOAD_GAME,OPTIONS_MUSIC
from utils.shortcuts import load_shortcuts
from data.music_data import DATA_MUSIC
from logger import logger


class Options_music(_Elements):
    """Menu screen"""

    def __init__(self):
        self.name = OPTIONS_MUSIC
        self.next = OPTIONS
        super(Options_music, self).__init__(self.name, self.next, 'options', 'background.jpg', self.create_buttons_dict())

        self.startup(0, load_shortcuts())

    def create_buttons_dict(self):
        """Create the dict for all buttons"""
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
        super().events_buttons()
        self.draw()

    def draw(self):
        """Draw content"""
        super().draw_elements("Dungeons and Dragons")

    @staticmethod
    def stop_window():
        """Quit the window using a user event"""
        quit_event = pg.event.Event(pg.USEREVENT, code="_State", name="quit")
        pg.event.post(quit_event)