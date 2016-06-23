from timeit import default_timer as current_time
from multiprocessing import Process, Pool
from operator import methodcaller

import multiprocessing, logging, pdb
mpl = multiprocessing.log_to_stderr()
mpl.setLevel(logging.INFO)

class Particle:
    """ Particle class represents an indivisable object on a 2D plane that is accelerated by forces """

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
        print(self.position)

class Simulation (Process):
    """ Simulation class represents an group of particles that can interact with each other """

    def __init__(self, plane, worker_amount=4):
        Process.__init__(self)
        self.plane = plane
        self.workers = Pool(processes=worker_amount)

    def call(self, number=0):
        Particle.update(self.plane[number])

    def run(self):
        while True:
            # Update each particle
            number_of_particles = len(self.plane)
            self.workers.map(self.call(), [0,1])
