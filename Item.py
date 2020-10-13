class Item():
    
    def __init__(self,name="Item",weight=0.1,quantity=1,price=0):
        self.name = name
        self.weight = weight
        self.quantity = quantity
        self.price = price

    


 ####SETTER######

    def setName(self,name):
        self.name = name

    def setWeight(self,weight):
        self.weight = weight

    def setQuantity(self,quantity):
        self.quantity = quantity

    def setPrice(self,price):
        self.price = price


 ####GETTER######

    def getName(self):
        return self.name

    def getWeight(self):
        return self.weight

    def getQuantity(self):
        return self.quantity

    def getPrice(self):
        return self.price