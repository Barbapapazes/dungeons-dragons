import pygame as pg
from window import _State


class Menu(_State):
    """
    End Menu Scene.
    """

    def __init__(self):
        super(Menu, self).__init__()
        self.name = 'menu'
        self.next = 'credits'
        self.credit = None

    def startup(self, current_time, game_data):
        """
        Initialize data at scene start.
        """
        self.alpha = 255
        self.game_data = game_data
        self.current_time = current_time
        self.background = pg.Surface((500, 500))
        self.background.fill((0, 255, 0))
        self.state_dict = self.make_state_dict()
        self.state = 'transition in'
        self.transition_surface = pg.Surface((500, 500))
        self.transition_surface.fill((19, 15, 48))
        self.transition_surface.set_alpha(self.alpha)

    def update(self, surface, keys, current_time):
        """
        Update scene.
        """
        update_level = self.state_dict[self.state]
        update_level(keys)
        self.draw_scene(surface)

    def make_state_dict(self):
        """
        Make the dictionary of state methods for the level.
        """
        state_dict = {'transition in': self.transition_in,
                      'transition out': self.transition_out,
                      'normal': self.normal_update}

        return state_dict

    def transition_in(self, *args):
        """
        Transition into scene with a fade.
        """
        self.transition_surface.set_alpha(self.alpha)
        self.alpha -= 35
        if self.alpha <= 0:
            self.alpha = 0
            self.state = 'normal'

    def transition_out(self, *args):
        """
        Transition out of scene with a fade.
        """
        self.transition_surface.set_alpha(self.alpha)
        self.alpha += 35
        if self.alpha >= 255:
            self.done = True

    def normal_update(self, *args):
        pass

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.done = True

    def draw_scene(self, surface):
        """
        Draw all graphics to the window surface.
        """
        surface.blit(self.background, (0, 0))
        surface.blit(self.transition_surface, (0, 0))

        # self.credit.draw(surface)
