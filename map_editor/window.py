"""Map editor for a user to create a new tiled map"""

import sys
import os
from os import path
import pygame as pg
from datetime import datetime, date
import pytmx
# pylint: disable=import-error
from settings import WIDTH, HEIGHT, TITLE, FPS, TILESIZE, LIGHTGREY, RED,  BGCOLOR, MAPSIZE, WHITE, BLACK, YELLOW, GREEN, VIEWSIZE
# pylint: disable=import-error
from tileset import Tileset
# pylint: disable=import-error
from tile import Tile
# pylint: disable=import-error
from tools import Paint, Rubber, Player
# pylint: disable=import-error
from logger import logger
# pylint: disable=import-error
from tilemap import Camera


class Window():
    """Open the main window"""

    def __init__(self):
        logger.info('Start Window')
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
        self.players = list()

    def draw_text(self, text, font_name, size, color, x, y, align="nw", screen=None):
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
        if not screen:
            self.screen.blit(text_surface, text_rect)
        else:
            screen.blit(text_surface, text_rect)

    def load_data(self):
        """Load data"""
        logger.info('Load data')
        game_folder = path.dirname('..')
        self.assets_folder = path.join(game_folder, 'assets')
        self.map_editor_folder = path.join(self.assets_folder, 'map_editor')
        self.fonts_folder = path.join(self.assets_folder, 'fonts')
        self.saved_maps = path.join(self.assets_folder, 'saved_maps')
        self.tileset = Tileset(self.map_editor_folder, 'town1.png')
        self.title_font = path.join(self.fonts_folder, 'Roboto-Regular.ttf')
        self.text_font = path.join(self.fonts_folder, 'Roboto-Regular.ttf')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

    def new(self):
        """Create data for a new loading"""
        self.map = pg.Surface((MAPSIZE * TILESIZE, MAPSIZE * TILESIZE))
        self.camera = Camera(MAPSIZE * TILESIZE, MAPSIZE * TILESIZE)
        self.show_shortcuts = False
        self.cut_surface = None
        self.map_color = None
        self.selected_layer = 0
        self.selected_tool = None
        self.saved = False
        self.alpha = 0
        self.tool_images = {'paint_pot': pg.Surface((TILESIZE, TILESIZE)),
                            'rubber': pg.Surface((TILESIZE, TILESIZE)),
                            'p': pg.Surface((TILESIZE, TILESIZE))}
        self.tools = pg.sprite.Group()

        self.paint_pot = Paint(self, 9, 0, 'paint_pot')
        self.rubber = Rubber(self, 10, 0, 'rubber')
        self.player = Player(self, 9, 1, 'p')

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
                    pg.event.wait()
                    self.save_map()
                    self.saved = True
                if event.key == pg.K_k and pg.key.get_mods() & pg.KMOD_CTRL:
                    self.show_shortcuts = not self.show_shortcuts
                    logger.info("Display all shortcuts")
                if event.key == pg.K_r:
                    self.cut_surface = None
                    logger.info('Remove cut surface')
                if event.key in [pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]:
                    self.selected_layer = event.unicode
                    logger.info(f'Layer selected {self.selected_layer}')
            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.key.get_mods() & pg.KMOD_ALT:
                    self.bound_drawer()
                else:
                    self.tileset.get_mouse(event)
                    self.mouse_listener()

    def save_map(self):
        """Save a tmx file map"""
        with open(path.join(self.map_editor_folder, 'map_template.tmx'), 'r') as r, open(path.join(self.saved_maps, self.selected_map), 'w') as f:
            for row in r:
                if row.rstrip('\n') == '_MAP':
                    f.write(
                        f'<map version="1.4" tiledversion="1.4.2" orientation="orthogonal" renderorder="right-down" width="{MAPSIZE}" height="{MAPSIZE}" tilewidth="32" tileheight="32" infinite="0" nextlayerid="2" nextobjectid="1">')
                elif row.rstrip('\n') == '_LAYERS':
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
                                if row_layer == MAPSIZE - 1 and col_layer == MAPSIZE - 1:
                                    f.write('\n')
                                elif col_layer != MAPSIZE - 1:
                                    f.write(',')
                                else:
                                    f.write(',\n')
                        f.write("  </data>\n")
                        f.write(" </layer>\n")
                elif row.rstrip('\n') == '_OBJECTS':
                    f.write(' <objectgroup name="Obstacles">\n')
                    i = 1
                    for index, rect in enumerate(self.bounds):
                        i = index
                        f.write(
                            f'  <object id="{index + 1}" name="wall" x="{rect.x - Tile.get_offset_x() * TILESIZE}" y="{rect.y}" width="{rect.width}" height="{rect.height}"/>\n')
                    for index, rect in enumerate(self.players):
                        f.write(
                            f'  <object id="{index + i + 2}" name="player" x="{rect.x - Tile.get_offset_x() * TILESIZE}" y="{rect.y}" width="{rect.width}" height="{rect.height}"/>\n')
                    f.write(' </objectgroup>\n')
                else:
                    f.write(row)
            logger.info(f'Save "{self.selected_map}" in "{path.abspath(self.saved_maps)}"')

    def bound_drawer(self):
        """Draw wall"""
        # reset the relative pos
        pg.mouse.get_rel()
        left, top = self.get_mouse_pos()
        move_x = 0
        move_y = 0
        first_time = True
        bound_size = len(self.bounds)
        while pg.mouse.get_pressed()[0]:
            pg.event.poll()

            mouse_x, mouse_y = self.get_mouse_pos()
            paint_x, paint_y = pg.mouse.get_rel()

            if self.is_in_map(mouse_x, mouse_y):
                if not first_time:
                    self.bounds = self.bounds[0:-1]
                move_x += paint_x
                move_y += paint_y

                tmp_rect = pg.Rect(left - self.camera.x, top - self.camera.y, move_x, move_y)
                self.bounds.append(tmp_rect)

                first_time = False
                self.draw()

        if len(self.bounds) > bound_size:
            logger.info("Create a wall")

        touched_rect = list()
        if pg.mouse.get_pressed()[2]:
            mouse_x, mouse_y = self.get_mouse_pos()
            if self.is_in_map(mouse_x, mouse_y):
                for rect in self.bounds:
                    if rect.collidepoint(mouse_x, mouse_y):
                        touched_rect.append(rect)

                for touched in touched_rect:
                    self.bounds.remove(touched)
                    logger.info('Remove a wall')

                touched_rect = list()
                for rect in self.players:
                    if rect.collidepoint(mouse_x, mouse_y):
                        touched_rect.append(rect)

                for touched in touched_rect:
                    self.players.remove(touched)
                    logger.info('Remove a player')

    def mouse_listener(self):
        """Listen mouse button"""
        mouse_x, mouse_y = self.get_mouse_pos()
        paint_x, paint_y = self.calc_mouse_pos(mouse_x, mouse_y)

        if self.paint_pot.clicked(paint_x, paint_y) and self.cut_surface != None:
            self.layers[f"layer_{self.selected_layer}"] = self.paint_pot.action(
                self.layers[f"layer_{self.selected_layer}"],
                self.cut_surface)
            logger.info("Use paint pot")

        if self.rubber.clicked(paint_x, paint_y):
            self.layers[f"layer_{self.selected_layer}"] = self.rubber.action()
            logger.info("Use rubber")

        if pg.mouse.get_pressed()[0] and self.is_in_map(mouse_x, mouse_y) and self.selected_tool:
            self.selected_tool.action(self.players, mouse_x, mouse_y)
            logger.info(f"Use action of {self.selected_tool.name}")

        if self.player.clicked(paint_x, paint_y):
            self.selected_tool = self.player
            logger.info("Select player tool")

        self.cut_tile()
        self.add_tiles()
        self.remove_tiles()

    def cut_tile(self):
        mouse_x, mouse_y = self.get_mouse_pos()
        paint_x, paint_y = self.calc_mouse_pos(mouse_x, mouse_y)
        if pg.mouse.get_pressed()[0]:
            if self.tileset.get_move_x() < mouse_x <= self.tileset.tileset_width and self.tileset.get_move_y() < mouse_y <= self.tileset.tileset_height:
                self.selected_tool = None
                self.cut_surface = {
                    'image': self.tileset.get_tileset().subsurface(
                        pg.Rect(
                            paint_x * TILESIZE - self.tileset.get_move_x(),
                            paint_y * TILESIZE - self.tileset.get_move_y(),
                            TILESIZE, TILESIZE)).copy(),
                    'pos': (paint_x,
                            paint_y - self.tileset.get_move_y() // TILESIZE)}
                logger.info(f"Cut surface at {self.cut_surface['pos']}")

    def add_tiles(self):
        while pg.mouse.get_pressed()[0]:
            pg.event.poll()
            mouse_x, mouse_y = self.get_mouse_pos()
            paint_x, paint_y = self.calc_mouse_pos(mouse_x, mouse_y)
            if self.is_in_map(mouse_x, mouse_y):
                if pg.mouse.get_pressed()[0] and self.cut_surface != None:
                    x = paint_x - self.camera.get_x()
                    y = paint_y - self.camera.get_y()
                    if self.find_in_layer(self.layers[f"layer_{self.selected_layer}"], x - Tile.get_offset_x(), y):
                        logger.info(f'Can\'t add this tile at {x} {y}')
                    else:
                        tile = Tile(
                            self.tileset, self.cut_surface['image'].copy(),
                            self.cut_surface['pos'][0],
                            self.cut_surface['pos'][1])
                        tile.set_pos(x, y)
                        self.layers[f'layer_{self.selected_layer}'].append(tile)
                        logger.info(
                            f"Create a tile at {x} {y} in layer {self.selected_layer}")
            self.draw()

    def remove_tiles(self):
        while pg.mouse.get_pressed()[2]:
            pg.event.poll()
            mouse_x, mouse_y = self.get_mouse_pos()
            paint_x, paint_y = self.calc_mouse_pos(mouse_x, mouse_y)
            if self.is_in_map(mouse_x, mouse_y):
                if pg.mouse.get_pressed()[2]:
                    x = paint_x - self.camera.get_x() - Tile.get_offset_x()
                    y = paint_y - self.camera.get_y()
                    if self.find_in_layer(self.layers[f"layer_{self.selected_layer}"], x, y):
                        self.remove_tile(self.layers[f"layer_{self.selected_layer}"],  x, y)
                        logger.info(f"Remove tile at {x} {y} in layer {self.selected_layer}")
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
            if tile.x == x and tile.y == y:
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
            if tile.x == x and tile.y == y:
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
        return WIDTH - VIEWSIZE * TILESIZE < x < WIDTH and 0 < y < VIEWSIZE * TILESIZE

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
        self.camera.update()

    def draw_grid(self):
        """Draw a grid to visualize"""
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

        pg.draw.line(self.screen, RED, (WIDTH - VIEWSIZE * TILESIZE, 0),
                     (WIDTH - VIEWSIZE * TILESIZE, VIEWSIZE * TILESIZE), 2)
        pg.draw.line(self.screen, RED, (WIDTH - VIEWSIZE * TILESIZE, VIEWSIZE * TILESIZE),
                     (WIDTH, VIEWSIZE * TILESIZE), 2)

    def draw(self):
        """Draw all elements to the screen"""
        self.screen.fill(BGCOLOR)
        self.draw_grid()

        self.draw_text(f'Layer Selected: {self.selected_layer}', self.text_font, 30, WHITE, WIDTH, HEIGHT, align="se")

        self.draw_text(f'Tile Selected: ', self.text_font, 30, WHITE, WIDTH // 2, HEIGHT, align="s")
        if self.cut_surface != None:
            self.screen.blit(self.cut_surface['image'], (19 * TILESIZE, HEIGHT - TILESIZE))

        self.screen.blit(self.tileset.get_tileset(), (0 + self.tileset.get_move_x(), 0 + self.tileset.get_move_y()))

        for layer in self.layers:
            for rect in self.layers[layer]:
                cam_rect = self.camera.apply(rect.rect)
                if self.is_in_map(cam_rect.centerx, cam_rect.centery):
                    self.screen.blit(rect.image, cam_rect)

        for rect in self.bounds:
            # width - cam_offset + diff between start rect and map border
            rect_width = rect.width + self.camera.get_x() * TILESIZE + (rect.left - Tile.get_offset_x() * TILESIZE)
            rect_height = rect.height + self.camera.get_y() * TILESIZE
            cam_rect = self.camera.apply(rect)
            if cam_rect.left < Tile.get_offset_x() * TILESIZE:
                cam_rect.left = Tile.get_offset_x() * TILESIZE
                cam_rect.width = rect_width
                if cam_rect.width < 0:
                    cam_rect.width = 0
            rect_bottom = cam_rect.bottom
            if cam_rect.bottom > VIEWSIZE * TILESIZE:
                cam_rect.height = rect.height - (rect_bottom - VIEWSIZE * TILESIZE)
                cam_rect.bottom = VIEWSIZE * TILESIZE
                if cam_rect.height < 0:
                    cam_rect.height = 0

            if cam_rect.width != 0 and cam_rect.height != 0:
                pg.draw.rect(self.screen, (255, 0, 0), cam_rect, 2)

        for rect in self.players:
            pg.draw.rect(self.screen, GREEN, rect, 2)

        self.tools.draw(self.screen)

        if self.show_shortcuts:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text('Shortcuts', self.title_font, 45, YELLOW, WIDTH / 2, 0, align="n")

            self.draw_text('CTRL + K: show all shortcuts', self.text_font, 25, WHITE, 0, 1 * HEIGHT / 10, align="w")
            self.draw_text('Left Click: select a tile', self.text_font, 25, WHITE, 0, 2 * HEIGHT / 10, align="w")
            self.draw_text('ZQSD or Scroll Wheel: move the tileset',
                           self.text_font, 25, WHITE, 0, 3 * HEIGHT / 10, align="w")

            self.draw_text('Number: select a layer', self.text_font, 25, WHITE, WIDTH // 2, 1 * HEIGHT / 10, align="w")
            self.draw_text('Left Click:  add a tile',
                           self.text_font, 25, WHITE, WIDTH // 2, 2 * HEIGHT / 10, align="w")
            self.draw_text('Right Click: remove a tile',
                           self.text_font, 25, WHITE, WIDTH // 2, 3 * HEIGHT / 10, align="w")
            self.draw_text('ALT + Left Click: create a wall', self.text_font,
                           25, WHITE, WIDTH // 2, 4 * HEIGHT / 10, align="w")
            self.draw_text('ALT + Right Click: remove a wall or a player', self.text_font,
                           25, WHITE, WIDTH // 2, 5 * HEIGHT / 10, align="w")
            self.draw_text('CTRL + R: remove the selected tile',
                           self.text_font, 25, WHITE, WIDTH // 2, 6 * HEIGHT / 10, align="w")
            self.draw_text('CTRL + S: save the map', self.text_font, 25, WHITE, WIDTH // 2, 7 * HEIGHT / 10, align="w")

        transition = pg.Surface((WIDTH, HEIGHT))
        transition.fill(BLACK)
        transition.set_alpha(self.alpha)
        if self.saved:
            self.alpha += 20

        if self.alpha >= 255:
            self.saved = False

        if self.alpha > 0 and not self.saved:
            self.alpha -= 20

        if self.saved or self.alpha > 0:
            transition = pg.Surface((WIDTH, HEIGHT))
            transition.fill(BLACK)
            transition.set_alpha(self.alpha)
            self.draw_text('Saved', self.title_font, 50, WHITE,
                           WIDTH // 2, HEIGHT / 2, align="center", screen=transition)
            self.screen.blit(transition, (0, 0))
        pg.display.flip()

    def show_start_screen(self):
        """Create the menu where the user choose a map"""
        logger.info("Start menu")
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
            self.draw_text("Press space to create a new file", self.text_font,
                           25, WHITE, WIDTH // 2, HEIGHT, align="s")
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
                    logger.info(f"Selected map: {self.selected_map}")
                if event.key == pg.K_UP:
                    self.selected -= 1
                    if self.selected < 0:
                        self.selected = 0
                    self.selected_map = self.maps[self.selected]
                    logger.info(f"Selected map: {self.selected_map}")
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN:
                    self.load_map(self.saved_maps, self.selected_map)
                    self.waiting = False
                if event.key == pg.K_SPACE:
                    now = datetime.now()
                    date = now.strftime("%Y-%b-%d")
                    timestamp = datetime.timestamp(now)
                    self.selected_map = f"{date}-{int(timestamp)}.tmx"
                    logger.info(f'Create "{self.selected_map}" in "{path.abspath(self.saved_maps)}"')
                    self.waiting = False

    def load_map(self, pathname, filename):
        """Load a map for the editor

        Args:
            pathname (string)
            filename (string)
        """
        logger.info(f'Load "{self.selected_map}" from "{path.abspath(self.saved_maps)}"')
        tm = pytmx.load_pygame(path.join(pathname, filename), pixel_alpha=True)
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
        for obj in tm.objects:
            if obj.name == "wall":
                rect = pg.Rect(obj.x + Tile.get_offset_x() * TILESIZE, obj.y, obj.width, obj.height)
                self.bounds.append(rect)
            if obj.name == 'player':
                rect = pg.Rect(obj.x + Tile.get_offset_x() * TILESIZE, obj.y, obj.width, obj.height)
                self.players.append(rect)
        logger.info('Map loaded')

    def show_go_screen(self):
        pass

    @staticmethod
    def quit():
        """Function to quit everything"""
        pg.quit()
        sys.exit()
