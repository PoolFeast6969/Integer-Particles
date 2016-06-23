from timeit import default_timer as current_time
from multiprocessing import Process
from time import sleep

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Terminal_Output (Process):
    def __init__(self, pipe):
        Process.__init__(self)
        self.pipe = pipe
        logger.info('Initialised Output')

    def run(self):
        previous_update = current_time()
        while True:
            plane = self.pipe.recv()
            for particle in plane:
                print(particle.position)
