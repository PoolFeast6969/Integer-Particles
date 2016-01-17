from timeit import default_timer as current_time
import time
from random import randint as random_integer

class Particle:
    """ Particle class represents a point on a 2D plane that is accelerated by forces and interacts with other Particles """

    def __init__(self, mass=600, X_velocity=0, Y_velocity=0, X_position=0, Y_position=0):
        self.mass = mass
        self.position = {'x':X_position,'y':Y_position}
        self.velocity = {'x':X_velocity,'y':Y_velocity}
        self.time_of_last_update = {'x':current_time(),'y':current_time()}

    def __str__(self):
        return str(self.position) #+ str(self.velocity)

    def update(self):
        for axis in self.position:
            # Calculate time since update was last run
            elapsed_time = current_time() - self.time_of_last_update[axis]
            # Calculate acceleration
            # acceleration = force[axis] / self.mass
            acceleration = -1
            # Calculate velocity
            self.velocity[axis] = self.velocity[axis] + ( acceleration * elapsed_time )
            # Change position
            if (elapsed_time >= 1 / abs( self.velocity[axis] )):
                # Collision detection
                self.position[axis] = self.position[axis] + int( elapsed_time * self.velocity[axis] )
                self.time_of_last_update[axis] = current_time()

plane = [Particle(X_velocity=random_integer(-10, 10), Y_position=random_integer(-1000, 1000), Y_velocity=random_integer(-10, 10), X_position=random_integer(-1000, 1000)) for count in range(30)]

while (None is None):
    for particle in plane:
        particle.update()
        print(particle)
    time.sleep(1/30)
    print("\033[1A[\033[2K" * len(plane), end="\r")
