import pygame as pg
from window import _State


class Credits(_State):
    """
    End Credits Scene.
    """

    def __init__(self):
        super(Credits, self).__init__()
        self.name = 'credits'
        self.credit = None
        self.next = 'menu'
        self.startup(0, 0)

    def startup(self, current_time, game_data):
        """
        Initialize data at scene start. 
        """
        self.game_data = game_data
        self.current_time = current_time
        self.background = pg.Surface((500, 500))
        self.background.fill((255, 0, 0))

    def update(self, surface, keys, current_time):
        """
        Update scene.
        """
        self.draw_scene(surface)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.done = True

    def draw_scene(self, surface):
        """
        Draw all graphics to the window surface.
        """
        surface.blit(self.background, (0, 0))
        # self.credit.draw(surface)
