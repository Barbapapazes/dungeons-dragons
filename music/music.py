import pygame as pg
from os import path
from data.music_data import DATA_MUSIC,DATA_SOUND
import time 


class Music():
    def __init__(self,win):
        print("creation du module music")
        self.win=win
        self.time_btw_stp=0
        self.startup()
        
    
    def startup(self):
        self.current_playing="enchanted-forest-music.mp3"
        self.enable=True
        self.state="menu"
        self.lib_music=path.join('.',"music")
        print("startup")

        #chargement et lancement de la musique 
        pg.mixer.music.set_volume(DATA_MUSIC["volume"])
        pg.mixer.music.load(path.join(self.lib_music,self.create_dict()[self.state]))
        self.play()
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

                    
                    #chargement et lancement de la musique 
                    pg.mixer.music.load(path.join(self.lib_music,self.create_dict()[self.state]))
                    self.play()

                    #mise a jour de la musique en cours
                    self.current_playing=self.create_dict()[self.state]
                    self.init_data()
        else:
            self.stop()

    def update_volume(self):
        #appeler en boucle qui modifie le volume 
        pg.mixer.music.set_volume(DATA_MUSIC["volume"])
        #print(self.current_playing)
        #print("je met a jour le volume", DATA_MUSIC["volume"])
    
    def click_sound(self):
        #appeler en boucle qui va lancer un son 
        if(DATA_SOUND["click"] and DATA_SOUND["is_enable"]):
            print("je joue le click")
            click=pg.mixer.Sound(path.join(self.lib_music,DATA_SOUND["piste"]["click"]))
            click.play()
            DATA_SOUND["click"]=False

    def step_sound(self):
        if(DATA_SOUND["step"] and DATA_SOUND["is_enable"]):
            if((pg.time.get_ticks()-self.time_btw_stp)>200 or self.time_btw_stp == 0):
                step=pg.mixer.Sound(path.join(self.lib_music,DATA_SOUND["piste"]["step"]))
                pg.mixer.Sound.set_volume(step,0.05)
                step.play()
                self.time_btw_stp=pg.time.get_ticks()
            DATA_SOUND["step"]=False


    def combat(self):
        if(self.state=="game" and DATA_MUSIC["start_combat"]):
            #chargement et lancement de la musique de combat 
            DATA_MUSIC["volume"]=0.05
            pg.mixer.music.load(path.join(self.lib_music,self.create_dict()["combat"]))
            self.play()
            self.current_playing="combat"
            print("musique de combat")
            DATA_MUSIC["start_combat"]=False
        
        if(self.state=="game" and DATA_MUSIC["end_combat"]):
            #chargement et lancement de la musique de base 
            pg.mixer.music.load(path.join(self.lib_music,self.create_dict()[self.state]))
            self.play()
            print("fin de la musique de combat")
            DATA_MUSIC["end_combat"]=False
        
        





            

