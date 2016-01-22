from timeit import default_timer as current_time
import time
from random import randint as random_integer
import numpy

class Particle:
    """ Particle class represents an indivisable object on a 2D plane that is accelerated by forces and interacts with other Particles """

    def __init__(self, mass=600, X_velocity=0, Y_velocity=0):
        self.mass = mass
        self.velocity = {'x':X_velocity,'y':Y_velocity}
        self.time_of_last_update = {'x':current_time(),'y':current_time()}

    def __str__(self):
        return str(self.velocity)

    def update(self, postion):
        for axis in position:
            # Calculate time since update was last run
            elapsed_time = current_time() - self.time_of_last_update[axis]
            # Calculate acceleration
            # acceleration = force[axis] / self.mass
            acceleration = -1
            # Calculate velocity
            self.velocity[axis] = self.velocity[axis] + ( acceleration * elapsed_time )
            # Change position
            if (elapsed_time >= 1 / abs( self.velocity[axis] )):
                position[axis] = position[axis] + int( elapsed_time * self.velocity[axis] )
                self.time_of_last_update[axis] = current_time()
                return position

#[Particle(X_velocity=random_integer(-10, 10), Y_position=random_integer(-1000, 1000), Y_velocity=random_integer(-10, 10), X_position=random_integer(-1000, 1000)) for count in range(30)]

Particle = numpy.vectorize(Particle)

plane = numpy.empty((1000, 1000), dtype = object)

plane[500,500] = Particle(X_velocity=random_integer(-10, 10), Y_velocity=random_integer(-10, 10))
plane[501,500] = Particle(X_velocity=random_integer(-10, 10), Y_velocity=random_integer(-10, 10))

while (None is None):
    print(plane[plane != numpy.array(None)])
        #if (particle.update(position) is not None):
