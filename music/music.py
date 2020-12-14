import pygame as pg
from os import path
from data.music_data import DATA_MUSIC,DATA_SOUND


class Music():
    def __init__(self,win):
        print("creation du module music")
        self.win=win
        self.startup()
        
    
    def startup(self):
        self.current_playing=None
        self.enable=True
        self.state="menu"
        self.lib_music=path.join('.',"music")
        self.init_data()
        

    def create_dict(self):
        return DATA_MUSIC["piste"]

    def play(self):
        pg.mixer.music.play(-1)
    
    def stop(self):
        pg.mixer.music.stop()
     
    def init_data(self):
        DATA_MUSIC["is_enable"]=self.enable
        DATA_MUSIC["current_playing"]=self.current_playing
     
    def load_data(self):
        self.enable=DATA_MUSIC["is_enable"]
        self.current_playing=DATA_MUSIC["current_playing"]

    def update(self):
        self.load_data()
        if(self.enable):
            self.state=self.win.state_name
            #si l'etat n'est pas nul et est dans le dict 
            if(self.state and (self.state in self.create_dict())):
                #si la musique qui se joue est différente de celle qui va etre jouer 
                if(self.create_dict()[self.state] != self.current_playing):
                    pg.mixer.music.load(path.join(self.lib_music,self.create_dict()[self.state]))
                    self.current_playing=self.create_dict()[self.state]
                    self.play()
        else:
            self.stop()

    def update_volume(self):
        #appeler en boucle qui modifie le volume 
        pg.mixer.music.set_volume(DATA_MUSIC["volume"])
        #print("je met a jour le volume", DATA_MUSIC["volume"])
    
    def click_sound(self):
        #appeler en boucle qui va lancer un son 
        if(DATA_SOUND["go"] and DATA_SOUND["is_enable"]):
            print("je joue le click")
            click=pg.mixer.Sound(path.join(self.lib_music,DATA_SOUND["piste"]["click"]))
            click.play()
            DATA_SOUND["go"]=False
        
        






            

