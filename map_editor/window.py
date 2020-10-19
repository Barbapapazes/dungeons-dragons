"""Map editor for a user to create a new tiled map"""

import sys
from os import path
import pygame as pg
# pylint: disable=import-error
from settings import WIDTH, HEIGHT, TITLE, FPS, TILESIZE, LIGHTGREY, RED,  BGCOLOR, MAPSIZE
# pylint: disable=import-error
from tileset import Tileset


class Window:
    """Open the main window"""

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.playing = None
        self.dt = None

    def load_data(self):
        """Load data"""
        game_folder = path.dirname('..')
        self.assets_folder = path.join(game_folder, 'assets', 'map_editor')
        self.tileset = Tileset(self.assets_folder, 'town1.png')

    def new(self):
        """Create data for a new loading"""
        self.layer_1 = list()
        self.layer_2 = list()
        self.list_rect = list()
        self.cut_surface = None
        self.map_color = None

    def run(self):
        """Main loop for the program"""
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        """"Catch all events here"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_s and pg.key.get_mods() & pg.KMOD_CTRL:
                    print('ctrl_s')
                    pg.event.wait()
                    self.save_map()
            if event.type == pg.MOUSEBUTTONDOWN:
                self.tileset.get_mouse(event)
                self.mouse_listener()

    def save_map(self):
        """Save a tmx file map"""
        print("layer 1")
        for rect in self.layer_1:
            print(rect)
        print("layer 2")
        for rect in self.layer_2:
            print(rect)
        # with open(path.join(self.assets_folder, 'map_template.tmx'), 'r') as f:
        #     for row in f:
        #         print(row)
        # with open(path.join(self.assets_folder, 'map.tmx'), 'w') as f:
        #     f.write('bonjour')

    def mouse_listener(self):
        """Listen mouse button"""
        mouse_x, mouse_y = self.get_mouse_pos()
        paint_x, paint_y = self.calc_mouse_pos(mouse_x, mouse_y)
        print(paint_x, paint_y)

        if pg.mouse.get_pressed()[0]:
            if self.tileset.get_move_x() < mouse_x <= self.tileset.tileset_width and self.tileset.get_move_y() < mouse_y <= self.tileset.tileset_height:
                self.cut_surface = self.tileset.get_tileset().subsurface(
                    pg.Rect(
                        paint_x * TILESIZE - self.tileset.get_move_x(),
                        paint_y * TILESIZE - self.tileset.get_move_y(),
                        TILESIZE, TILESIZE)).copy()
            elif self.cut_surface != None and self.is_in_map(mouse_x, mouse_y):
                if self.find_in_layer(self.layer_1, paint_x, paint_y):
                    if self.find_in_layer(self.layer_2, paint_x, paint_y):
                        print('can add this tile here')
                    else:
                        print('add to layer 2')
                        self.layer_2.append({'surface': self.cut_surface.copy(), 'rect': pg.Rect(
                            paint_x * TILESIZE, paint_y * TILESIZE, TILESIZE, TILESIZE)})
                else:
                    print('add to layer 1')
                    self.layer_1.append({'surface': self.cut_surface.copy(), 'rect': pg.Rect(
                        paint_x * TILESIZE, paint_y * TILESIZE, TILESIZE, TILESIZE)})
                self.cut_surface = None

        if pg.mouse.get_pressed()[2]:
            if self.is_in_map(mouse_x, mouse_y):
                if self.find_in_layer(self.layer_2, paint_x, paint_y):
                    print('remove in layer 2')
                    self.remove_tile(self.layer_2, paint_x, paint_y)
                elif self.find_in_layer(self.layer_1, paint_x, paint_y):
                    print('remove in layer 1')
                    self.remove_tile(self.layer_1, paint_x, paint_y)

    @staticmethod
    def remove_tile(layer, x, y):
        for tile in layer:
            if tile['rect'].left == x * TILESIZE and tile['rect'].top == y * TILESIZE:
                layer.remove(tile)

    @staticmethod
    def find_in_layer(layer, x, y):
        """Find a tile in a layer using a position

        Args:
            layer (list): contains all tiles
            x (int)
            y (int)

        Returns:
            tile: a tile if found or None
        """
        for tile in layer:
            if tile['rect'].left == x * TILESIZE and tile['rect'].top == y * TILESIZE:
                return tile
        return None

    @staticmethod
    def is_in_map(x, y):
        """Check if the position is in the map editor

        Args:
            x (int): x position
            y (int): y position

        Returns:
            boolean
        """
        return WIDTH - MAPSIZE * TILESIZE < x < WIDTH and 0 < y < MAPSIZE * TILESIZE

    @staticmethod
    def get_mouse_pos():
        """Get the position of the mouse

        Returns:
            (int, int): the x and the y of the mouse
        """
        # """Get the position of the mouse"""
        mouse_x, mouse_y = pg.mouse.get_pos()
        return mouse_x, mouse_y

    @staticmethod
    def calc_mouse_pos(x, y):
        """Calcul the case of the given position

        Args:
            x (int)
            y (int)

        Returns:
            (int, int): the case of the grid
        """
        return x // TILESIZE, y // TILESIZE

    def update(self):
        """ Update portion of the game loop"""
        self.tileset.update()

    def draw_grid(self):
        """Draw a grid to visualize"""
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

        pg.draw.line(self.screen, RED, (WIDTH - MAPSIZE * TILESIZE, 0),
                     (WIDTH - MAPSIZE * TILESIZE, MAPSIZE * TILESIZE), 2)
        pg.draw.line(self.screen, RED, (WIDTH - MAPSIZE * TILESIZE, MAPSIZE * TILESIZE),
                     (WIDTH, MAPSIZE * TILESIZE), 2)

    def draw(self):
        """Draw all elements to the screen"""
        self.screen.fill(BGCOLOR)
        self.draw_grid()

        # faire une classe et l'instancier pour chaque case, on verra ensuite
        # réfléchir à la data à sauvegarder pour pouvoir ensuite la retranscrire dans le fichier tmx
        # dessiner toutes les cases
        # sauvegarder en tmx en réfléchissant bien pour être en mesure de l'ouvrir avec tiled

        self.screen.blit(self.tileset.get_tileset(), (0 + self.tileset.get_move_x(), 0 + self.tileset.get_move_y()))

        for rect in self.layer_1:
            self.screen.blit(rect['surface'], rect['rect'])
        for rect in self.layer_2:
            self.screen.blit(rect['surface'], rect['rect'])

        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    @staticmethod
    def quit():
        """Function to quit everything"""
        pg.quit()
        sys.exit()
