import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Start Manager (shares plane between processes)
from multiprocessing import Process, Manager, Pipe, Array
recv, send = Pipe(False)

# Make up some things to simulate
from Physics import Particle
from random import randint as random_integer
# Some config width height settings
width = 1000
height = 1000
particle_amount = 5
random_plane = [Particle(X_position=random_integer(0, width), Y_position=random_integer(0, height), X_velocity=random_integer(-500, 500), Y_velocity=random_integer(-500, 500)) for count in range(particle_amount)]
logger.info('Created plane with %s particles', particle_amount)

# Start the display
import pygame
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))

# Initialise the physics stuff
from Physics import World
Jacks_sweet_thread = World(random_plane, send)

from timeit import default_timer as current_time
from multiprocessing import Process, Pool
from time import sleep

import ctypes
import numpy as np

pixel_array_base = Array(ctypes.c_int, width*height)
pixel_array = np.ctypeslib.as_array(pixel_array_base.get_obj())
pixel_array = pixel_array.reshape(width, height)

from pygametranslator import Translator
Jacks_sweet_threads = Translator(recv, pixel_array)

# Start things
Jacks_sweet_thread.start()
Jacks_sweet_threads.start()
update_interval = 1/60
running = True
previous_update = current_time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.surfarray.blit_array(screen, pixel_array)
    pygame.display.flip()
    clock.tick()
    pygame.display.set_caption('FPS: ' + str(int(clock.get_fps())))

    # Sleep to maintain update rate
    update_delay = update_interval - (current_time() - previous_update)
    previous_update = current_time()
    sleep(max(0, update_delay))

logger.info('Exiting')
pygame.display.quit()
pygame.quit()
Jacks_sweet_threads.terminate()
Jacks_sweet_threads.join()
Jacks_sweet_thread.terminate()
Jacks_sweet_thread.join()
logger.info('Exit Complete')
