class Person():

    
    def __init__(self,nom="Joe",STR=10,DEX=10,CON=10,INT=10,WIS=10,CHA=10,PV=500,PM=50):
        self.nom = nom
        self.STR = STR      #force
        self.DEX = DEX      #dexterité
        self.CON = CON      #
        self.INT = INT      #intelligence
        self.WIS = WIS      #chance
        self.CHA = CHA      #charme
        self.PV = PV        #point de vie
        self.max_PV = PV
        self.PM = PM        #point de mana
        self.max_PM = PM


    
    def dammage(self,dmg):
        self.setPV(self.getPV() - int(dmg))

    def heal(self,heal):
        self.setPV(self.getPV() + int(heal))

    def IsDead(self):
        return self.getPV() <= 0




    ######SETTER########

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
        assert PV <= self.getMax_PV()
        self.PV = PV

    def setPM(self,PM):
        assert PM <= self.getMax_PM()
        self.PM = PM

    def setMax_PV(self,max_PV):
        self.max_PV = max_PV

    def setMax_PM(self,max_PM):
        self.max_PM = max_PM




    #######GETTER########

    def getNom(self):
        return self.nom
    
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

sosso=Person()
akim=Person("akim",5,5,5,5,5,5,100,25)
print(sosso.getPV())
sosso.dammage(6000)
print(sosso.getPV())
print(sosso.IsDead())