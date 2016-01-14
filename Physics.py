from timeit import default_timer as current_time
import time

class Particle:
    def __init__(self, mass=600, X_velocity=0, Y_velocity=0, X_position=0, Y_position=0):
        self.mass = mass
        self.position = {'x':X_position,'y':Y_position}
        self.velocity = {'x':X_velocity,'y':Y_velocity}
        self.time_of_last_update = {'x':current_time(),'y':current_time()}

    def update(self):
        for axis in self.position:
            # Calculate time since update was last run
            elapsed_time = current_time() - self.time_of_last_update[axis]
            # Calculate acceleration
            # acceleration = force[axis] / self.mass
            acceleration = -10
            # Calculate velocity
            self.velocity[axis] = self.velocity[axis] + ( acceleration * elapsed_time )
            # Change position
            if (elapsed_time >= 1 / abs( self.velocity[axis] )):
                self.position[axis] = self.position[axis] + int( elapsed_time * self.velocity[axis] )
                self.time_of_last_update[axis] = current_time()
            print("Position: " + str( self.position ), end="\r")

cool_particle = Particle(X_velocity=75,Y_position=100)

while (None is None):
    cool_particle.update()
    time.sleep(1/60)
