"""Create the map viewer manager"""
from config.buttons import HEIGHT_SLIDER, WIDTH_SLIDER
from components.cursor import Cursor
from config.colors import BEIGE
import os
from os import path

import pygame as pg
from config.sprites import ITEMS
from config.store import STORE_BG
from config.window import HEIGHT, TILESIZE, WIDTH
from logger import logger
from utils.tilemap import TiledMap


class MapViewerManager:
    def __init__(self, folder, filename, game):
        self.game = game
        self.map = TiledMap(path.join(folder, filename))
        self.folder = folder

        self.index = 0

        self.game_folder = path.dirname('.')
        self.maps_path = folder
        self.saved_notes = path.join(self.game_folder, 'assets', 'saved_notes')
        self.maps_names = [f for f in os.listdir(self.maps_path) if f.endswith('.tmx')]
        self.saved_notes_names = [f for f in os.listdir(self.saved_notes) if f.endswith('.png')]
        self.len_maps = len(self.maps_names)

        self.set_new_map(folder, filename)

        self.pen_btn = pg.Rect((0, 3 * TILESIZE), (TILESIZE, TILESIZE))
        self.pen = pg.transform.scale(ITEMS['pen'], (int(TILESIZE * 0.8), int(TILESIZE * 0.8)))
        self.eraser_btn = pg.Rect((0, 4 * TILESIZE), (TILESIZE, TILESIZE))
        self.eraser = pg.transform.scale(ITEMS['eraser'], (int(TILESIZE * 0.8), int(TILESIZE * 0.8)))
        self.bg = pg.transform.scale(STORE_BG, (TILESIZE, TILESIZE))

        # settings
        self.color = (255, 0, 0)
        self.size = 3

        self.active = False

    # on crée un flag qui permet d'activer ou de désactive si oui ou non on veut un carousel de carte, ça permet de gérer facilement les cartes uniques comme les customs maps.

    def save(self):
        """Save the canvas"""
        try:
            name = f"{self.maps_names[self.index].split('.tmx')[0]}.png"
            _path = path.join(self.saved_notes, name)
            pg.image.save(self.canvas, _path)
            logger.info("Saved notes %s, in %s", name, path.abspath(_path))
        except EnvironmentError as e:
            logger.exception(e)

    def load(self, filename):
        """Load a file if existe

        Args:
            filename (str)
        """
        self.new_canvas()
        name = filename.split(".tmx")[0] + '.png'
        if name in self.saved_notes_names:
            logger.info("Load %s", path.join(self.saved_notes, name))
            self.canvas = pg.image.load(path.join(self.saved_notes, name)).convert_alpha()

            # on doit faire une variable qui contient la surface et si on la trouve pas alors on met dedans celle du map manager

    def set_new_map(self, folder, filename):
        """Set a new filename and recreate a map

        Args:
            filename (str)
            folder (str)
        """
        self.folder = folder
        self.map.new_map(path.join(folder, filename))  # et ça du coup ça va aller dans le laod
        self.new_map()
        self.load(filename)

    def new_canvas(self):
        """Create a new canvas"""
        logger.info("Create a new canvas")
        self.canvas = pg.Surface(self.map_img.get_size()).convert_alpha()
        self.canvas.fill((0, 0, 0, 0))
        self.canvas_rect = self.canvas.get_rect()
        self.canvas_rect.center = (WIDTH // 2, HEIGHT // 2)

    def new_map(self):
        """Create the map image"""
        logger.info("Create a new map")
        self.height = int(HEIGHT * 0.8)
        self.map_ratio = self.map.width / self.map.height
        self.width = int(self.height * self.map_ratio)

        self.map_img = pg.transform.scale(self.map.make_map(), (self.width, self.height))
        self.map_rect = self.map_img.get_rect()
        self.map_rect.center = (WIDTH // 2, HEIGHT // 2)

    def event(self, event):
        """Evetns

        Args:
            event (Event)
        """
        if event.type == pg.KEYUP:
            if self.folder.endswith('levels_maps'):
                if event.key == pg.K_RIGHT:
                    self.save()
                    self.index += 1
                    if self.index >= self.len_maps:
                        self.index = self.len_maps - 1
                        logger.info('No more maps')
                    else:
                        logger.info('Next map')
                        self.set_new_map(self.maps_path, self.maps_names[self.index])
                if event.key == pg.K_LEFT:
                    self.save()
                    self.index -= 1
                    if self.index < 0:
                        self.index = 0
                        logger.info('No more maps')
                    else:
                        logger.info('Previous map')
                        self.set_new_map(self.maps_path, self.maps_names[self.index])
            if event.key == pg.K_e:
                self.use_eraser()
            if event.key == pg.K_r:
                self.use_stylus()
            if event.key == pg.K_n:
                self.new_canvas()

            if event.key == pg.K_s and pg.key.get_mods() & pg.KMOD_CTRL:
                self.save()

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.paint()
                pos_x, pos_y = pg.mouse.get_pos()
                if self.eraser_btn.collidepoint(pos_x, pos_y):
                    self.use_eraser()
                if self.pen_btn.collidepoint(pos_x, pos_y):
                    self.use_stylus()

    def paint(self):
        """Paint on the screen"""
        pg.mouse.get_rel()
        while pg.mouse.get_pressed()[0]:
            pg.event.poll()

            mouse_x, mouse_y = pg.mouse.get_pos()

            if self.canvas_rect.collidepoint(mouse_x, mouse_y):
                paint_x, paint_y = self.get_rel_mouse_pos()
                pg.draw.circle(self.canvas, self.color, (paint_x, paint_y), self.size)

                self.draw(self.game.screen)
                pg.display.update()

    def use_stylus(self):
        """Use the stylus"""
        logger.info("Use the stylus")
        self.color = (255, 0, 0)
        self.size = 3

    def use_eraser(self):
        """Use the eraser"""
        logger.info("Use the eraser")
        self.color = pg.Color(0, 0, 0, 0)
        self.size = 10

    def get_rel_mouse_pos(self):
        """Get the relative pos from the canvas

        Returns:
            tuple: x, y
        """
        x, y = pg.mouse.get_pos()
        x -= (WIDTH - self.width) // 2
        y -= (HEIGHT - self.height) // 2

        return x, y

    def update(self):
        """Update"""

    def draw(self, screen):
        """Draw"""
        screen.blit(self.map_img, self.map_rect)
        screen.blit(self.canvas, self.map_rect)

        self.game.draw_text(self.maps_names[self.index].split('.tmx')[0],
                            self.game.title_font, 56, BEIGE, WIDTH // 2, 0, align="n", screen=screen)

        screen.blit(self.bg, self.pen_btn)
        screen.blit(self.bg, self.eraser_btn)
        screen.blit(self.pen, (self.pen_btn.left + (TILESIZE - self.pen.get_width()) //
                               2, self.pen_btn.top + (TILESIZE - self.pen.get_height()) // 2))
        screen.blit(self.eraser, (self.eraser_btn.left + (TILESIZE - self.eraser.get_width()) //
                                  2, self.eraser_btn.top + (TILESIZE - self.eraser.get_height()) // 2))

        pos = pg.mouse.get_pos()
        if self.canvas_rect.collidepoint(pos):
            pg.draw.circle(screen, self.color, pos, self.size, width=2)
