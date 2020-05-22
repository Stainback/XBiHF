import pygame
import random
from character_desc import *


pygame.init()

display_width = 800
display_height = 600
win = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption((str(random.randint(3, 36)) + ' Bastards in the Hidden Fortress'))

map = [[1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],         #0
       [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],         #1
       [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0],         #2
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],         #3
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],         #4
       [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0],         #5
       [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0],         #6
       [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1],         #7
       [0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0],         #8
       [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],         #9
       [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],         #10
       [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]         #11


def decode_map(map):
    wall_layer = []
    for i in range(len(map)):
        for k in range(len(map[i])):
            if map[i][k] == 1:
                wall_layer.append(Wall(k * 25, i * 25))
    return wall_layer


def redraw_win(display, player, wall, interactive_object):
    # draw background
    display.fill((192, 192, 192))
    #draw walls
    for Wall in wall:
        Wall.draw(display)
    # draw character
    player.draw(display)
    # draw interactive objects
    interactive_object.draw(display)
    # update screen
    pygame.display.update()


def check_collision(player, wall):
    player_corners = [(player.x, player.y),
                      (player.x, player.y + player.dim),
                      (player.x + player.dim, player.y),
                      (player.x + player.dim, player.y + player.dim)]
    for Wall in wall:
        wall_corners = [(Wall.x, Wall.y),
                        (Wall.x, Wall.y + Wall.dim),
                        (Wall.x + Wall.dim, Wall.y),
                        (Wall.x + Wall.dim, Wall.y + Wall.dim)]
        # collision checking
        if abs(player_corners[0][0] - wall_corners[0][0]) <= player.dim:
            player.x = Wall.x + player.dim
        if abs(player_corners[0][1] - wall_corners[0][1]) <= player.dim:
            player.y = Wall.y + player.dim


def main():
    character = Char(100, 100)
    wall_segment = decode_map(map)
    int_obj = IntObject(200, 200)
    clock = pygame.time.Clock()
    tick = 0

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        character.movement()
        check_collision(character, wall_segment)
        redraw_win(win, character, wall_segment, int_obj)


main()
