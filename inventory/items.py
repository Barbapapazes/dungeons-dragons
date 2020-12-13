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
        self.price = price
        self.weight = weight
        self.is_moving = False

    def __str__(self):
        return self.name
