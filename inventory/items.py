"""Item"""


class Item:
    """Item"""

    def __init__(self, name, image, image_name, price, weight):
        """Create a item

        Args:
            image (Surface)
            price (Number)
            weight (Number)
        """
        self.name = name
        self.image = image
        self.image_name = image_name
        self.rect = self.image.get_rect()
        self.price = price
        self.weight = weight
        self.is_moving = False

    def save(self):
        return {
            "object_type": "item",
            "name": self.name,
            "price": self.price,
            "weight": self.weight,
            "image_name": self.image_name
        }

    def __str__(self):
        return self.name

    def __deepcopy__(self, memo):
        return Item(self.name, self.image.copy(), self.image_name, self.price, self.weight)
