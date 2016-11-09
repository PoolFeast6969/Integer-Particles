from timeit import default_timer as current_time
from multiprocessing import Process, Event
from time import sleep

class Physics_Thread (Process):
    """ A group of particles"""

    def __init__(self, frame_queue, position, velocity, time_since_update):
        Process.__init__(self)
        self.exit = Event()
        self.frame = frame_queue
        self.position = position
        self.velocity = velocity
        self.time_since_update = time_since_update
        print(self.name+' Initialised')

    def run(self):
        for axis in self.time_since_update:
            for particle in self.time_since_update[axis]:
                particle = current_time()
        print(self.time_since_update['x'][:])
        while not self.exit.is_set():
            particles_to_update = self.frame.get()
            for particle in particles_to_update:
                        for axis in self.position:
                            # Calculate time since particle was last updated
                            elapsed_time = current_time() - self.time_since_update[axis][particle]
                            # Determine if a position change is needed
                            try:
                                inverse_velocity = 1 / (self.velocity[axis][particle] + 9.81 * elapsed_time)
                            except ZeroDivisionError:
                                inverse_velocity = 0
                            if (elapsed_time >= abs(inverse_velocity)):
                                # Calculate velocity
                                self.velocity[axis][particle] = self.velocity[axis][particle] + 9.81 * elapsed_time
                                # Edge bouncing
                                if not (0 <= self.position[axis][particle] <= 1000):
                                    self.velocity[axis][particle] = -self.velocity[axis][particle]/1.1
                                    # Teleport back inside displayed range
                                    if (self.position[axis][particle] > 500):
                                        self.position[axis][particle] = 1000
                                    else:
                                        self.position[axis][particle] = 0
                                # Move to new position
                                self.position[axis][particle] = self.position[axis][particle] + int(elapsed_time * self.velocity[axis][particle])
                                # Calculate position accuracy lost due to rounding
                                lost_position = elapsed_time * self.velocity[axis][particle] - int(elapsed_time * self.velocity[axis][particle])
                                # Reset the timer and adjust time for loss of position
                                self.time_since_update[axis][particle] = current_time() - lost_position / self.velocity[axis][particle]

    def terminate(self):
        print(self.name+' Exiting')
        self.exit.set()
