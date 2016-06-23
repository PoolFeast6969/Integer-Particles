from timeit import default_timer as current_time
from multiprocessing import Process, Pool
from time import sleep

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Particle:
    """ An indivisable object on a 2D plane that is accelerated by forces """

    def __init__(self, X_position, Y_position, X_velocity=0 ,Y_velocity=0, mass=600):
        self.mass = mass
        self.velocity = {'x':X_velocity,'y':Y_velocity}
        self.position = {'x':X_position,'y':Y_position}
        self.time_of_last_update = {'x':current_time(),'y':current_time()}

    def update(self):
        for axis in self.position:
            # Calculate time since update was last run
            elapsed_time = current_time() - self.time_of_last_update[axis]
            # Calculate acceleration
            # acceleration = force[axis] / self.mass
            acceleration = -1
            # Calculate velocity
            self.velocity[axis] = self.velocity[axis] + ( acceleration * elapsed_time )
            # Change position if needed
            if (elapsed_time >= 1 / abs( self.velocity[axis] )):
                # Calculate new postion
                self.position[axis] = self.position[axis] + int( elapsed_time * self.velocity[axis] )
                # Reset the timer
                self.time_of_last_update[axis] = current_time()

class World (Process):
    """ A group of particles that can interact with each other """

    def __init__(self, plane, pipe, worker_amount=None, update_rate=30):
        Process.__init__(self)
        self.pipe = pipe
        self.plane = plane
        self.workers = Pool(processes=worker_amount)
        self.update_interval = 1/update_rate
        logger.info('Created World with %s updates per second', update_rate)

    def run(self):
        previous_update = current_time()
        while True:
            # Update each particle
            for particle in self.plane:
                particle.update()
            # Send to Graphics
            self.pipe.send(self.plane)
            # Sleep to maintain update rate
            update_delay = previous_update + self.update_interval - current_time()
            previous_update = current_time()
            sleep(max(0, update_delay))
