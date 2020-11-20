""""""

import pygame as pg
import string
import pygame_widgets as pw
from window import _State
from config.window import WIDTH, HEIGHT
from config.screens import GAME, MENU, TRANSITION_OUT
import config.colors as couleur


class Character_crea(_State):
    """Creation_player"""

    def __init__(self):
        self.name = MENU
        super(Character_crea, self).__init__(self.name)
        self.next = GAME

        self.background = pg.Surface((WIDTH, HEIGHT))
        self.startup(0, 0)
        #Backgroud image 
        self.image=pg.image.load("./img/Character_crea/background.jpg").convert()
        self.image=pg.transform.scale(self.image,(WIDTH,HEIGHT))

        #titre du jeu 
        self.police=pg.font.Font("./assets/fonts/Enchanted Land.otf",100)
        self.titre=self.police.render("NewGame",True,couleur.YELLOW_LIGHT)

        #textbox
        self.name_setting={
            "command":self.output
        }
        self.name=TextBox(rect=(70,100,150,30),**self.name_setting)
        
        

    def output(self):
        # Get text in the textbox
        print(self.name.getText())

    def startup(self, dt, game_data):
        """Initialize data at scene start."""
        self.game_data = game_data
        self.dt = dt
        self.background.fill((0, 255, 0))
        pg.init()
        pg.display.set_mode((WIDTH,HEIGHT))
        super().setup_transition()

    def run(self, surface, keys, dt):
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
        self.draw()

    def get_events(self, event):
        """Events loop"""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                super().set_state(TRANSITION_OUT)
            if event.key == pg.K_p:
                self.game_data['count'] += 1
                print(self.game_data["count"])

    def draw(self):
        events=pg.event.get()
        self.screen.blit(self.background, (0, 0))
        self.background.blit(self.image,(0,0))
        self.background.blit(self.titre,(375,0))

        self.name.update()
        self.name.draw(self.background)



 
class TextBox(object):
    def __init__(self,rect,**kwargs):
        '''
        Optional kwargs and their defaults:
            "id" : None,
            "command" : None,
                function to execute upon enter key
                Callback for command takes 2 args, id and final (the string in the textbox)
            "active" : True,
                textbox active on opening of window
            "color" : pg.Color("white"),
                background color
            "font_color" : pg.Color("black"),
            "outline_color" : pg.Color("black"),
            "outline_width" : 2,
            "active_color" : pg.Color("blue"),
            "font" : pg.font.Font(None, self.rect.height+4),
            "clear_on_enter" : False,
                remove text upon enter
            "inactive_on_enter" : True
            "blink_speed": 500
                prompt blink time in milliseconds
            "delete_speed": 500
                backspace held clear speed in milliseconds
             
        Values:
            self.rect = pg.Rect(rect)
            self.buffer = []
            self.final = None
            self.rendered = None
            self.render_rect = None
            self.render_area = None
            self.blink = True
            self.blink_timer = 0.0
            self.delete_timer = 0.0
            self.accepted = string.ascii_letters+string.digits+string.punctuation+" "
        '''
        self.rect = pg.Rect(rect)
        self.buffer = []
        self.final = None
        self.rendered = None
        self.render_rect = None
        self.render_area = None
        self.blink = True
        self.blink_timer = 0.0
        self.delete_timer = 0.0
        self.accepted = string.ascii_letters+string.digits+string.punctuation+" "
        self.process_kwargs(kwargs)
 
    def process_kwargs(self,kwargs):
        defaults = {"id" : None,
                    "command" : None,
                    "active" : True,
                    "color" : pg.Color("white"),
                    "font_color" : pg.Color("black"),
                    "outline_color" : pg.Color("black"),
                    "outline_width" : 2,
                    "active_color" : pg.Color("blue"),
                    "font" : pg.font.Font(None, self.rect.height+4),
                    "clear_on_enter" : False,
                    "inactive_on_enter" : True,
                    "blink_speed": 500,
                    "delete_speed": 75}
        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
            else:
                raise KeyError("TextBox accepts no keyword {}.".format(kwarg))
        self.__dict__.update(defaults)
 
    def get_event(self,event, mouse_pos=None):
        ''' Call this on your event loop
         
            for event in pg.event.get():
                TextBox.get_event(event)
        '''
        if event.type == pg.KEYDOWN and self.active:
            if event.key in (pg.K_RETURN,pg.K_KP_ENTER):
                self.execute()
            elif event.key == pg.K_BACKSPACE:
                if self.buffer:
                    self.buffer.pop()
            elif event.unicode in self.accepted:
                self.buffer.append(event.unicode)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if not mouse_pos:
                mouse_pos = pg.mouse.get_pos()
            self.active = self.rect.collidepoint(mouse_pos)
 
    def execute(self):
        if self.command:
            self.command(self.id,self.final)
        self.active = not self.inactive_on_enter
        if self.clear_on_enter:
            self.buffer = []
             
    def switch_blink(self):
        if pg.time.get_ticks()-self.blink_timer > self.blink_speed:
            self.blink = not self.blink
            self.blink_timer = pg.time.get_ticks()
 
    def update(self):
        '''
        Call once on your main game loop
        '''
        new = "".join(self.buffer)
        if new != self.final:
            self.final = new
            self.rendered = self.font.render(self.final, True, self.font_color)
            self.render_rect = self.rendered.get_rect(x=self.rect.x+2,
                                                      centery=self.rect.centery)
            if self.render_rect.width > self.rect.width-6:
                offset = self.render_rect.width-(self.rect.width-6)
                self.render_area = pg.Rect(offset,0,self.rect.width-6,
                                           self.render_rect.height)
            else:
                self.render_area = self.rendered.get_rect(topleft=(0,0))
        self.switch_blink()
        self.handle_held_backspace()
         
    def handle_held_backspace(self):
        if pg.time.get_ticks()-self.delete_timer > self.delete_speed:
            self.delete_timer = pg.time.get_ticks()
            keys = pg.key.get_pressed()
            if keys[pg.K_BACKSPACE]:
                if self.buffer:
                    self.buffer.pop()
 
    def draw(self,surface):
        '''
        Call once on your main game loop
        '''
        outline_color = self.active_color if self.active else self.outline_color
        outline = self.rect.inflate(self.outline_width*2,self.outline_width*2)
        surface.fill(outline_color,outline)
        surface.fill(self.color,self.rect)
        if self.rendered:
            surface.blit(self.rendered,self.render_rect,self.render_area)
        if self.blink and self.active:
            curse = self.render_area.copy()
            curse.topleft = self.render_rect.topleft
            surface.fill(self.font_color,(curse.right+1,curse.y,2,curse.h))
