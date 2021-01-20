

import pygame as pg
from os import path
from logger import logger


class MusicManager():
    def __init__(self, game, music_loaded):
        self.game = game
        self.time_btw_stp = 0
        self.music_loaded = music_loaded
        self.startup()

    def set_data(self, data):
        logger.debug(data)
        self.music_loaded = data

    def startup(self):
        self.current_playing = "enchanted-forest-music.ogg"
        self.enable = True
        self.state = "menu"

        # chargement et lancement de la musique
        pg.mixer.music.set_volume(self.music_loaded["song"]["volume"])
        pg.mixer.music.load(path.join(self.game.music_folder, self.create_dict()[self.state]))
        self.play()
        self.init_data()

    def create_dict(self):
        return self.music_loaded["song"]["piste"]

    def play(self):
        pg.mixer.music.play(-1)

    def stop(self):
        pg.mixer.music.stop()

    def init_data(self):
        self.music_loaded["song"]["is_enable"] = self.enable
        self.music_loaded["song"]["current_playing"] = self.current_playing

    def load_data(self):
        self.enable = self.music_loaded["song"]["is_enable"]
        self.current_playing = self.music_loaded["song"]["current_playing"]

    def flip_music(self):
        self.load_data()
        if(self.enable):
            self.state = self.game.state_name
            # si l'etat n'est pas nul et est dans le dict
            if(self.state and (self.state in self.create_dict())):

                # si la musique qui se joue est différente de celle qui va etre jouer
                if(self.create_dict()[self.state] != self.current_playing):

                    # chargement et lancement de la musique
                    pg.mixer.music.load(path.join(self.game.music_folder, self.create_dict()[self.state]))
                    self.play()

                    # mise a jour de la musique en cours
                    self.current_playing = self.create_dict()[self.state]
                    self.init_data()
        else:
            self.stop()

    def update_volume(self):
        # appeler en boucle qui modifie le volume
        pg.mixer.music.set_volume(self.music_loaded["song"]["volume"])
        # print(self.current_playing)
        #print("je met a jour le volume", self.music_loaded["song"]["volume"])

    def update(self):
        self.update_volume()
        self.click_sound()
        self.step_sound()
        self.combat()

    def click_sound(self):
        # appeler en boucle qui va lancer un son
        if(self.music_loaded["sound"]["click"] and self.music_loaded["sound"]["is_enable"]):
            click = pg.mixer.Sound(path.join(self.game.music_folder, self.music_loaded["sound"]["piste"]["click"]))
            pg.mixer.Sound.set_volume(click,0.05)
            click.play()
            self.music_loaded["sound"]["click"] = False

    def step_sound(self):
        if(self.music_loaded["sound"]["step"] and self.music_loaded["sound"]["is_enable"]):
            if((pg.time.get_ticks()-self.time_btw_stp) > 200 or self.time_btw_stp == 0):
                step = pg.mixer.Sound(path.join(self.game.music_folder, self.music_loaded["sound"]["piste"]["step"]))
                pg.mixer.Sound.set_volume(step, 0.05)
                step.play()
                self.time_btw_stp = pg.time.get_ticks()
            self.music_loaded["sound"]["step"] = False

    def combat(self):
        if(self.state == "game" and self.music_loaded["song"]["start_combat"]):
            # chargement et lancement de la musique de combat
            self.music_loaded["song"]["volume"] = 0.05
            pg.mixer.music.load(path.join(self.game.music_folder, self.create_dict()["combat"]))
            self.play()
            self.current_playing = "combat"
            self.music_loaded["song"]["start_combat"] = False

        if(self.state == "game" and self.music_loaded["song"]["end_combat"]):
            # chargement et lancement de la musique de base
            pg.mixer.music.load(path.join(self.game.music_folder, self.create_dict()[self.state]))
            self.play()
            self.music_loaded["song"]["end_combat"] = False
