from timeit import default_timer as current_time
from multiprocessing import Process, Event
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
        self.acceleration = {'x':0,'y':90.81}

    def update(self):
        for axis in self.position:
            # Calculate time since update was last run
            elapsed_time = current_time() - self.time_of_last_update[axis]
            # Determine if position change needed
            try:
                inverse_velocity = 1 / abs( self.velocity[axis] + self.acceleration[axis] * elapsed_time )
            except ZeroDivisionError:
                inverse_velocity = 0
            if (elapsed_time >= inverse_velocity):
                # Calculate acceleration toward center
                self.acceleration[axis] = -(self.position[axis] - 500)
                # Calculate velocity
                self.velocity[axis] = self.velocity[axis] + self.acceleration[axis] * elapsed_time
                # Edge bouncing
                if not (0 <= self.position[axis] <= 1000):
                    self.velocity[axis] = -self.velocity[axis]/1.7
                    # Teleport back inside displayed range
                    if (self.position[axis] > 500):
                        self.position[axis] = 1000
                    else:
                        self.position[axis] = 0
                # Move to new position
                self.position[axis] = self.position[axis] + round( elapsed_time * self.velocity[axis] )
                # Reset the timer
                self.time_of_last_update[axis] = current_time()

class World (Process):
    """ A group of particles that can interact with each other """

    def __init__(self, plane, send, update_rate=60):
        Process.__init__(self)
        self.plane = plane
        self.send = send
        self.update_interval = 1/update_rate
        self.exit = Event()
        logger.info('Initialised')

    def run(self):
        logger.info('Running')
        previous_update = current_time()
        while not self.exit.is_set():
            # Update each particle
            for particle in self.plane:
                particle.update()

            # stuff and things
            self.send.send(self.plane)

            # Sleep to maintain update rate
            update_delay = self.update_interval - (current_time() - previous_update)
            previous_update = current_time()
            sleep(max(0, update_delay))

    def terminate(self):
        logger.info('Exiting')
        self.exit.set()
