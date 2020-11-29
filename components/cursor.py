"""Extend the base slider"""
from config.colors import WHITE, YELLOW_LIGHT
from pygame_widgets import Slider


class Cursor(Slider):
    def __init__(
            self,
            name,
            x,
            y,
            width,
            height,
            surface,
            min,
            max,
            step,
            start, font, draw_text):
        super(
            Cursor,
            self).__init__(
            surface,
            x,
            y,
            width,
            height,
            min=min,
            max=max,
            step=step,
            initial=start)

        self.name = name
        self.screen = surface
        self.start = start
        self.x = x
        self.y = y
        self.font= font
        self.width = width
        self.height = height
        self.draw_text = draw_text
        self.previous = start
        # self.titre = self.font_biss.render(title, True, YELLOW_LIGHT)
        # self.output = TextBox(
        #     self.surface,
        #     self.x +
        #     self.width +
        #     20,
        #     self.y -
        #     5,
        #     65,
        #     30,
        #     fontSize=21)

        # selector
        # self.slider = Slider(
        #     self.surface,
        #     x,
        #     y,
        #     width,
        #     height,
        #     min=min,
        #     max=max,
        #     step=1,
        #     initial=start)

    def draw(self):
        # if not stopval:
        #     stopval = self.start
        # self.surface.blit(
        #     self.titre, (self.x + self.width / 2 - 20, self.y - 30))

        value = super().getValue() - self.start

        self.draw_text(f"base: {self.start}, add : {value}", self.font, 15, WHITE, self.x + self.width * 1.1, self.y + self.height // 2, align="w")
        self.draw_text(self.name.upper(), self.font, 20, YELLOW_LIGHT, self.x, self.y - 3 * self.height // 4, align="w")

        super().draw()
        # self.output.setText(str(self.min) + " + " +
        #                     str(self.slider.getValue()))
        # self.output.draw()

    def update(self, stop_count=False):
        self.check_min_value()
        if stop_count:
            super().setValue(self.previous)

    def check_min_value(self):
        """Check if the value is under the start value"""
        value = super().getValue()
        if value < self.start:
            value = self.start
            super().setValue(self.start)

    def listen(self, events):
        self.previous = super().getValue()
        super().listen(events)

    def getvalue_tot(self):
        return super().getValue() + self.min
