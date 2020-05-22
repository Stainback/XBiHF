import pygame

display_width = 800
display_height = 600
celldim = 25

#colors
BLACK = (0, 0, 0)
DARK_OLIVE_GREEN = (85, 107, 47)
TEAL = (0, 128, 128)

class Char:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dim = celldim
        self.color = DARK_OLIVE_GREEN
        self.rect = (x, y, celldim, celldim)
        self.speed = 4

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        self.rect = (self.x, self.y, self.dim, self.dim)


class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dim = celldim
        self.color = BLACK
        self.rect = (x, y, celldim, celldim)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)


class IntObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dim = celldim
        self.color = TEAL
        self.rect = (x, y, celldim, celldim)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)