from timeit import default_timer as current_time
from multiprocessing import Process, Event
from time import sleep
import ctypes

class Physics_Thread (Process):
    """ A group of particles that do things when stuff happens"""

    def __init__(self, frame_queue, particles):
        Process.__init__(self)
        self.exit = Event()
        self.frame = frame_queue
        self.particles = particles
        print(self.name+' Initialised')

    def run(self):
        while not self.exit.is_set():
            particles_to_update = self.frame.get(timeout = 3)
            for particle_number in particles_to_update:
                particle = self.particles[particle_number]
                with particle['lock']:
                    new_position = {'x':particle['position']['x'], 'y':particle['position']['y']}
                    for axis in new_position:
                        # Calculate time since particle was last updated
                        elapsed_time = current_time() - particle['time_of_update'][axis].value
                        # Determine if a position change is needed
                        try:
                            inverse_velocity = 1 / (particle['velocity'][axis].value + particle['acceleration'][axis].value * elapsed_time)
                        except ZeroDivisionError:
                            inverse_velocity = 0
                        if (elapsed_time >= abs(inverse_velocity)):
                            # Calculate velocity
                            particle['velocity'][axis].value = particle['velocity'][axis].value + particle['acceleration'][axis].value * elapsed_time
                            # Calculate new position
                            new_position[axis] = particle['position'][axis].value + int(elapsed_time * particle['velocity'][axis].value)

                            print('moved',int(elapsed_time * particle['velocity'][axis].value))
                            # Calculate position accuracy lost due to rounding
                            lost_position = elapsed_time * particle['velocity'][axis].value - int(elapsed_time * particle['velocity'][axis].value)
                            # Reset the timer and adjust time for loss of position
                            try:
                                particle['time_of_update'][axis].value = current_time() - lost_position / particle['velocity'][axis].value
                            except ZeroDivisionError:
                                particle['time_of_update'][axis].value = current_time()
                            # Edge bouncing
                            if not (0 <= new_position[axis] <= 999):
                                particle['velocity'][axis].value = particle['velocity'][axis].value / -1.1
                                # Teleport back inside displayed range
                                if (new_position[axis] > 500):
                                    new_position[axis] = 999
                                else:
                                    new_position[axis] = 0

                        particle['position'][axis].value = ctypes.c_int(new_position[axis])

    def terminate(self):
        print(self.name+' Exiting')
        self.exit.set()
