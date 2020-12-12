"""Define test for versus"""

import pygame as pg
from math import sqrt
from config.window import WIDTH, HEIGHT, TILESIZE
from config.colors import RED, YELLOW, BLUE, BLUE_SKY,WHITE,BLACK
from config.versus import TOUCH_HAND, DISTANCE_MOVE, DMG_ANY_WEAPON, NUM_MSG, SIZE_TEXT
from versus.sort import collisionZoneEffect
from utils.tilemap import Camera
from logger import logger



# temp
from temp.enemy import Enemy


class Versus():

    def __init__(self,game):

        self.game = game

        self.BT_attck = pg.Rect((0, HEIGHT - TILESIZE), (TILESIZE, HEIGHT))
        self.BT_sort = pg.Rect((TILESIZE, HEIGHT - TILESIZE), (TILESIZE, HEIGHT))
        self.BT_move = pg.Rect((2*TILESIZE, HEIGHT - TILESIZE), (TILESIZE, HEIGHT))
        
        self.action=None
        self.selectEnemy=None
        self.isVersus = False

        self.countLog = 0
        self.all_msg=[]
        for i in range(NUM_MSG):
            self.all_msg.append('')
        self.nb_msg = NUM_MSG-1
        self.screenLog= pg.Rect((0,0),(5*TILESIZE,(NUM_MSG*SIZE_TEXT)))
        
        
    


    def setCamera(self,camera):
        self.camera=camera

    def setMouse(self,mouse_pos):
        self.mouse_pos = mouse_pos
    
    def setSurface(self,surface):
        self.screen = surface

    def isProgress(self):
        """return True if thre are one action"""
        return  not self.action is None

    def setAction(self,msg):
        self.action= msg

    def begin(self):
        self.isVersus = True
        self.action =None
       
    def end(self):
        self.isVersus = False

    def draw(self, surface):
        pg.draw.rect(surface, RED, self.BT_attck.copy())
        pg.draw.rect(surface,YELLOW,self.BT_move.copy())
        pg.draw.rect(surface,BLUE,self.BT_sort.copy())

        pg.draw.rect(surface,BLACK,self.screenLog.copy())

        for i in range(len(self.all_msg)):
            self.game.draw_text(self.all_msg[i],self.game.text_font,SIZE_TEXT,WHITE,0,i*SIZE_TEXT)


    def isMOV(self):
        return self.BT_move.collidepoint(self.mouse_pos[0], self.mouse_pos[1])

    def isATK(self):
        return self.BT_attck.collidepoint(self.mouse_pos[0], self.mouse_pos[1])

    def isSRT(self):
        return self.BT_sort.collidepoint(self.mouse_pos[0], self.mouse_pos[1])

    def selectedEnemy(self, listEnemy):
        for enemy in listEnemy:
            if enemy.rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1]):
                self.selectEnemy = enemy

    def rangeATK(self,surface,player):
        if player.weapon != None:
            logger.debug(player.weapon.scope)
            pg.draw.circle(surface,RED,player.pos,player.weapon.scope*TILESIZE,2)
        else:
            self.CircleATK= pg.Rect((player.pos.x-(TOUCH_HAND+1)*TILESIZE,player.pos.y -(TOUCH_HAND+1)*TILESIZE),((TOUCH_HAND+1)*TILESIZE*2,(TOUCH_HAND+1)*TILESIZE*2))
            #pg.draw.circle(surface,RED,player.pos,(TOUCH_HAND+1)*TILESIZE,2)
            pg.draw.ellipse(surface,RED,self.CircleATK.copy(),2)
    
    def rangeMOV(self,surface,player):
        pg.draw.circle(surface,YELLOW,player.pos,(DISTANCE_MOVE)*TILESIZE,2)

    def ZoneSort(self,player):
        pg.draw.circle(self.screen,BLUE_SKY,pg.mouse.get_pos(),player.sort.scope * TILESIZE,2)

    def CheckMove(self,player):
        return  (DISTANCE_MOVE*TILESIZE >= abs(sqrt((player.pos.x-self.mouse_pos[0])**2 + (player.pos.y-self.mouse_pos[1])**2)))

    def CheckSort(self,player):
        return (player.sort is not None and (player.MP-player.sort.manaCost >= 0)) 

    def createZone(self,player):
        player.subMP(player.sort.manaCost)
        player.sort.placeSort(self.mouse_pos,self.game)
        self.ENDofAction(player)

    def ENDofAction(self,player):
        player.numberOfAction -= 1
        self.action=None
        self.selectEnemy = None
        self.game.zoneEffect.update()
        collisionZoneEffect(player,self.game)

    def log(self,msg):
        
        for i in range(self.nb_msg):
            self.all_msg[i]=self.all_msg[i+1]

        self.all_msg[self.nb_msg] = msg


       
 
        




    def ONE_action(self,player,screen):

        if(self.action == 'ATK'):
            self.log("Your action is Attack")
            self.action = 'select_enemy'
            self.log("Select your cible")
            
        
        if(self.action=='select_enemy'):
            self.rangeATK(screen,player)
            

        if self.selectEnemy is not None:
            dmg = 0
            self.log(self.selectEnemy.name)
            if player.weapon is not None:  # check if player had a weapon

                if player.weapon.wpn_type == "sword" and player.weapon.scope >= self.distance(
                        player, self.selectEnemy):
                    if player.throwDice(player.STR):
                        dmg = player.weapon.attack()
                    else:
                        self.log("You miss your cible")

                elif player.weapon.wpn_type == "arc":
                    dist = self.distance(player, self.selectEnemy)
                    scope = player.weapon.scope
                    if scope < dist:
                        malus = -((dist - scope) // TILESIZE) * MALUS_ARC
                    else:
                        malus = 0
                    logger.debug(
                        "dist: %i scp: %i  malus: %i", dist, scope, malus)
                    if player.throwDice(player.DEX, malus):
                        dmg = player.weapon.attack()
                    else:
                        self.log("You miss your cible")

                else:
                    self.log("It's too far away ")
            else:
                if self.distance(player, self.selectEnemy)//TILESIZE <= TOUCH_HAND:
                    dmg = DMG_ANY_WEAPON  
                else:
                    self.log("It's too far away ")

            self.selectEnemy.HP -= dmg
            if dmg != 0:
                self.log("The enemy " + str(self.selectEnemy.name) + " lose " + str(dmg) + " HP")
                   
            self.ENDofAction(player)


        if self.action =='Move':
            self.rangeMOV(screen,player)
            
        
        if self.action=='Move_autorised':
            #player pathfinding
            logger.debug("personnage moved wait fct pathfinding")
            self.ENDofAction(player)

        if self.action == 'Select_pos_sort':
            self.ZoneSort(player)
        

    def distance(self, player, enemy):
        return sqrt(
            (enemy.x - player.pos.x)**2 + (enemy.y - player.pos.y)**2)
