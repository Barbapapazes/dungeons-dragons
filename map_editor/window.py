"""Map editor for a user to create a new tiled map"""

import sys
from os import path
import pygame as pg
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

    @staticmethod
    def quit():
        """Function to quit everything"""
        pg.quit()
        sys.exit()

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
                self.mouse_listener()

    def save_map(self):
        """Save a tmx file map"""
        for rect in self.list_rect:
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
            elif self.cut_surface != None and WIDTH - MAPSIZE * TILESIZE < mouse_x < WIDTH and 0 < mouse_y < MAPSIZE * TILESIZE:
                print('add a new surface')
                self.list_rect.append({'surface': self.cut_surface, 'rect': pg.Rect(
                    paint_x * TILESIZE, paint_y * TILESIZE, TILESIZE, TILESIZE)})
                self.cut_surface = None

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

        # mettre en place la grille de 20*20
        # mettre en place du scroll pour défiler le tileset
        #  mettre en place un clique droit pour dépop la tuile sélect
        # faire une classe et l'instancier pour chaque case, on verra ensuite
        # réfléchir à la data à sauvegarder pour pouvoir ensuite la retranscrire dans le fichier tmx
        # dessiner toutes les cases
        # sauvegarder en tmx en réfléchissant bien pour être en mesure de l'ouvrir avec tiled

        self.screen.blit(self.tileset.get_tileset(), (0 + self.tileset.get_move_x(), 0 + self.tileset.get_move_y()))

        for rect in self.list_rect:
            self.screen.blit(rect['surface'], rect['rect'])

        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
