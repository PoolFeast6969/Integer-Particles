import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from multiprocessing import Process, Event
import ctypes
import numpy as np
import copy

import pygame
from pygame.locals import *

class Translator (Process):
    """ not sure """

    def __init__(self, recv, pixel_array):
        Process.__init__(self)
        self.pixel_array = pixel_array
        self.recv = recv
        self.exit = Event()
        logger.info('Initialised')


    def terminate(self):
        logger.info('Exiting')
        self.exit.set()

    def run(self):
        logger.info('Running')
        initial_color = 6215470
        while not self.exit.is_set():
            for particle in self.recv.recv():
                initial_color = initial_color + 1234
                if (0 < particle.position['x'] < 1000) and (0 < particle.position['y'] < 1000):
                    self.pixel_array[particle.position['x'], particle.position['y']] = initial_color
