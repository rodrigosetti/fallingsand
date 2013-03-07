#! /usr/bin/env python
# coding: utf-8

import sys
import pygame
from pygame.locals import *
from sand import *

class PyGameEnvironment(Environment):

    def __init__(self, surface, *args, **kargs):
        super(PyGameEnvironment, self).__init__(*args, **kargs)
        self.surface = surface

    def report_change(self, position, particle):
        if particle == VOID:
            color = (0,0,0)
        elif particle == LIMIT:
            color = (100, 100, 100)
        elif particle == SAND:
            color = (255, 255, 0)
        else:
            color = (255, 0, 255)
        self.surface.set_at(position, color)

if __name__ == "__main__":

    WIDTH, HEIGHT = 640, 480

    # initialize pygame stuff
    pygame.init()
    fps_clock = pygame.time.Clock()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Falling sand game")

    # where to draw the particles
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill((0, 0, 0))

    # initialize the particles environment
    environment = PyGameEnvironment(surface, WIDTH, HEIGHT)

    # flags
    dragging = False

    while True:
        # blit the particles into the display
        window.blit(surface, (0,0))

        # update screen and fps
        pygame.display.update()
        fps_clock.tick(60)

        # perform user interaction
        if dragging:
            mouse_pos = pygame.mouse.get_pos()
            environment[mouse_pos] = SAND
            environment.awake(mouse_pos)

        # update
        environment.step()

        # handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                dragging = True
            elif event.type == MOUSEBUTTONUP:
                dragging = False

