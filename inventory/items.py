"""Item"""


class Item():
    """Item"""

    def __init__(self, name, img, value):
        """Create a item

        Args:
            img (Surface)
            value (Number)
        """
        self.name = name
        self.img = img
        self.value = value
        self.is_moving = False
