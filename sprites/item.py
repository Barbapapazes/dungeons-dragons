"""Define a placable item"""

from config.sprites import BOB_RANGE, BOB_SPEED
import pygame as pg
import pytweening as tween


class PlacableItem(pg.sprite.Sprite):
    """Create a Placable item"""

    def __init__(self, game, pos, name, properties, image_name, image):  # ajouter un nom et image (surface)
        self._layer = 1
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.transform.scale(image, (32, 32))
        self.rect = self.image.get_rect()
        self.properties = properties
        self.image_name = image_name
        self.name = name
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        """Update the item"""
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1

    def save(self):
        return {
            "name": self.name,
            "pos": {
                "x": self.pos.x,
                "y": self.pos.y
            },
            "properties": self.properties,
            "image_name": self.image_name,
        }
