"""Map editor for a user to create a new tiled map"""

import sys
from os import path
import pygame as pg
from settings import WIDTH, HEIGHT, TITLE, FPS, TILESIZE, LIGHTGREY, BGCOLOR
from tileset import Tileset


class Window:
    """Open the main window"""

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        # pg.key.set_repeat(500, 100)
        self.load_data()
        self.playing = None
        self.dt = None

    def load_data(self):
        """Load data"""
        map_editor_folder = path.dirname(__file__)
        game_folder = path.dirname('..')
        assets_folder = path.join(game_folder, 'assets', 'map_editor')
        self.tileset = Tileset(assets_folder, 'town1.png')

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
            if event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_listener()

    def mouse_listener(self):
        """Listen mouse button"""
        mouse_x, mouse_y = self.get_mouse_pos()
        paint_x, paint_y = self.calc_mouse_pos(mouse_x, mouse_y)
        print(paint_x, paint_y)

        if pg.mouse.get_pressed()[0] == True:
            if self.tileset.get_move_x() < mouse_x <= self.tileset.tileset_width and self.tileset.get_move_y() < mouse_y <= self.tileset.tileset_height:
                self.cut_surface = self.tileset.get_tileset().subsurface(
                    pg.Rect(
                        paint_x * TILESIZE - self.tileset.get_move_x(),
                        paint_y * TILESIZE - self.tileset.get_move_y(),
                        TILESIZE, TILESIZE)).copy()
            elif self.cut_surface != None:
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

    def draw(self):
        """Draw all elements to the screen"""
        self.screen.fill(BGCOLOR)
        self.draw_grid()

        # faire une grande surface avec plus de couleur et sélectionner dedans à chaque clique
        # passer ensuite à une image (utiliser que quelques cases d'une image de tuiles)
        # faire une classe et l'instancier pour chaque case
        # dessiner toutes les cases
        # sauvegarder en tmx en réfléchissant bien pour être en mesure de l'ouvrir avec tiled
        # self.map_color = pg.Surface((3 * TILESIZE, 3 * TILESIZE))
        # self.map_color.fill((0, 255, 0))
        # map_color_rect = self.map_color.get_rect()
        # map_color_rect.top = 0
        # map_color_rect.left = 0

        # self.red = pg.Surface((TILESIZE, TILESIZE))
        # self.red.fill((255, 0, 0))
        # red_rect = self.red.get_rect()
        # red_rect.top = 0
        # red_rect.left = 0
        # self.map_color.blit(self.red, red_rect)
        # self.blue = pg.Surface((TILESIZE, TILESIZE))
        # self.blue.fill((0, 0, 255))
        # blue_rect = self.blue.get_rect()
        # blue_rect.top = TILESIZE
        # blue_rect.left = TILESIZE
        # self.map_color.blit(self.blue, blue_rect)
        # self.screen.blit(self.map_color, map_color_rect)

        self.screen.blit(self.tileset.get_tileset(), (0 + self.tileset.get_move_x(), 0 + self.tileset.get_move_y()))

        # print(self.list_rect)
        for rect in self.list_rect:
            # print(rect)
            self.screen.blit(rect['surface'], rect['rect'])

        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
