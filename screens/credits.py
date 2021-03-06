"""Credits screen"""

from config.colors import BEIGE, YELLOW_LIGHT
from config.window import HEIGHT, WIDTH
import pygame as pg
from window import _Elements
from config.screens import BACKGROUND_CREDITS, CREDITS, MENU, NEW_GAME, OPTIONS, LOAD_GAME
from itertools import cycle


class Credits(_Elements):
    """Credit screen"""

    def __init__(self):
        self.name = CREDITS
        self.next = MENU
        super(Credits, self).__init__(self.name, self.next, 'credits', '0001.png', {})

        self.names = ["Alyson", "Sang", "Younes", "Estéban", "Valentin", "Sofiane"]

        self.frames = list()
        for frame in BACKGROUND_CREDITS:
            self.frames.append(pg.transform.scale(frame, (WIDTH, HEIGHT)))

        self.frames = cycle(self.frames)
        self.background = next(self.frames)

        self.frame_time = 80 / 1000
        self.frame_timer = 0

        self.win = pg.Surface((WIDTH, HEIGHT)).convert_alpha()
        self.win.fill((0, 0, 0, 0))
        self.create_back_button(self.win, self.load_next_state, [MENU])

    def all_events(self, events):
        for event in events:
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    self.load_next_state(MENU)

    def run(self, surface, keys, mouse, dt):
        """Run states"""
        self.screen = surface
        self.keys = keys
        self.mouse = mouse
        self.dt = dt
        update_level = self.states_dict[self.state]
        if self.state != 'normal':
            self.draw()
        update_level()

    def normal_run(self):
        """Run the normal state"""
        self.update_background()
        super().events_buttons(back=True)
        self.draw()

    def update_background(self):
        """Used to update the background"""
        self.frame_timer += self.dt
        if self.frame_timer >= self.frame_time:
            self.frame_timer -= self.frame_time
            self.background = next(self.frames)

    def draw(self):
        """Draw content"""
        super().draw_elements("Credits")
        self.draw_text("Groupe 10 - 2020", self.text_font, 72, BEIGE, WIDTH//2, 4 * HEIGHT // 10, align="center")
        for index, name in enumerate(self.names):
            self.draw_text(name, self.text_font, 52, YELLOW_LIGHT, WIDTH//2, HEIGHT//2 + 58 * index, align="center")
        self.back_btn.draw()
        self.screen.blit(self.win, (0, 0))
