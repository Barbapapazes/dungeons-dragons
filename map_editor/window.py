"""Map editor for a user to create a new tiled map"""

import sys
import os
from os import path
import pygame as pg
from datetime import datetime, date
import pytmx
# pylint: disable=import-error
from settings import WIDTH, HEIGHT, TITLE, FPS, TILESIZE, LIGHTGREY, RED,  BGCOLOR, MAPSIZE, WHITE, BLACK, YELLOW
# pylint: disable=import-error
from tileset import Tileset
# pylint: disable=import-error
from tile import Tile
# pylint: disable=import-error
from tools import Paint, Rubber


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
        self.layers = {f"layer_{x}": list() for x in range(10)}
        self.bounds = list()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        """Load data"""
        game_folder = path.dirname('..')
        self.assets_folder = path.join(game_folder, 'assets')
        self.map_editor_folder = path.join(self.assets_folder, 'map_editor')
        self.fonts_folder = path.join(self.assets_folder, 'fonts')
        self.saved_maps = path.join(self.assets_folder, 'saved_maps')
        self.tileset = Tileset(self.map_editor_folder, 'town1.png')
        self.title_font = path.join(self.fonts_folder, 'Roboto-Regular.ttf')
        self.text_font = path.join(self.fonts_folder, 'Roboto-Regular.ttf')

    def new(self):
        """Create data for a new loading"""
        self.cut_surface = None
        self.map_color = None
        self.selected_layer = 0
        self.tool_images = {'paint_pot': pg.Surface((TILESIZE, TILESIZE)), 'rubber': pg.Surface((TILESIZE, TILESIZE))}
        self.tools = pg.sprite.Group()

        self.paint_pot = Paint(self, 9, 0, 'paint_pot')
        self.rubber = Rubber(self, 10, 0, 'rubber')

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
                if pg.key.get_mods() & pg.KMOD_ALT:
                    print('alt click')
                    self.bound_drawer()
                else:
                    self.tileset.get_mouse(event)
                    self.mouse_listener()

    def save_map(self):
        """Save a tmx file map"""
        with open(path.join(self.map_editor_folder, 'map_template.tmx'), 'r') as r, open(path.join(self.saved_maps, self.selected_map), 'w') as f:
            for row in r:
                if row.rstrip('\n') == '_LAYERS':
                    found = False
                    for index, layer in enumerate(self.layers):
                        f.write(f' <layer id="{index + 1}" name="{layer}" width="{MAPSIZE}" height="{MAPSIZE}">\n')
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

    def bound_drawer(self):
        # reset the relative pos
        pg.mouse.get_rel()
        left, top = self.get_mouse_pos()
        move_x = 0
        move_y = 0
        first_time = True
        while pg.mouse.get_pressed()[0]:
            pg.event.poll()

            mouse_x, mouse_y = self.get_mouse_pos()
            paint_x, paint_y = pg.mouse.get_rel()

            if self.is_in_map(mouse_x, mouse_y):
                if not first_time:
                    self.bounds = self.bounds[0:-1]
                move_x += paint_x
                move_y += paint_y

                tmp_rect = pg.Rect(left, top, move_x, move_y)
                self.bounds.append(tmp_rect)

                first_time = False
                self.draw()

        touched_bounds = list()
        if pg.mouse.get_pressed()[2]:
            mouse_x, mouse_y = self.get_mouse_pos()
            if self.is_in_map(mouse_x, mouse_y):
                for rect in self.bounds:
                    if rect.collidepoint(mouse_x, mouse_y):
                        touched_bounds.append(rect)

                for touched in touched_bounds:
                    self.bounds.remove(touched)

    def mouse_listener(self):
        """Listen mouse button"""
        mouse_x, mouse_y = self.get_mouse_pos()
        paint_x, paint_y = self.calc_mouse_pos(mouse_x, mouse_y)
        print(paint_x, paint_y)

        if self.paint_pot.clicked(paint_x, paint_y) and self.cut_surface != None:
            self.layers[f"layer_{self.selected_layer}"] = self.paint_pot.action(
                self.layers[f"layer_{self.selected_layer}"],
                self.cut_surface)

        if self.rubber.clicked(paint_x, paint_y):
            self.layers[f"layer_{self.selected_layer}"] = self.rubber.action()

        if pg.mouse.get_pressed()[0]:
            if self.tileset.get_move_x() < mouse_x <= self.tileset.tileset_width and self.tileset.get_move_y() < mouse_y <= self.tileset.tileset_height:
                self.cut_surface = {
                    'image': self.tileset.get_tileset().subsurface(
                        pg.Rect(
                            paint_x * TILESIZE - self.tileset.get_move_x(),
                            paint_y * TILESIZE - self.tileset.get_move_y(),
                            TILESIZE, TILESIZE)).copy(),
                    'pos': (paint_x,
                            paint_y - self.tileset.get_move_y() // TILESIZE)}
                print('pos', self.cut_surface['pos'])
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

        self.draw_text(f'Layer Selected: {self.selected_layer}', self.text_font, 30, WHITE, WIDTH, HEIGHT, align="se")

        self.draw_text(f'Tile Selected: ', self.text_font, 30, WHITE, WIDTH // 2, HEIGHT, align="s")
        if self.cut_surface != None:
            self.screen.blit(self.cut_surface['image'], (19 * TILESIZE, HEIGHT - TILESIZE))

        # faire la doc absolument
        # mettre en place un système pour les murs
        # faire un menu accessible à tout moment pour avoir accès au short cuts
        # add a logger pour infomer dans la console ce qu'il se passe

        self.screen.blit(self.tileset.get_tileset(), (0 + self.tileset.get_move_x(), 0 + self.tileset.get_move_y()))

        for layer in self.layers:
            for rect in self.layers[layer]:
                self.screen.blit(rect.image, rect.rect)

        for rect in self.bounds:
            pg.draw.rect(self.screen, (255, 0, 0), rect, 2)

        self.tools.draw(self.screen)

        pg.display.flip()

    def show_start_screen(self):
        """Create the menu where the user choose a map"""
        self.screen.fill(BLACK)
        self.draw_text('Map Editor', self.title_font, 45, WHITE, WIDTH // 2, HEIGHT // 2, align="center")
        self.waiting = True
        self.selected = 0
        self.selected_map = None
        self.len_maps = 0
        while self.waiting:
            self.clock.tick(FPS)
            self.maps = [f for f in os.listdir(self.saved_maps) if path.isfile(path.join(self.saved_maps, f))]
            self.selected_map = self.maps[self.selected]
            self.len_maps = len(self.maps)
            for value in enumerate(self.maps):
                color = WHITE
                if value[0] == self.selected:
                    color = YELLOW
                self.draw_text(value[1], self.text_font, 25, color, WIDTH //
                               2, 6 * HEIGHT // 10 + 30 * value[0], align="center")
            self.draw_text("Press space to create a new file", self.text_font, 25, WHITE, WIDTH // 2, HEIGHT, align="s")
            self.start_events()

            pg.display.flip()

    def start_events(self):
        """Manage the event in the menu"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.waiting = False
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.waiting = False
                    self.quit()
                if event.key == pg.K_DOWN:
                    self.selected += 1
                    if self.selected >= self.len_maps:
                        self.selected = self.len_maps - 1
                    self.selected_map = self.maps[self.selected]
                if event.key == pg.K_UP:
                    self.selected -= 1
                    if self.selected < 0:
                        self.selected = 0
                    self.selected_map = self.maps[self.selected]
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN:
                    print(self.selected_map)
                    self.load_map(self.saved_maps, self.selected_map)
                    self.waiting = False
                if event.key == pg.K_SPACE:
                    now = datetime.now()
                    date = now.strftime("%Y-%b-%d")
                    timestamp = datetime.timestamp(now)
                    self.selected_map = f"{date}-{int(timestamp)}.tmx"
                    print("create a new file")  # ajouter le path dans le logger
                    self.waiting = False

    def load_map(self, pathname, filename):
        """Load a map for the editor

        Args:
            pathname (string)
            filename (string)
        """
        tm = pytmx.load_pygame(path.join(pathname, filename), pixel_alpha=True)
        # print(tm.tiledgidmap) # dict with the translation btween the gid and the pytmx gid
        ti = tm.get_tile_image_by_gid
        for index, layer in enumerate(tm.visible_layers):
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        # create the tile using the pos for the screen
                        new_tile = Tile(self.tileset, tile, x + Tile.get_offset_x(), y)
                        # set the gid using it from the tmx file
                        new_tile.gid = tm.tiledgidmap[gid]
                        # set the x value for the map
                        new_tile.x = x
                        self.layers[f"layer_{index}"].append(new_tile)

    def show_go_screen(self):
        pass

    @staticmethod
    def quit():
        """Function to quit everything"""
        pg.quit()
        sys.exit()
