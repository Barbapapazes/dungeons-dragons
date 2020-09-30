class Item():
    
    def __init__(self,name="Item",height=0.1,quantity=1,price=0):
        self.name = name
        self.height = height
        self.quantity = quantity
        self.price = price

    


    ####SETTER######

    def setName(self,name):
        self.name = name

    def setHeight(self,height):
        self.height = height

    def setQuantity(self,quantity):
        self.quantity = quantity

    def setPrice(self,price):
        self.price = price


    ####GETTER######

    def getName(self):
        return self.name

    def getHeight(self):
        return self.height

    def getQuantity(self):
        return self.quantity

    def getPrice(self):
        return self.price