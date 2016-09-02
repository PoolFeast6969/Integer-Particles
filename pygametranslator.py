import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from multiprocessing import Process
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

    def run(self):
        while True:
            for particle in self.recv.recv():
                if (0 < particle.position['x'] < 1000) and (0 < particle.position['y'] < 1000):
                    self.pixel_array[particle.position['x'], particle.position['y']] = 6612480
