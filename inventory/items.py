"""Item"""


class Item:
    """Item"""

    def __init__(self, name, image, price, weight):
        """Create a item

        Args:
            image (Surface)
            price (Number)
            weight (Number)
        """
        self.name = name
        self.image = image
        self.rect = self.image.get_rect()
        self.price = price
        self.weight = weight
        self.is_moving = False

    def __str__(self):
        return self.name

    def __deepcopy__(self, memo):
        return Item(self.name, self.image.copy(), self.price, self.weight)
