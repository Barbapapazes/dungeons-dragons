import pygame as pg
from os import path


class Music():
    def __init__(self,win):
        print("creation du module music")
        self.state="menu"
        self.win=win
        self.lib_music=path.join('.',"music")
        self.current_playing=None
        self.run
        
        
    def run(self):
        pg.init()
        pg.mixer.init()
        pg.mixer.music.load(path.join(self.lib_music,self.create_dict()["menu"]))
        pg.mixer.music.play(-1)

    
    def create_dict(self):
        return {
            "menu":"medieval_music.mp3",
            "options":"test.wav"
        }

    def play(self):
        if(self.state):
            pg.mixer.music.play(-1)
        

    def pause(self):
        pg.mixer.music.pause

    def update(self):
        self.state=self.win.state_name
        #si l'etat n'est pas nul et est dans le dict 
        if(self.state and self.state in self.create_dict()):
            #si la musique qui se joue est différente de celle qui va etre jouer 
            if(self.create_dict()[self.state] != self.current_playing):
                pg.mixer.music.load(path.join(self.lib_music,self.create_dict()[self.state]))
                self.current_playing=self.create_dict()[self.state]
                self.play()
                print("OK")

            

