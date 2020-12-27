"""Define a spell"""

import pygame as pg
from config.window import TILESIZE


class Spell(pg.sprite.Sprite):
    """Create a spell"""

    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.spells
        super(Spell, self).__init__(self.groups)

        self.game = game
        self.x = x
        self.y = y

        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        pass
        # il faut donner un nombre de tour à un spell et vérifier à chaque tour si on doit l'enlever ou lui retirer un tour. ensuite il faut mettre des dégats dès que un enemy le touche. ajouter aussi un image animée

    def draw(self):
        pass
