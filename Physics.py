from timeit import default_timer as current_time
from multiprocessing import Process, Event
from time import sleep

class Physics_Thread (Process):
    """ A group of particles"""

    def __init__(self, frame_queue, position, velocity, time_of_update, acceleration):
        Process.__init__(self)
        self.exit = Event()
        self.frame = frame_queue
        self.position = position
        self.velocity = velocity
        self.time_of_update = time_of_update
        self.acceleration = acceleration
        print(self.name+' Initialised')

    def run(self):
        while not self.exit.is_set():
            particles_to_update = self.frame.get(timeout = 3)
            for particle in particles_to_update:
                new_position = {'x':self.position['x'][particle],'y':self.position['y'][particle]}
                for axis in self.position:
                    # Calculate time since particle was last updated
                    elapsed_time = current_time() - self.time_of_update[axis][particle]
                    # Determine if a position change is needed
                    try:
                        inverse_velocity = 1 / (self.velocity[axis][particle] + self.acceleration[axis][particle] * elapsed_time)
                    except ZeroDivisionError:
                        inverse_velocity = 0
                    if (elapsed_time >= abs(inverse_velocity)):
                        # Calculate velocity
                        self.velocity[axis][particle] = self.velocity[axis][particle] + self.acceleration[axis][particle] * elapsed_time
                        # Calculate new position
                        new_position[axis] = self.position[axis][particle] + int(elapsed_time * self.velocity[axis][particle])
                        # Calculate position accuracy lost due to rounding
                        lost_position = elapsed_time * self.velocity[axis][particle] - int(elapsed_time * self.velocity[axis][particle])
                        # Reset the timer and adjust time for loss of position
                        try:
                            self.time_of_update[axis][particle] = current_time() - lost_position / self.velocity[axis][particle]
                        except ZeroDivisionError:
                            self.time_of_update[axis][particle] = current_time()
                        # Edge bouncing
                        if not (0 <= new_position[axis] <= 999):
                            self.velocity[axis][particle] = self.velocity[axis][particle]/-1.1
                            # Teleport back inside displayed range
                            if (new_position[axis] > 500):
                                new_position[axis] = 999
                            else:
                                new_position[axis] = 0

                # Collision detection
                if (new_position['x'] != self.position['x'][particle]) or (new_position['y'] != self.position['y'][particle]):
                    # Determine positions crossed to reach new position
                    final_x = new_position['x']
                    final_y = new_position['y']
                    initial_x = self.position['x'][particle]
                    initial_y = self.position['y'][particle]
                    change_in_x = abs(final_x - initial_x)
                    change_in_y = abs(final_y - initial_y)
                    x, y = initial_x, initial_y
                    sx = -1 if initial_x > final_x else 1
                    sy = -1 if initial_y > final_y else 1
                    positions_traversed = []
                    if change_in_x > change_in_y:
                        error = change_in_x / 2
                        while x != final_x:
                            error -= change_in_y
                            if error < 0:
                                y += sy
                                error += change_in_x
                            x += sx
                            positions_traversed.append([x, y])
                    else:
                        error = change_in_y / 2
                        while y != final_y:
                            error -= change_in_x
                            if error < 0:
                                x += sx
                                error += change_in_y
                            y += sy
                            positions_traversed.append([x, y])
                    # Check those positions for stuff
                    for position in positions_traversed:
                        print(position)



    def terminate(self):
        print(self.name+' Exiting')
        self.exit.set()
