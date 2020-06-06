import pygame
import random
from settings import *
from engine_objects import *
from map import *

pygame.init()

win = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
pygame.display.set_caption((str(random.randint(3, 36)) + ' Bastards in the Hidden Fortress'))

# ------------------------------------------------ GAME ENGINE ------------------------------------------------------- #


def interact_with_objects(player, objects):
    for object in objects:
        if player.int_area.colliderect(object.rect) and object.__class__.__name__ == 'Door':
            if unpass_sprites.has(object):
                object.set_condition('open')
            else:
                object.set_condition('close')
        elif player.int_area.colliderect(object.rect) and object.__class__.__name__ == 'IntObject':
            print('grab')


def draw_grid(display):
    for x in range(0, W_WIDTH, CELL):
        pygame.draw.line(display, LIGHTGREY, (x, 0), (x, W_HEIGHT))
    for y in range(0, W_HEIGHT, CELL):
        pygame.draw.line(display, LIGHTGREY, (0, y), (W_WIDTH, y))


def redraw_win(display, player, cursor, clock, camera):
    all_sprites.update()
    camera.update(player)

    # draw background
    display.fill(DARKGREY)

    # all_sprites.draw(win)
    for sprite in all_sprites:
        display.blit(sprite.image, camera.apply(sprite))

    # devmod data
    if DEV_MOD == 'on':
        draw_grid(win)
        pygame.draw.rect(win, BLUE, player.int_area)
        pygame.draw.circle(win, RED, cursor, 5)
        pygame.draw.line(win, WHITE, player.rect.center, cursor, 2)
        # fps counter
        font = pygame.font.SysFont('Arial', 36, bold=True)
        display_fps = str(int(clock.get_fps()))
        render = font.render(display_fps, 0, RED)
        win.blit(render, (W_WIDTH - 65, 5))

    # update screen
    pygame.display.update()


# -------------------------------------- INITIALIZING OF THE GAME PROCESS -------------------------------------------- #


def main():
    # creating object layers
    map = Map('map_simple.txt')
    obj_layer = map.decode()
    # creating character
    character = Char(600, 600, all_sprites)
    # spawn camera
    camera = Camera(map.map_width, map.map_height)
    # initialize game timer
    clock = pygame.time.Clock()

    # main game loop
    while True:
        clock.tick(FPS)
        dt = clock.tick(FPS) / 1000
        cursor = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    interact_with_objects(character, obj_layer)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
        # events
        character.movement(dt)
        # updates
        redraw_win(win, character, cursor, clock, camera)

# initializing the game
main()
