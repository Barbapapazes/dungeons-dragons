""""""

import pygame as pg
import pygame_widgets as pw
from window import _State
from config.window import WIDTH, HEIGHT
from config.screens import GAME, MENU, TRANSITION_OUT
import config.colors as couleur

WIDHT_CHAR=220
HEIGHT_CHAR=340
NB_POINT=12
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
        self.mage=["< MAGE >","./img/Character_crea/Mage.png","description",("STR",0,7),("DEX",2,12),("CON",2,12),("INT",2,12),("WIS",2,12),("CHA",2,12)]
        self.guerrier=["< FIGHTER >","./img/Character_crea/Guerrier.png","""Chevaliers menant une quête,seigneurs conquérants,champions royaux, fantassins d'élite,mercenaires endurcis et rois-bandits, tous partagent une maîtrise inégalée des armes et des armures ainsi /
        qu'une connaissance approfondie des compétences de combat./
         Tous connaissent bien la mort, l'infligeant autant qu'ils lui font face.""",("STR",3,12),("DEX",0,4),("CON",2,12),("INT",2,12),("WIS",2,12),("CHA",2,12)]
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
                onClick=self.next_action,
                textVAlign="centre",
                textHAlign="centre")

        self.anim=pw.Resize(self.Validation,4,200,30)
        self.anim2=pw.Translate(self.Validation,3,200,200)
    
        #curseur 
        print(self.list_perso[self.index][3][1])
        self.str=Curseur("STR",700,350,200,20,self.background,self.list_perso[self.index][3][1],self.list_perso[self.index][3][2]-self.list_perso[self.index][3][1],1)
        self.dex=Curseur("DEX",700,420,200,20,self.background,self.list_perso[self.index][4][1],self.list_perso[self.index][4][2]-self.list_perso[self.index][4][1],1)
        self.con=Curseur("CON",700,490,200,20,self.background,self.list_perso[self.index][5][1],self.list_perso[self.index][5][2]-self.list_perso[self.index][5][1],1)
        
        self.int=Curseur("INT",20,350,200,20,self.background,self.list_perso[self.index][5][1],self.list_perso[self.index][5][2]-self.list_perso[self.index][5][1],1)
        self.wis=Curseur("WIS",20,420,200,20,self.background,self.list_perso[self.index][5][1],self.list_perso[self.index][5][2]-self.list_perso[self.index][5][1],1)
        self.cha=Curseur("CHA",20,490,200,20,self.background,self.list_perso[self.index][5][1],self.list_perso[self.index][5][2]-self.list_perso[self.index][5][1],1)

        self.list_selector=[self.str,self.dex,self.con,self.int,self.wis,self.cha]

        #nbpoint
        self.nbpts = pw.TextBox(self.background, 100, 100, 100, 100, fontSize=30)

    def start_anim(self):
        self.anim2.start()

    def sommepts(self):
        print(sum(x.getvalue() for x in self.list_selector))
        return sum(x.getvalue() for x in self.list_selector)

    def output(self):
        # Get text in the textbox
        print("ok")

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
        #remise à zero des points a attribuer et slider 
        
        self.actualisation_item()
        


    def actualisation_item(self):
        self.item_text=self.police_bis.render(self.list_perso[self.index][0],True,couleur.BLACK)
        self.perso=pg.image.load(self.list_perso[self.index][1]).convert_alpha()
        self.perso=pg.transform.scale(self.perso,(WIDHT_CHAR,HEIGHT_CHAR))

        self.str=Curseur("STR",700,350,200,20,self.background,self.list_perso[self.index][3][1],self.list_perso[self.index][3][2]-self.list_perso[self.index][3][1],1)
        self.dex=Curseur("DEX",700,420,200,20,self.background,self.list_perso[self.index][4][1],self.list_perso[self.index][4][2]-self.list_perso[self.index][4][1],1)
        self.con=Curseur("CON",700,490,200,20,self.background,self.list_perso[self.index][5][1],self.list_perso[self.index][5][2]-self.list_perso[self.index][5][1],1)
        
        self.int=Curseur("INT",20,350,200,20,self.background,self.list_perso[self.index][5][1],self.list_perso[self.index][5][2]-self.list_perso[self.index][5][1],1)
        self.wis=Curseur("WIS",20,420,200,20,self.background,self.list_perso[self.index][5][1],self.list_perso[self.index][5][2]-self.list_perso[self.index][5][1],1)
        self.cha=Curseur("CHA",20,490,200,20,self.background,self.list_perso[self.index][5][1],self.list_perso[self.index][5][2]-self.list_perso[self.index][5][1],1)

        self.list_selector=[self.str,self.dex,self.con,self.int,self.wis,self.cha]

    def next_action(self):
        super().set_state(TRANSITION_OUT)
        #initialisation du personnage 
        #creation de la sauvegarde 



    def draw(self):
        events=pg.event.get()
        self.screen.blit(self.background, (0, 0))
        self.background.blit(self.image,(0,0))
        self.background.blit(self.titre,(375,0))
        self.background.blit(self.item_text,(425,165))
        drawText(self.background,self.list_perso[self.index][2],couleur.BLACK,(10,225,WIDTH-10,70),self.police_biss)
        self.background.blit(self.perso,(415,300))

        #self.name.listen(events)
        #self.name.draw()

        self.Validation.listen(events)
        self.Validation.draw()
        if(NB_POINT-self.sommepts()<=0):
            self.str.draw(events,stopb=True,stopval=self.str.getvalue())
            self.dex.draw(events,stopb=True,stopval=self.dex.getvalue())
            self.con.draw(events,stopb=True,stopval=self.con.getvalue())
            self.int.draw(events,stopb=True,stopval=self.int.getvalue())
            self.wis.draw(events,stopb=True,stopval=self.wis.getvalue())
            self.cha.draw(events,stopb=True,stopval=self.cha.getvalue())
        else:
            self.str.draw(events)
            self.dex.draw(events)
            self.con.draw(events)
            self.int.draw(events)
            self.wis.draw(events)
            self.cha.draw(events)


        self.nbpts.setText(NB_POINT-self.sommepts())
        self.nbpts.draw()
    
        



        



class Curseur():
    def __init__(self,title,x,y,width,height,surface,min,max,step,ini=0):
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
        self.output = pw.TextBox(self.surface, self.x+self.width+20, self.y-5, 65, 30, fontSize=21)

        

        #selector
        self.slider = pw.Slider(self.surface, x, y, width, height, min=0, max=max, step=step,initial=ini)
       


    def draw(self,events,stopb=False,stopval=2):
        self.surface.blit(self.titre,(self.x+self.width/2-20,self.y-30))
        self.slider.listen(events)
        if(stopb==True and self.slider.getValue()>=stopval):
            self.slider.value=stopval
        self.slider.draw()
        self.output.setText(str(self.min)+" + "+str(self.slider.getValue()))
        self.output.draw()
    
    def getvalue_tot(self):
        return self.slider.getValue()+self.min
    def getvalue(self):
        return self.slider.getValue()
































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
