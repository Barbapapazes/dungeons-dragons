"""Item"""


class Item():
    """Item"""

    def __init__(self, name, img, price, weight):
        """Create a item

        Args:
            img (Surface)
            price (Number)
            weight (Number)
        """
        self.name = name
        self.img = img
        self.price = price
        self.weight = weight
        self.is_moving = False
