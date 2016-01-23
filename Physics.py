from timeit import default_timer as current_time
from random import randint as random_integer
from threading import Thread
import numpy


class Particle:
    """ Particle class represents an indivisable object on a 2D self.plane that is accelerated by forces and interacts with other Particles """

    def __init__(self, mass=600, X_velocity=0, Y_velocity=0):
        self.mass = mass
        self.velocity = {'x':X_velocity,'y':Y_velocity}
        self.time_of_last_update = {'x':current_time(),'y':current_time()}

    def __str__(self):
        return str(self.velocity)

    def update(self, X_position=0, Y_position=0):
        position = {'x':X_position,'y':Y_position}
        for axis in position:
            # Calculate time since update was last run
            elapsed_time = current_time() - self.time_of_last_update[axis]
            # Calculate acceleration
            # acceleration = force[axis] / self.mass
            acceleration = -1
            # Calculate velocity
            self.velocity[axis] = self.velocity[axis] + ( acceleration * elapsed_time )
            # Change position if needed
            if (elapsed_time >= 1 / abs( self.velocity[axis] )):
                position[axis] = position[axis] + int( elapsed_time * self.velocity[axis] )
                #Reset the timer
                self.time_of_last_update[axis] = current_time()
        return position


class Physics_Thread (Thread):
    def __init__(self):
        Thread.__init__(self)
        self.plane = numpy.empty((1000, 1000), dtype = object)
        for count in range(5):
            self.plane[random_integer(10, 999),count] = Particle(X_velocity=random_integer(-10, 10), Y_velocity=random_integer(-10, 10))
        self.run_signal = True

    def run(self):
        print('Running ' + str( self.__class__.__name__ ))
        while self.run_signal is True:
            particle_indexs = numpy.argwhere(self.plane)
            for particle in particle_indexs:
                position = {'x':particle[0], 'y':particle[1]}
                calculated_position = self.plane[position['x'], position['y']].update(X_position=position['x'], Y_position=position['y'])
                print(position, end='\r')
                if (calculated_position is not position):
                    self.plane[position['x'], position['y']], self.plane[calculated_position['x'], calculated_position['y']] = self.plane[calculated_position['x'], calculated_position['y']], self.plane[position['x'], position['y']]


Physics_Thread().start()
