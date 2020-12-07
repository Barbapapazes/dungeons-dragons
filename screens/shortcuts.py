"""Shortcuts screen"""

import json
from os import path
import pygame as pg
from pygame_widgets import Button
from window import _State
from logger import logger
from config.window import WIDTH, HEIGHT
from config.colors import BEIGE, BLACK, WHITE, YELLOW_LIGHT, GREEN_DARK
from config.buttons import HEIGHT_BUTTON, MARGIN_BUTTON, RADIUS_BUTTON, WIDTH_BUTTON
from config.screens import SHORTCUTS
from data.shortcuts import CUSTOM_SHORTCUTS_FILENAME, SHORTCUTS_DEFAULT


class Shortcuts(_State):
    """Shortcuts screen"""

    def __init__(self):
        self.name = SHORTCUTS
        super(Shortcuts, self).__init__(self.name)
        self.next = None

        self.key = None

        image = pg.image.load(
            path.join(
                self.img_folder, 'shortcuts',
                "background.jpg")).convert()
        self.background = pg.transform.scale(image, (WIDTH, HEIGHT))
        self.screen_menu = self.background.copy()
        self.screen_shortcuts = self.background.copy()

        self.fontsize = 35

        self.shortcuts = None

        self.selected_menu = 0
        self.selected_shortcut = 0
        self.is_menu_selected = False
        self.is_shortcut_selected = False

        self.ctrl = None
        self.alt = None
        self.key = 107

        self.saved_file = False
        self.saved_memory = False
        self.reset_memory = False
        self.alpha_actions = 0

    def startup(self, dt, game_data):
        """Initialize data at scene start."""
        self.game_data = game_data
        self.shortcuts = self.game_data["shortcuts"]
        self.menu_keys = list(self.shortcuts.keys())
        self.create_btns()
        self.dt = dt
        super().setup_transition()

    def create_btns(self):
        """Create all buttons"""
        self.create_menu_shortcuts()
        self.create_shortcuts()
        self.create_return_btn()
        self.create_validate_btn()

    def create_validate_btn(self):
        """Create a validation button"""
        self.validate_btn = self.create_button(
            self.background, WIDTH - (WIDTH_BUTTON // 2 + HEIGHT_BUTTON),
            HEIGHT - HEIGHT_BUTTON, WIDTH_BUTTON // 2, HEIGHT_BUTTON // 2, "validate", self.button_font, 30,
            MARGIN_BUTTON, RADIUS_BUTTON, BEIGE, YELLOW_LIGHT, GREEN_DARK, self.set_validate, [])

    def create_return_btn(self):
        """Create th return to previous button"""
        self.back_btn = self.create_button(
            self.background, HEIGHT_BUTTON,
            HEIGHT_BUTTON, WIDTH_BUTTON // 2, HEIGHT_BUTTON // 2, "back", self.button_font,
            30, MARGIN_BUTTON, RADIUS_BUTTON, BEIGE, YELLOW_LIGHT, GREEN_DARK, self.unselect_btn, [])

    def create_shortcuts(self):
        """Create buttons for selected shortcuts"""
        _x = WIDTH // 2 - (WIDTH_BUTTON) // 4
        y_base = 250
        self.shortcuts_btns = list()
        logger.info("Create all buttons from load_game")
        for index, (key, value) in enumerate(self.get_selected_shortcuts()):
            self.shortcuts_btns.append(self.create_button(
                self.screen_shortcuts, _x, y_base + 60 * index, WIDTH_BUTTON // 2, HEIGHT_BUTTON // 2,
                key.upper() + " : " + self.create_text_shortcut(
                    value["keys"][0], value["keys"][1], value["keys"][2]),
                self.button_font, 20, MARGIN_BUTTON, RADIUS_BUTTON, BEIGE,
                YELLOW_LIGHT, GREEN_DARK, self.set_selected_shortcut, [index]))

    def create_menu_shortcuts(self):
        """Create buttons for selected menu"""
        _x = WIDTH // 2 - (WIDTH_BUTTON) // 4
        y_base = 210
        self.menu_btns = list()
        logger.info("Create all buttons from load_game")
        for index, text in enumerate(self.menu_keys):
            self.menu_btns.append(self.create_button(
                self.screen_menu, _x, y_base + 70 * index, WIDTH_BUTTON // 2, HEIGHT_BUTTON,
                text.capitalize(),
                self.button_font, self.fontsize, MARGIN_BUTTON, RADIUS_BUTTON, BEIGE,
                YELLOW_LIGHT, GREEN_DARK, self.set_selected_menu, [index]))

    def set_validate(self):
        """Save the selected  shortcuts in memory"""
        if self.is_shortcut_selected:
            # saved the new shortcut in the program data
            menu = self.menu_keys[self.selected_menu]
            shortcut_keys = list(self.shortcuts[menu].keys())
            shortcut = shortcut_keys[self.selected_shortcut]
            self.shortcuts[menu][shortcut]["keys"] = self.create_shortcut()
            logger.info(
                "Save %s to %s in %s, memory", self.create_shortcut(), shortcut, menu)
            self.create_shortcuts()
            self.saved_memory = True

    def set_selected_menu(self, index):
        """Change the selected menu"""
        if self.is_menu_selected:
            self.is_shortcut_selected = False
            self.selected_shortcut = 0
        else:
            self.is_menu_selected = True
        self.selected_menu = index
        self.screen_shortcuts = self.background.copy()
        self.create_shortcuts()
        logger.info("Menu : %d, Shortcut : %d",
                    self.selected_menu,
                    self.selected_shortcut)

    def set_selected_shortcut(self, index):
        """Change the selected shortcut"""
        self.is_shortcut_selected = True
        self.selected_shortcut = index
        logger.info("Menu : %d, Shortcut : %d",
                    self.selected_menu,
                    self.selected_shortcut)

    def get_selected_shortcuts(self):
        """Get the selected shortcuts

        Returns:
            object
        """
        return self.shortcuts[self.menu_keys[self.selected_menu]].items()

    def run(self, surface, keys, mouse, dt):
        """Run states"""
        self.screen = surface
        self.keys = keys
        self.dt = dt
        update_level = self.states_dict[self.state]
        if self.state != 'normal':
            self.draw()
        update_level()

    def normal_run(self):
        """Run the normal state"""
        self.events_buttons()
        self.draw()

    def events_buttons(self):
        """Used to manage the event for buttons"""
        events = pg.event.get()
        self.back_btn.listen(events)
        if self.is_shortcut_selected:
            self.validate_btn.listen(events)
        if not self.is_menu_selected:
            for btn in self.menu_btns:
                btn.listen(events)
        if self.is_menu_selected:
            for btn in self.shortcuts_btns:
                btn.listen(events)

    def get_events(self, event):
        """Events loop"""
        self.capture_new_shortcuts(event)

        if event.type == pg.KEYUP:
            if event.key == pg.K_s and pg.key.get_mods() & pg.KMOD_ALT:
                self.save_shortcuts()
            elif event.key == pg.K_r and pg.key.get_mods() & pg.KMOD_ALT:
                self.reset_shortcuts()
            elif event.key == pg.K_ESCAPE:
                self.unselect_btn()

    def unselect_btn(self):
        """Unselect the last selected button"""
        if self.is_shortcut_selected:
            self.is_shortcut_selected = False
            logger.info("A shortcut is unselected")
        else:
            self.is_menu_selected = False
            logger.info("A menu is unselected")

    def reset_shortcuts(self):
        """Reset shortcuts in memory"""
        self.game_data["shortcut"] = SHORTCUTS_DEFAULT
        self.shortcuts = SHORTCUTS_DEFAULT
        self.reset_memory = True
        logger.info("Reset shortcuts")

    def capture_new_shortcuts(self, event):
        """Capture key to create a recort form a shortcut

        Args:
            event (Event)
        """
        if event.type == pg.KEYUP:
            if event.key is not pg.K_RETURN and self.is_shortcut_selected:
                mod = pg.key.get_mods()
                if mod & pg.KMOD_CTRL:
                    self.ctrl = not self.ctrl
                    logger.info("CTRL set to %s", self.ctrl)
                elif mod & pg.KMOD_ALT:
                    self.alt = not self.alt
                    logger.info("ALT set to %s", self.alt)
                else:
                    self.key = event.key
                    logger.info("KEY set to %s", self.key)

    def save_shortcuts(self):
        """Save shortcuts to a custom file"""
        self.game_data["shortcut"] = self.shortcuts
        with open(path.join(self.saved_shortcuts, CUSTOM_SHORTCUTS_FILENAME), 'w') as _f:
            _f.write(json.dumps(self.shortcuts))
            logger.info(
                'Save shortcuts to %s',
                path.join(
                    self.saved_shortcuts,
                    CUSTOM_SHORTCUTS_FILENAME))
        self.saved_file = True

    def create_shortcut(self):
        """Create the array for a shortcut

        Returns:
            list
        """
        return [self.ctrl, self.alt, self.key]

    def draw(self):
        """Draw content"""
        if not self.is_menu_selected:
            self.screen.blit(self.screen_menu, (0, 0))
            self.draw_table_btns()
        else:
            self.screen.blit(self.screen_shortcuts, (0, 0))
            self.draw_content_btns()
            self.draw_help()

        self.validate_btn.draw()
        self.back_btn.draw()

        self.draw_title()
        self.draw_subtitle()

        if self.is_shortcut_selected:
            self.draw_to_save()

        self.draw_saved()

    def draw_to_save(self):
        """Draw text explanation to save a shortcut"""
        self.draw_text(
            f"Shortcut à enregistrer : {self.create_text_shortcut(self.ctrl, self.alt, self.key)}",
            self.text_font,
            24,
            YELLOW_LIGHT,
            WIDTH //
            2,
            HEIGHT,
            align="s")

    def draw_title(self):
        """Draw the title"""
        self.draw_text(
            "shortcuts".capitalize(),
            self.title_font,
            150,
            YELLOW_LIGHT,
            WIDTH // 2,
            15,
            align="n")

    def draw_subtitle(self):
        """Draw the subtitle"""
        text = ""
        if self.is_menu_selected:
            text = self.menu_keys[self.selected_menu].upper()
        else:
            text = "Select a menu"
        self.draw_text(
            text,
            self.title_font,
            48,
            YELLOW_LIGHT,
            WIDTH // 2,
            160,
            align="n")

    def draw_content_btns(self):
        """Draw shortcuts buttons"""
        for index, btn in enumerate(self.shortcuts_btns):
            if self.is_shortcut_selected and self.selected_shortcut == index:
                btn.inactiveColour = YELLOW_LIGHT
            else:
                btn.inactiveColour = BEIGE
            btn.draw()

    def draw_table_btns(self):
        """Draw menu buttons"""
        for index, btn in enumerate(self.menu_btns):
            if self.is_menu_selected and self.selected_menu == index:
                btn.inactiveColour = YELLOW_LIGHT
            else:
                btn.inactiveColour = BEIGE
            btn.draw()

    def draw_help(self):
        """Draw help text"""
        for index, (_, value) in enumerate(
                self.shortcuts[self.menu_keys[self.selected_menu]].items()):
            color = BEIGE
            text = ""
            for key_2, value_2 in value.items():
                if key_2 == 'help':
                    text = f"{value_2}"
            self.draw_text(
                text,
                self.text_font,
                16,
                color,
                WIDTH // 2,
                250 + (HEIGHT_BUTTON // 2) + 5 + 60 * index,
                align="n")

    def draw_saved(self):
        """Draw the saved page"""
        if self.saved_file or self.saved_memory or self.reset_memory:
            self.alpha_actions += 8
        if self.alpha_actions >= 255:
            self.saved_file = False
            self.saved_memory = False
            self.reset_memory = False
        if self.alpha_actions > 0 and not self.saved_file and not self.saved_memory and not self.reset_memory:
            self.alpha_actions -= 16
        if self.saved_file or self.alpha_actions > 0 or self.saved_memory or self.reset_memory:
            transition = pg.Surface((WIDTH, HEIGHT))
            transition.fill(BLACK)
            transition.set_alpha(self.alpha_actions)
            self.screen.blit(transition, (0, 0))
            text = ''
            if self.saved_file:
                text = "Saved in a file"
            elif self.saved_memory:
                text = "Saved in memory"
            elif self.reset_memory:
                text = "Reset in memory"
            self.draw_text(text, self.title_font, 150, WHITE,
                           WIDTH // 2, HEIGHT // 2, align="center")

    @staticmethod
    def create_text_shortcut(ctrl, alt, key):
        """Create the string the show the chosen shortcut

        Args:
            ctrl (int)
            alt (int)
            key (int)

        Returns:
            str
        """
        return f"{'ctrl + ' if ctrl else ''}{'alt + ' if alt else ''}{pg.key.name(key) if key else ''}"

    @staticmethod
    def create_button(
            background,
            x,
            y,
            width,
            height,
            text,
            font,
            fontsize,
            margin,
            radius,
            inactive_color,
            hover_color,
            pressed_color,
            on_click,
            on_click_params):
        """Create button

        Args:
            background (Surface)
            x (int)
            y (int)
            width (int)
            height (int)
            text (str)
            font (Font)
            fontsize (int)
            margin (int)
            radius (int)
            inactive_color (tuple)
            hover_color (tuple)
            pressed_color (tuple)
            on_click (fn)
            on_click_params (list)

        Returns:
            Button
        """
        return Button(
            background,
            x,
            y,
            width,
            height,
            text=text,
            font=pg.font.Font(font, fontsize),
            fontSize=fontsize,
            margin=margin,
            radius=radius,
            inactiveColour=inactive_color,
            hoverColour=hover_color,
            pressedColour=pressed_color,
            onClick=on_click,
            onClickParams=on_click_params)
