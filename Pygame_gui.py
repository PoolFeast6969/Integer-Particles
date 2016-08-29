import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import pygame
import time
import math

from timeit import default_timer as current_time
from multiprocessing import Process, Pool
from time import sleep

# Some config width height settings
canvas_width = 1000
canvas_height = 1000

# Just define some colors we can use
color = pygame.Color(255, 255, 0, 0)
background_color = pygame.Color(0, 0, 0, 0)

pygame.init()
# Set the window title

# Make a screen to see
screen = pygame.display.set_mode((canvas_height ,canvas_width))
screen.fill(background_color)

# Make a surface to draw on
surface = pygame.Surface((canvas_width, canvas_height))
surface.fill(background_color)


class GUI (Process):
    """ window stuff """

    def __init__(self, plane, update_rate=60):
        Process.__init__(self)
        self.plane = plane
        self.update_interval = 1/update_rate

    def run(self):
        previous_update = current_time()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for particle in self.plane:
                surface.set_at((particle['x'], particle['y']), color)

            # Put the surface we draw on, onto the screen
            screen.blit(surface, (0, 0))

            # Show it.
            pygame.display.flip()

            # Sleep to maintain update rate
            update_delay = previous_update + self.update_interval - current_time()
            previous_update = current_time()
            sleep(max(0, update_delay))
