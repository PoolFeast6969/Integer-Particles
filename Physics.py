from timeit import default_timer as current_time
from multiprocessing import Process, Event
from time import sleep

class Physics_Thread (Process):
    """ A group of particles that do things when stuff happens"""

    def __init__(self, frame_queue, particles, axes, properties):
        Process.__init__(self)
        self.exit = Event()
        self.frame = frame_queue
        self.particles = particles
        self.axes = axes
        self.properties = properties
        print(self.name+' Initialised')

    def run(self):
        while not self.exit.is_set():
            particles_to_update = self.frame.get(timeout = 3)
            for particle_index in particles_to_update:
                for axis in self.particles[particle_index]:
                    # Calculate time since particle was last updated
                    elapsed_time = current_time() - axis[self.properties.index('time of update')]
                    # Determine if a position change is needed
                    try:
                        inverse_velocity = 1 / (axis[self.properties.index('velocity')] + axis[self.properties.index('acceleration')] * elapsed_time)
                    except ZeroDivisionError:
                        inverse_velocity = 0
                    if (elapsed_time >= abs(inverse_velocity)):
                        # A position change is needed
                        # Calculate velocity
                        axis[self.properties.index('velocity')] = axis[self.properties.index('velocity')] + axis[self.properties.index('acceleration')] * elapsed_time
                        # Calculate new position
                        new_position = axis[self.properties.index('position')] + int(elapsed_time * axis[self.properties.index('velocity')])
                        # Calculate position accuracy lost due to rounding
                        lost_position = elapsed_time * axis[self.properties.index('velocity')] - int(elapsed_time * axis[self.properties.index('velocity')])
                        # Reset the timer and adjust time for loss of position
                        try:
                            axis[self.properties.index('time of update')] = current_time() - lost_position / axis[self.properties.index('velocity')]
                        except ZeroDivisionError:
                            axis[self.properties.index('time of update')] = current_time()
                        # Edge bouncing
                        if not (0 <= new_position <= 999):
                            axis[self.properties.index('velocity')] = axis[self.properties.index('velocity')]/-1.1
                            # Teleport back inside displayed range
                            if (new_position > 500):
                                new_position = 999
                            else:
                                new_position = 0
                        axis[self.properties.index('position')] = new_position

    def terminate(self):
        print(self.name+' Exiting')
        self.exit.set()
