class Person():

    
    def __init__(self,name="Joe",STR=10,DEX=10,CON=10,INT=10,WIS=10,CHA=10,PV=500,PM=50,capacity=100):
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
        self.capacity = capacity   # capacite de porter des items dans l'inventaire,  peut etre a init en fonction du poid de la personne (si on implemente) 
        self.itemTransport = 0
        self.items = []         #c'est l'inventaire

        #TODO cf la methode d'implementation pour le gadrillage (x,y)?

    
    def dammage(self,dmg):
        "Dégat subbit"
        self.setPV(self.getPV() - int(dmg))

    def heal(self,heal):
        "Redonne des PV"
        self.setPV(self.getPV() + int(heal))

    def IsDead(self):
        "Vérifie si Class Person est morte"
        return self.getPV() <= 0

    def addItems(self,Item):
        "ajout d'un item (arg --> obj type Item)"
        New = True
        for i in self.getItems():
            if i.getName() == Item.getName():
                self.setItemTransport(self.getItemTransport() + Item.getHeight() * Item.getQuantity())
                i.setQuantity(i.getQuantity() + Item.getQuantity())
                New = False
                break
        
        if New:
            self.setItemTransport(self.getItemTransport() + Item.getHeight() * Item.getQuantity())
            self.setItems(Item)
        

    def rmItems(self,Item):
        #TODO
        return 0



    ######SETTER########

    def setName(self,name):
        self.name = name

    def setSTR(self,STR):
        self.STR = STR

    def setDEX(self,DEX):
        self.DEX = DEX

    def setCON(self,CON):
        self.CON = CON

    def setINT(self,INT):
        self.INT = INT

    def setWIS(self,WIS):
        self.WIS = WIS

    def setCHA(self,CHA):
        self.CHA = CHA

    def setPV(self,PV):
        "Si PV depasse son max -> set PV a son max_PV"
        if(PV > self.getMax_PV()):
            self.PV = self.getMax_PV()
        else:
            self.PV = PV

    def setPM(self,PM):
        "si PM depasse son max -> set PM a son max_PM"
        if (PM > self.getMax_PM()):
            self.PM = self.getMax_PM()
        self.PM = PM

    def setMax_PV(self,max_PV):
        self.max_PV = max_PV

    def setMax_PM(self,max_PM):
        self.max_PM = max_PM

    def setCapacity(self,capacity):
        self.capacity = capacity

    def setItemTransport(self,ItemHeight):
        assert self.getItemTransport() + int(ItemHeight) <= self.getCapacity()
        self.itemTransport = ItemHeight

    def setItems(self,items):
        self.items.append(items)

    #######GETTER########

    def getName(self):
        return self.name
    
    def getSTR(self):
        return self.STR

    def getDEX(self):
        return self.DEX

    def getCON(self):
        return self.CON

    def getINT(self):
        return self.INT

    def getWIS(self):
        return self.WIS

    def getCHA(self):
        return self.CHA

    def getPV(self):
        return self.PV
    
    def getMax_PV(self):
        return self.max_PV

    def getPM(self):
        return self.PM

    def getMax_PM(self):
        return self.max_PM

    def getCapacity(self):
        return self.capacity

    def getItemTransport(self):
        return self.itemTransport

    def getItems(self):
        return self.items