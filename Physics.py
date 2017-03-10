from timeit import default_timer as current_time
from multiprocessing import Process, Event
from time import sleep

class Physics_Thread (Process):
    """ A group of particles that do things when stuff happens"""

    def __init__(self, frame_queue, particle_list, particle_map, axes, properties):
        Process.__init__(self)
        self.exit = Event()
        self.frame = frame_queue
        self.particle_list = particle_list
        self.particle_map = particle_map
        self.axes = axes
        self.properties = properties
        print(self.name+' Initialised')

    def run(self):
        while not self.exit.is_set():
            particles_to_update = self.frame.get(timeout = 3)
            for particle_index in particles_to_update:
                axis_to_update = []
                for axis in self.particle_list[particle_index]:
                    # Calculate time since particle was last updated
                    elapsed_time = current_time() - axis[self.properties.index('time of update')]
                    # Determine if a position change is needed
                    try:
                        inverse_velocity = 1 / (axis[self.properties.index('velocity')] + axis[self.properties.index('acceleration')] * elapsed_time)
                    except ZeroDivisionError:
                        inverse_velocity = 0
                    if (elapsed_time >= abs(inverse_velocity)):
                        axis_to_update.append(True)
                    else:
                        axis_to_update.append(False)

                if any(axis_to_update):
                    new_position = [None] * len(self.axes)
                    # Calculate potential new position
                    for axis_index, update_required in enumerate(axis_to_update):
                        # Less spaghetti
                        axis = self.particle_list[particle_index][axis_index]
                        if update_required:
                            # Calculate acceleration toward center
                            # axis[self.properties.index('acceleration')] = (axis[self.properties.index('position')] - 500) * -2
                            # Get elapsed_time
                            elapsed_time = current_time() - axis[self.properties.index('time of update')]
                            # Calculate velocity
                            axis[self.properties.index('velocity')] = axis[self.properties.index('velocity')] + axis[self.properties.index('acceleration')] * elapsed_time
                            # Calculate new position
                            proposed_position = axis[self.properties.index('position')] + int(elapsed_time * axis[self.properties.index('velocity')])
                            # Calculate position accuracy lost due to rounding
                            lost_position = elapsed_time * axis[self.properties.index('velocity')] - int(elapsed_time * axis[self.properties.index('velocity')])
                            # Reset the timer and adjust time for loss of position
                            try:
                                axis[self.properties.index('time of update')] = current_time() - lost_position / axis[self.properties.index('velocity')]
                            except ZeroDivisionError:
                                axis[self.properties.index('time of update')] = current_time()
                            # Edge bouncing
                            if not (0 <= proposed_position <= 999):
                                axis[self.properties.index('velocity')] = axis[self.properties.index('velocity')]/-1.9
                                # Teleport back inside displayed range
                                if (proposed_position > 500):
                                    proposed_position = 999
                                else:
                                    proposed_position = 0
                            # Record new position
                            new_position[axis_index] = proposed_position
                        else:
                            # Keep same position
                            new_position[axis_index] = axis[self.properties.index('position')]

                    # Determine positions crossed to reach new position
                    final_x = new_position[self.axes.index('x')]
                    final_y = new_position[self.axes.index('y')]
                    initial_x = self.particle_list[particle_index][self.axes.index('x')][self.properties.index('position')]
                    initial_y = self.particle_list[particle_index][self.axes.index('y')][self.properties.index('position')]
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
                            positions_traversed.append({'x':x,'y':y})
                    else:
                        error = change_in_y / 2
                        while y != final_y:
                            error -= change_in_x
                            if error < 0:
                                x += sx
                                error += change_in_y
                            y += sy
                            positions_traversed.append({'x':x,'y':y})

                    # Check for collisions
                    for position_traversed in positions_traversed:
                        collided_particle_index = self.particle_map[int(position_traversed['x'])][int(position_traversed['y'])]
                        if collided_particle_index != 0:
                            for axis in self.particle_list[collided_particle_index]:
                                axis[self.properties.index('velocity')] = -axis[self.properties.index('velocity')]
                                print('oh shit')



                    # Update map
                    self.particle_map[int(self.particle_list[particle_index][self.axes.index('x')][self.properties.index('position')])][int(self.particle_list[particle_index][self.axes.index('y')][self.properties.index('position')])] = 0
                    self.particle_map[int(new_position[self.axes.index('x')])][int(new_position[self.axes.index('y')])] = particle_index
                    # Update list
                    for axis_index, update_required in enumerate(axis_to_update):
                        self.particle_list[particle_index][axis_index][self.properties.index('position')] = new_position[axis_index]



    def terminate(self):
        print(self.name+' Exiting')
        self.exit.set()
