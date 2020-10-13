from Inventory import *
import pygame

class Person(pygame.sprite.Sprite):
    
    
    def __init__(self, game, name="Joe",STR=10,DEX=10,CON=10,INT=10,WIS=10,
                                CHA=10,PV=500,PM=50,max_weight=100):

        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()



        self.name = name
        self.STR = STR      #force
        self.DEX = DEX      #dexterite
        self.CON = CON      #
        self.INT = INT      #intelligence
        self.WIS = WIS      #chance
        self.CHA = CHA      #charme
        self.PV = PV        #point de vie
        self.max_PV = PV
        self.PM = PM        #point de mana
        self.max_PM = PM
        self.max_weight = max_weight   # capacite de porter des items dans l'inventaire,  peut etre a init en fonction du poid de la personne (si on implemente) 
        self.itemTransport = 0
        self.items = []         #c'est l'inventaire
        self.x = 0
        self.y = 0
        self.armor = []  # selection getArmor[0] --> Casque    [1]--> Torse    [2]-->Pantalon  [3]-->pied
        self.weapon = 0 #add de l'amrme selectionné
        self.coin = 0
    
    def move(self, dx=0, dy=0):
        if self.game.inventory.display_inventory != True:
            self.x += dx
            self.y += dy
            self.check_collision()

    def IsDead(self):
        "Vérifie si Class Person est morte"
        if self.PV <= 0: print(self.name, "est mort...") 


    def dammage(self,dmg):
        "Dégat subbit"
        self.PV = self.PV - dmg
        self.IsDead()

    
    def heal(self,heal):
        "Redonne des PV"
        self.PV = self.PV + heal
        if self.PV > self.max_PV :
            self.PV = self.max_PV 
