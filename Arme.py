from Item import *
from random import randint

class Arme(Item):

    def __init__(self,name="Item_Arme",weight=0.1,quantity=1,price=0,nb_d=3,val_d=5,scope=3):
        super().__init__(name,weight,quantity,price)
        self.nb_d = nb_d
        self.val_d =val_d
        self.scope = scope      




    def attack(self):
        dmg = 0
        for _ in range(self.getNb_d()):
            dmg += randint(1,self.getVal_d())
        
        return dmg
    




    #####SETTER######

    def setNb_d(self,nb_d):
        self.nb_d = nb_d 

    def setVal_d(self,val_d):
        self.val_d = val_d 

    def setScope(self,scope):
        self.scope = scope


    ######GETTER#####

    def getNb_d(self):
        return self.nb_d

    def getVal_d(self):
        return self.val_d

    def getScope(self):
        return self.scope