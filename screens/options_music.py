"""Menu screen"""

from data.music_data import CUSTOM_MUSIC_FILENAME
import pygame as pg
from os import path
import json
from config.buttons import HEIGHT_SLIDER, WIDTH_SLIDER
from config.colors import BLACK, LIGHTGREY
from config.screens import OPTIONS, OPTIONS_MUSIC
from config.window import HEIGHT
from logger import logger
from window import _Elements


class Options_music(_Elements):
    """Menu screen"""

    def __init__(self):
        self.name = OPTIONS_MUSIC
        self.next = None
        super(Options_music, self).__init__(self.name, self.next,
                                            'options', 'background.jpg', {})

    def startup(self, dt, game_data):
        super().startup(dt, game_data)
        self.btns_dict = self.create_buttons_dict()
        self.create_buttons(self.background)
        self.create_back_button(self.background, self.load_next_state, [OPTIONS])
        self.create_sliders()

    def get_events(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_s and pg.key.get_mods() & pg.KMOD_ALT:
                self.save_settings()

    def save_settings(self):
        """Save settings from this screen"""
        with open(path.join(self.saved_music, CUSTOM_MUSIC_FILENAME), 'w') as _f:
            _f.write(json.dumps(self.game_data["music"]))
            logger.info(
                'Save music to %s',
                path.join(
                    self.saved_music,
                    CUSTOM_MUSIC_FILENAME))
        self.saved_file = True

    def create_buttons_dict(self):
        """Create the dict for all buttons"""
        return {
            "song": {
                "text": "Song: " + ('Off' if self.game_data["music"]["song"]["is_enable"] else 'On'),
                "on_click": self.status_music,
                "on_click_params": [],
            },
            "sound": {
                "text": "Sound: " + ('Off' if self.game_data["music"]["sound"]["is_enable"] else 'On'),
                "on_click": self.status_sound,
                "on_click_params": [],
            },
        }

    def create_sliders_dict(self):
        """Create the dict for all sliders

        Returns:
            dict
        """
        return {
            "Music": {
                "name": "music",
                "max": 100,
                "start": self.game_data["music"]["song"]["volume"],
            },

        }

    def create_sliders(self):
        """Create sliders"""
        self.sliders = list()
        logger.info("Create all sliders from option music")
        for index, (key, value) in enumerate(
                self.create_sliders_dict().items()):
            y = 6 * HEIGHT // 10 + (index % 3) * 70
            x = 420
            self.sliders.append(
                self.create_slider(
                    key.upper(),
                    "None",
                    x,
                    y,
                    WIDTH_SLIDER,
                    HEIGHT_SLIDER,
                    self.background,
                    0,
                    1,
                    0.02,
                    value["start"],
                    self.text_font,
                    self.draw_text, BLACK, LIGHTGREY

                ))

    def status_music(self, *args):
        self.game_data["music"]["song"]["is_enable"] = not self.game_data["music"]["song"]["is_enable"]
        self.game_data["music"]["song"]["current_playing"] = None
        pg.event.wait()
        self.game_data["music"]["sound"]["click"] = True
        logger.info("Toggle music status")
        self.btns_dict = self.create_buttons_dict()
        self.create_buttons(self.background)
        self.load_next_state(OPTIONS_MUSIC)

    def status_sound(self, *args):
        self.game_data["music"]["sound"]["is_enable"] = not self.game_data["music"]["sound"]["is_enable"]
        pg.event.wait()
        self.game_data["music"]["sound"]["click"] = True
        logger.info("Toggle sound status")
        self.btns_dict = self.create_buttons_dict()
        self.create_buttons(self.background)
        self.load_next_state(OPTIONS_MUSIC)

    def run(self, surface, keys, mouse, dt):
        """Run states"""
        self.screen = surface
        self.keys = keys
        self.mouse = mouse
        self.dt = dt
        update_level = self.states_dict[self.state]
        if self.state != 'normal':
            self.draw()
            self.back_btn.draw()
        update_level()

    def normal_run(self):
        """Run the normal state"""
        super().events_buttons(back=True)
        self.events_sliders()
        self.update()
        self.draw()

    def update(self):
        """Update the content"""
        pass

    def draw_sliders(self):
        """Draw sliders"""
        for slider in self.sliders:
            slider.draw_without_text()

    def events_sliders(self):
        """Events for sliders"""
        events = pg.event.get()
        for slider in self.sliders:
            slider.listen(events)
        self.game_data["music"]["song"]["volume"] = self.sliders[0].getValue()

    def draw(self):
        """Draw content"""
        super().draw_elements("Options")
        super().draw_subtitle("Music & Sounds")
        self.draw_sliders()

    @staticmethod
    def actualize():
        """Actualize the settings"""
        actu_event = pg.event.Event(pg.USEREVENT, code="_State", name="music")
        pg.event.post(actu_event)
