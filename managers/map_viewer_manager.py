"""Create the map viewer manager"""
import os
from os import path

import pygame as pg
from config.window import HEIGHT, WIDTH
from logger import logger
from utils.tilemap import TiledMap


class MapViewerManager:
    def __init__(self, folder, filename, game):
        self.game = game
        self.map = TiledMap(path.join(folder, filename))

        self.index = 0

        self.game_folder = path.dirname('.')
        self.maps_path = folder
        self.saved_notes = path.join(self.game_folder, 'assets', 'saved_notes')
        self.maps_names = [f for f in os.listdir(self.maps_path) if f.endswith('.tmx')]
        self.saved_notes_names = [f for f in os.listdir(self.saved_notes) if f.endswith('.png')]
        self.len_maps = len(self.maps_names)

        self.set_new_map(folder, filename)

        # settings
        self.color = (255, 0, 0)
        self.size = 3

        self.active = False

    # on crée une fonction qui prend en paramètre le path qui permet de trouver la carte à afficher
    # on crée un flag qui permet d'activer ou de désactive si oui ou non on veut un carousel de carte, ça permet de gérer facilement les cartes uniques comme les customs maps.
    # il faut gérer le brouillard de guerre ! on va dire que non (mais c'est sûrement un souci avec le fait que on le gère sur la minimap mais au pire on le recodera)

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
        """
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
        """Events"""
        if event.type == pg.KEYUP:
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
        pass

    def draw(self, screen):
        """Draw"""
        screen.blit(self.map_img, self.map_rect)
        screen.blit(self.canvas, self.map_rect)

        pos = pg.mouse.get_pos()
        if self.canvas_rect.collidepoint(pos):
            pg.draw.circle(screen, self.color, pos, self.size, width=2)
