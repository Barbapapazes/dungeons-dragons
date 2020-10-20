"""Map editor for a user to create a new tiled map"""

import sys
from os import path
import pygame as pg
# pylint: disable=import-error
from settings import WIDTH, HEIGHT, TITLE, FPS, TILESIZE, LIGHTGREY, RED,  BGCOLOR, MAPSIZE
# pylint: disable=import-error
from tileset import Tileset
# pylint: disable=import-error
from tile import Tile


class Window():
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
        self.layers = {f"layer_{x}": list() for x in range(10)}
        self.cut_surface = None
        self.map_color = None
        self.selected_layer = 0

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
                if event.key == pg.K_r:
                    self.cut_surface = None
                if event.key in [pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]:
                    self.selected_layer = event.unicode
                    print('layer selected', self.selected_layer)
            if event.type == pg.MOUSEBUTTONDOWN:
                self.tileset.get_mouse(event)
                self.mouse_listener()

    def save_map(self):
        """Save a tmx file map"""
        with open(path.join(self.assets_folder, 'map_template.tmx'), 'r') as r, open(path.join(self.assets_folder, 'map.tmx'), 'w') as f:
            for row in r:
                if row.rstrip('\n') == '_LAYERS':
                    found = False
                    for layer in self.layers:
                        f.write(f' <layer id="1" name="{layer}" width="{MAPSIZE}" height="{MAPSIZE}">\n')
                        f.write('  <data encoding="csv">\n')
                        for row_layer in range(MAPSIZE):
                            for col_layer in range(MAPSIZE):
                                for tile in self.layers[layer]:
                                    if tile.x == col_layer and tile.y == row_layer:
                                        f.write(f'{tile.gid}')
                                        found = True
                                        break
                                if not found:
                                    f.write('0')
                                else:
                                    found = False
                                if row_layer == 19 and col_layer == 19:
                                    f.write('\n')
                                elif col_layer != 19:
                                    f.write(',')
                                else:
                                    f.write(',\n')
                        f.write("  </data>\n")
                        f.write(" </layer>\n")
                else:
                    f.write(row)

    def mouse_listener(self):
        """Listen mouse button"""
        mouse_x, mouse_y = self.get_mouse_pos()
        paint_x, paint_y = self.calc_mouse_pos(mouse_x, mouse_y)
        print(paint_x, paint_y)

        if pg.mouse.get_pressed()[0]:
            if self.tileset.get_move_x() < mouse_x <= self.tileset.tileset_width and self.tileset.get_move_y() < mouse_y <= self.tileset.tileset_height:
                self.cut_surface = {'image': self.tileset.get_tileset().subsurface(
                    pg.Rect(
                        paint_x * TILESIZE - self.tileset.get_move_x(),
                        paint_y * TILESIZE - self.tileset.get_move_y(),
                        TILESIZE, TILESIZE)).copy(), 'pos': (paint_x, paint_y)}
            # pg.event.wait()

        while pg.mouse.get_pressed()[0]:
            pg.event.poll()
            mouse_x, mouse_y = self.get_mouse_pos()
            paint_x, paint_y = self.calc_mouse_pos(mouse_x, mouse_y)
            print(paint_x, paint_y, mouse_x, mouse_y)
            if self.is_in_map(mouse_x, mouse_y):
                if pg.mouse.get_pressed()[0] and self.cut_surface != None:
                    if self.find_in_layer(self.layers[f"layer_{self.selected_layer}"], paint_x, paint_y):
                        print('can\'t add this tile here')
                    else:
                        print(f'add to layer {self.selected_layer}')
                        tile = Tile(
                            self.tileset, self.cut_surface['image'].copy(),
                            self.cut_surface['pos'][0],
                            self.cut_surface['pos'][1])
                        tile.set_pos(paint_x, paint_y)
                        self.layers[f'layer_{self.selected_layer}'].append(tile)
            self.draw()

        while pg.mouse.get_pressed()[2]:
            pg.event.poll()
            mouse_x, mouse_y = self.get_mouse_pos()
            paint_x, paint_y = self.calc_mouse_pos(mouse_x, mouse_y)
            print(paint_x, paint_y, mouse_x, mouse_y)
            if self.is_in_map(mouse_x, mouse_y):
                if pg.mouse.get_pressed()[2]:
                    if self.find_in_layer(self.layers[f"layer_{self.selected_layer}"], paint_x, paint_y):
                        print(f"remove in layer_{self.selected_layer}")
                        self.remove_tile(self.layers[f"layer_{self.selected_layer}"], paint_x, paint_y)
                    # remove all layers on a tile
                    # for index, _ in enumerate(self.layers):
                    #     desc_layer = len(self.layers) - index - 1
                    #     if self.find_in_layer(self.layers[f"layer_{desc_layer}"], paint_x, paint_y):
                    #         print(f"remove in layer_{desc_layer}")
                    #         self.remove_tile(self.layers[f"layer_{desc_layer}"], paint_x, paint_y)
                    #         break
            self.draw()

    @staticmethod
    def remove_tile(layer, x, y):
        """Remove a tile form a layer

        Args:
            layer (list)
            x (int)
            y (int)
        """
        for tile in layer:
            if tile.rect.left == x * TILESIZE and tile.rect.top == y * TILESIZE:
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
            if tile.rect.left == x * TILESIZE and tile.rect.top == y * TILESIZE:
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

        # réfléchir à la data à sauvegarder pour pouvoir ensuite la retranscrire dans le fichier tmx
        # faire la doc absolument
        # mettre en place un système pour les murs
        # mettre en place un système pour ajouter pleins de cases (très complexe)
        # faire un menu accessible à tout moment pour avoir accès au short cuts
        # faire le menu d'accueil aussi

        self.screen.blit(self.tileset.get_tileset(), (0 + self.tileset.get_move_x(), 0 + self.tileset.get_move_y()))

        for layer in self.layers:
            for rect in self.layers[layer]:
                self.screen.blit(rect.image, rect.rect)

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
