import pygame
from settings import *
from engine_objects import *


class Map:
    def __init__(self, map_path):
        self.map_data = []
        self.obj_layer = []
        self.map_path = map_path
        with open(self.map_path) as m:
            for line in m:
                self.map_data.append((line.strip()).split(sep=' '))
        self.map_width = len(self.map_data[0]) * CELL
        self.map_height = len(self.map_data) * CELL

    def decode(self):
        for row in range(len(self.map_data)):
            for column in range(len(self.map_data[row])):
                if self.map_data[row][column] == '1':
                    self.obj_layer.append(Wall(column * CELL, row * CELL, all_sprites, obj_sprites, unpass_sprites))
                if self.map_data[row][column] == '2':
                    self.obj_layer.append(IntObject(column * CELL, row * CELL, all_sprites, obj_sprites, pass_sprites))
                if self.map_data[row][column] == '3':
                    self.obj_layer.append(Door(column * CELL, row * CELL, all_sprites, obj_sprites, unpass_sprites))
        return self.obj_layer
