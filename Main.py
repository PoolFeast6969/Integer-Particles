import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Start Manager (shares plane between processes)
from multiprocessing import Process, Manager, Pipe
recv, send = Pipe(False)

# Make up some things to simulate
from Physics import Particle
from random import randint as random_integer
# Some config width height settings
width = 1000
height = 1000
particle_amount = 700
random_plane = [Particle(X_position=random_integer(0, width), Y_position=random_integer(0, height), X_velocity=random_integer(-500, 500), Y_velocity=random_integer(-500, 500)) for count in range(particle_amount)]
logger.info('Created plane with %s particles', particle_amount)

# Initialise the physics stuff
from Physics import World
Jacks_sweet_thread = World(random_plane, send)
logger.info('Initialised World')

# Start things
Jacks_sweet_thread.start()
logger.info('Running Physics')


if __name__ == "__main__":

    import pygame
    from pygame.locals import *

    from timeit import default_timer as current_time
    from multiprocessing import Process, Pool
    from time import sleep

    # Just define some colors we can use
    color = pygame.Color(255, 255, 0, 0)
    background_color = pygame.Color(0, 0, 0, 0)

    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((height ,width), RESIZABLE|HWSURFACE|DOUBLEBUF)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(background_color)

        for particle in recv.recv():
            screen.set_at((particle.position['x'], particle.position['y']), color)

        pygame.display.flip()

        clock.tick()
        pygame.display.set_caption('FPS: ' + str(int(clock.get_fps())))

    Jacks_sweet_thread.terminate()
