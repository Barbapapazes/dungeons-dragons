""""""

import pygame as pg
import pygame_widgets as pw
from window import _State
from config.window import WIDTH, HEIGHT
from config.screens import GAME, MENU, TRANSITION_OUT
import config.colors as couleur

WIDHT_CHAR=220
HEIGHT_CHAR=340
class Character_crea(_State):
    """Creation_player"""

    def __init__(self):
        self.name = MENU
        super(Character_crea, self).__init__(self.name)
        self.next = GAME
        self.index=0

        self.background = pg.Surface((WIDTH, HEIGHT))
        self.startup(0, 0)
        #Backgroud image 
        self.image=pg.image.load("./img/Character_crea/background3.jpg").convert()
        self.image=pg.transform.scale(self.image,(WIDTH,HEIGHT))

        #titre du jeu 
        self.police=pg.font.Font("./assets/fonts/Enchanted Land.otf",100)
        self.police_bis=pg.font.Font("./assets/fonts/Enchanted Land.otf",50)
        self.police_biss=pg.font.Font("./assets/fonts/Roboto-Regular.ttf",20)
        self.titre=self.police.render("NewGame",True,couleur.YELLOW_LIGHT)

        #textbox
        self.name= pw.TextBox(self.background, 20, 100, 400, 40, fontSize=50,
                  borderColour=couleur.RED, textColour=(0, 200, 0),
                  onSubmit=self.output, radius=10, borderThickness=4)


        #structure des persos
        self.mage=["< MAGE >","./img/Character_crea/Mage.png","description",("STR",0,10)]
        self.guerrier=["< FIGHTER >","./img/Character_crea/Guerrier.png","""Chevaliers menant une quête,seigneurs conquérants,champions royaux, fantassins d'élite,mercenaires endurcis et rois-bandits, tous partagent une maîtrise inégalée des armes et des armures ainsi /
        qu'une connaissance approfondie des compétences de combat./
         Tous connaissent bien la mort, l'infligeant autant qu'ils lui font face.""",("STR",380,400)]
        self.list_perso=[self.mage,self.guerrier]
    
        #selector 
        self.item_text=self.police_bis.render(self.list_perso[self.index][0],True,couleur.BLACK)
        self.description=self.police_biss.render(self.list_perso[self.index][2],True,couleur.BLACK)

        self.perso=pg.image.load(self.list_perso[self.index][1]).convert_alpha()
        self.perso=pg.transform.scale(self.perso,(WIDHT_CHAR,HEIGHT_CHAR))

        #button et anim 
        self.Validation = pw.Button(
                self.background, 420, 700, 200, 30, text='Start ! ',
                fontSize=20, margin=20,
                inactiveColour=couleur.BEIGE,
                hoverColour=couleur.YELLOW_LIGHT,
                pressedColour=(9, 48, 22), radius=10,
                onClick=self.start_anim,
                textVAlign="centre",
                textHAlign="centre")

        self.anim=pw.Resize(self.Validation,4,200,30)
        self.anim2=pw.Translate(self.Validation,3,200,200)
    


        #curseur 
        self.strong=Curseur("STR",750,350,200,20,self.background,self.list_perso[self.index][3][1],self.list_perso[self.index][3][2]-self.list_perso[self.index][3][1],1)
        self.dex=Curseur("DEX",750,420,200,20,self.background,self.list_perso[self.index][3][1],self.list_perso[self.index][3][2]-self.list_perso[self.index][3][1],1)

    def start_anim(self):
        self.anim2.start()

        

    def output(self):
        # Get text in the textbox
        print("ok")

    def startup(self, dt, game_data):
        """Initialize data at scene start."""
        self.game_data = game_data
        self.dt = dt
        pg.init()
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
                #super().set_state(TRANSITION_OUT)
                self.switch_perso("r")
            if event.key == pg.K_LEFT:
                #super().set_state(TRANSITION_OUT)
                self.switch_perso("l")
            if event.key == pg.K_p:
                self.game_data['count'] += 1
                print(self.game_data["count"])

    
    
    def switch_perso(self,side):
        if(side=="r"):
            if(self.index < len(self.list_perso)-1):
                self.index=self.index+1
            else:
                self.index=0
        if(side=="l"):
            if(self.index > 0):
                self.index=self.index-1
            else:
                self.index=len(self.list_perso)-1
        self.actualisation_item()
        


    def actualisation_item(self):
        self.item_text=self.police_bis.render(self.list_perso[self.index][0],True,couleur.BLACK)
        self.perso=pg.image.load(self.list_perso[self.index][1]).convert_alpha()
        self.perso=pg.transform.scale(self.perso,(WIDHT_CHAR,HEIGHT_CHAR))
        self.strong=Curseur("STR",750,350,200,20,self.background,self.list_perso[self.index][3][0],self.list_perso[self.index][3][1],1)


    def draw(self):
        events=pg.event.get()
        self.screen.blit(self.background, (0, 0))
        self.background.blit(self.image,(0,0))
        self.background.blit(self.titre,(375,0))
        self.background.blit(self.item_text,(425,165))
        drawText(self.background,self.list_perso[self.index][2],couleur.BLACK,(10,225,WIDTH-10,70),self.police_biss)
        self.background.blit(self.perso,(415,300))

        self.name.listen(events)
        self.name.draw()

        self.Validation.listen(events)
        self.Validation.draw()

        self.strong.draw(events)
        self.dex.draw(events)
        



class Curseur():
    def __init__(self,title,x,y,width,height,surface,min,max,step):
        #police
        self.police=pg.font.Font("./assets/fonts/Enchanted Land.otf",100)
        self.police_bis=pg.font.Font("./assets/fonts/Enchanted Land.otf",50)
        self.police_biss=pg.font.Font("./assets/fonts/Roboto-Regular.ttf",20)

        #definition des tailles 
        self.height=height
        self.width=width
        self.x=x
        self.y=y
        self.surface=surface
        self.min=min

        #label et point
        self.titre=self.police_biss.render(title,True,couleur.YELLOW_LIGHT)
        self.output = pw.TextBox(self.surface, self.x+self.width+20, self.y-5, 35, 30, fontSize=21)

        

        #selector
        self.slider = pw.Slider(self.surface, x, y, width, height, min=0, max=max, step=step)
       


    def draw(self,events):
        self.surface.blit(self.titre,(self.x+self.width/2-20,self.y-30))
        self.slider.listen(events)
        self.slider.draw()
        self.output.setText(self.slider.getValue()+self.min)
        self.output.draw()
































# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pg.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] <rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i <len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text
