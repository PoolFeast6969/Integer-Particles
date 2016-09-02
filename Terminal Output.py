from timeit import default_timer as current_time
from multiprocessing import Process
from time import sleep
import os

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Terminal_Output (Process):
    def __init__(self, plane, update_rate=60):
        Process.__init__(self)
        self.plane = plane
        self.update_interval = 1/update_rate
        logger.info('Initialised Output')

    def run(self):
        previous_update = current_time()
        while True:
            os.system('clear')
            # Go through each particle
            for particle in self.plane:
                print(particle.position)
            # Sleep to maintain update rate
            update_delay = previous_update + self.update_interval - current_time()
            previous_update = current_time()
            sleep(max(0, update_delay))
