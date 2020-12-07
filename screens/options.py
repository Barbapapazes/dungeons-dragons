"""Options screen"""

from window import _Elements
from config.screens import OPTIONS, SHORTCUTS


class Options(_Elements):
    """Options screen"""

    def __init__(self):
        self.name = OPTIONS
        self.next = None
        super(Options, self).__init__(self.name, self.next, 'options', "background.jpg", self.create_buttons_dict())

    def create_buttons_dict(self):
        """Create the dict for all buttons"""
        return {
            "shortcuts": {
                "text": "Shortcuts",
                "on_click": self.load_next_state,
                "on_click_params": [SHORTCUTS],
            },
        }

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
        super().events_buttons()
        self.draw()

    def draw(self):
        """Draw content"""
        super().draw_elements("Options")
