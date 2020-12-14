"""Define a enemy"""


from sprites.character import Character


class Enemy(Character):
    def __init__(self, game, x, y, _type, images):
        super(Enemy, self).__init__(game, x, y, _type, images)
        pass
