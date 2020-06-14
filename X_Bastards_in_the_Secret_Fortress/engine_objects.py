import pygame
import math
from settings import *

all_sprites = pygame.sprite.Group()
obj_sprites = pygame.sprite.Group()
unpass_sprites = pygame.sprite.Group()
pass_sprites = pygame.sprite.Group()


class Char(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites):
        self.groups = all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.dim = CELL
        self.image = pygame.Surface([self.dim, self.dim])
        self.image.fill(RED)
        self.rect = pygame.Rect(x, y, CELL, CELL)
        self.int_area = self.rect.inflate(10, 10)
        self.speed = 500          # pixels per second

    def overview(self, cursor, display):
        center = self.rect.center
        guiding_vector_length = math.sqrt((center[0] - cursor[0]) ** 2 + (center[1] - cursor[1]) ** 2)
        cos_a, cos_b = 0, 0
        if guiding_vector_length != 0:
            cos_a = (center[0] - cursor[0]) / guiding_vector_length
            cos_b = (center[1] - cursor[1]) / guiding_vector_length
        end_point = (center[0] - DEPTH * cos_a, center[1] - DEPTH * cos_b)
        # main ray cast
        pygame.draw.line(display, WHITE, center, end_point)

    def movement(self, dt):
        keys = pygame.key.get_pressed()
        self.vx, self.vy = 0, 0
        if keys[pygame.K_w]:
            self.vy -= self.speed
        if keys[pygame.K_s]:
            self.vy += self.speed
        if keys[pygame.K_a]:
            self.vx -= self.speed
        if keys[pygame.K_d]:
            self.vx += self.speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        self.x += self.vx * dt
        self.rect.x = self.x
        self.y += self.vy * dt
        self.rect.y = self.y
        self.check_collisions()
        self.rect = pygame.Rect(self.x, self.y, self.dim, self.dim)
        self.int_area = self.rect.inflate(10, 10)

    def check_collisions(self):
        collisions = pygame.sprite.spritecollide(self, unpass_sprites, False)
        vectors = {}
        backward_vector = (0, 0)
        for object in collisions:
            vec_x = (self.rect.center[0] - (object.x + 0.5 * object.dim))
            if vec_x == 0:
                ort_x = 0
            else:
                ort_x = vec_x // abs(vec_x)
            vec_y = (self.rect.center[1] - (object.y + 0.5 * object.dim))
            if vec_y == 0:
                ort_y = 0
            else:
                ort_y = vec_y // abs(vec_y)
            if abs(vec_x) > abs(vec_y):
                vectors[object] = [[abs(vec_x), ort_x], [0, 0]]
            elif abs(vec_x) < abs(vec_y):
                vectors[object] = [[0, 0], [abs(vec_y), ort_y]]
            else:
                vectors[object] = [[abs(vec_x), ort_x], [abs(vec_y), ort_y]]
            x = 0
            dirort_x = 0
            y = 0
            dirort_y = 0
            for vector in vectors.values():
                if vector[0][0] > x:
                    x = vector[0][0]
                    dirort_x = vector[0][1]
                if vector[1][0] > y:
                    y = vector[1][0]
                    dirort_y = vector[1][1]
            backward_vector = (((0.5 * (self.dim + object.dim)) - x) * dirort_x,
                               ((0.5 * (self.dim + object.dim)) - y) * dirort_y)
        self.x += backward_vector[0]
        self.y += backward_vector[1]


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites, obj_sprites, unpass_sprites):
        self.groups = all_sprites, obj_sprites, unpass_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.dim = CELL
        self.image = pygame.Surface([self.dim, self.dim])
        self.image.fill(LIGHTGREY)
        self.rect = pygame.Rect(x, y, CELL, CELL)


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites, obj_sprites, unpass_sprites):
        self.groups = all_sprites, obj_sprites, unpass_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.dim = CELL
        self.image = pygame.Surface([self.dim, self.dim])
        self.image.fill(TEAL)
        self.rect = pygame.Rect(x, y, CELL, CELL)

    def set_condition(self, condition):
        if condition == 'open':
            unpass_sprites.remove(self)
            pass_sprites.add(self)
            self.image.fill(GREEN)
        if condition == 'close':
            pass_sprites.remove(self)
            unpass_sprites.add(self)
            self.image.fill(TEAL)


class IntObject(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites, obj_sprites, pass_sprites):
        self.groups = all_sprites, obj_sprites, pass_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.dim = CELL
        self.image = pygame.Surface([self.dim, self.dim])
        self.image.fill(YELLOW)
        self.rect = pygame.Rect(x, y, CELL, CELL)

