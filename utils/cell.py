"""Used to create a representation of a cell"""
import pygame as pg
from config.window import TILESIZE
vec = pg.Vector2


class Cell():
    """classe de cases qui sert pour le pathfinding
    """

    def __init__(self, coor=vec(0, 0), g=0, f=0):
        self.coor = coor
        self.g = g
        self.f = f
        self.came_from = None
        self.connections = [vec(TILESIZE, 0), vec(0, TILESIZE), vec(-TILESIZE, 0), vec(0, -TILESIZE)]  # 4 ways movement
        #self.connections = [vec(TILESIZE,0), vec(TILESIZE,TILESIZE), vec(0,TILESIZE), vec(-TILESIZE,TILESIZE), vec(-TILESIZE,0), vec(-TILESIZE,-TILESIZE), vec(0,-TILESIZE), vec(TILESIZE,-TILESIZE)]

    def reconstruct_path(self, path):
        """create the list containing the path to the destination

        Returns:
            list: of cells
        """
        if self.came_from is not None:
            path.insert(0, self)
            return self.came_from.reconstruct_path(path)
        return path

    def neighbor(self):
        """analyse the surroundings of the cell to return its neighbors

        Returns:
            tuple: of the 4 neighbors around the cell
        """
        neighbors = [Cell(coor=self.coor + connection) for connection in self.connections]
        return neighbors

    def __str__(self):
        return f"{self.coor}"