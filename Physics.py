from timeit import default_timer as current_time
from multiprocessing import Process
from time import sleep
from os import getpid
from setproctitle import setproctitle

class Physics_Thread (Process):
    """ A process of particles that do things when stuff happens"""

    def __init__(self, frame_queue, particle_list, particle_map, axes, indexs):
        Process.__init__(self)
        self.daemon = True
        self.frame = frame_queue
        self.particle_list = particle_list
        self.particle_map = particle_map
        self.axes = axes
        self.indexs = indexs
        self.size = [particle_map.shape[0], particle_map.shape[1]]

    def run(self):
        setproctitle(self.name)
        print(self.name+' ready')

        i = self.indexs # Less spag bowl

        particles_to_update = self.frame.get()

        while particles_to_update is not None:
            for particle_index in particles_to_update:
                axis_to_update = []
                for particle_axis in self.particle_list[particle_index]:
                    # Calculate time since particle was last updated
                    elapsed_time = current_time() - particle_axis[i['time of update']]
                    # Determine if a position change is needed
                    try:
                        inverse_velocity = 1 / (particle_axis[i['velocity']] + particle_axis[i['acceleration']] * elapsed_time)
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
                        particle_axis = self.particle_list[particle_index][axis_index] # Less spaghetti
                        if update_required:
                            # Calculate acceleration toward center sometimes
                            #particle_axis[i['acceleration']] = (particle_axis[i['position']] - self.size[axis_index]/2) * -2
                            # Get elapsed_time
                            elapsed_time = current_time() - particle_axis[i['time of update']]
                            # Calculate velocity
                            particle_axis[i['velocity']] = particle_axis[i['velocity']] + particle_axis[i['acceleration']] * elapsed_time
                            # Calculate new position
                            move_distance = elapsed_time * particle_axis[i['velocity']]
                            # Calculate position accuracy lost due to rounding
                            lost_position =  int(move_distance) - move_distance
                            # Reset the timer and adjust time for loss of position
                            try:
                                particle_axis[i['time of update']] = current_time() + lost_position / particle_axis[i['velocity']]
                            except ZeroDivisionError:
                                particle_axis[i['time of update']] = current_time()
                            proposed_position = particle_axis[i['position']] + int(move_distance)
                            # Edge bouncing
                            if not (0 <= proposed_position <= self.size[axis_index] -1):
                                particle_axis[i['velocity']] = -particle_axis[i['velocity']]/1.1
                                # Teleport back inside displayed range
                                if (proposed_position > self.size[axis_index]/2):
                                    proposed_position = self.size[axis_index] -1
                                else:
                                    proposed_position = 0
                            # Record new position
                            new_position[axis_index] = proposed_position
                        else:
                            # Keep same position
                            new_position[axis_index] = particle_axis[i['position']]

                    # Determine positions crossed to reach new position
                    final_x = new_position[i['x']]
                    final_y = new_position[i['y']]
                    initial_x = self.particle_list[particle_index][i['x']][i['position']]
                    initial_y = self.particle_list[particle_index][i['y']][i['position']]
                    change_in_x = abs(final_x - initial_x)
                    change_in_y = abs(final_y - initial_y)
                    x, y = initial_x, initial_y
                    sx = -1 if initial_x > final_x else 1
                    sy = -1 if initial_y > final_y else 1
                    positions_traversed = []
                    if change_in_x > change_in_y:
                        error = change_in_x / 2
                        while x != final_x:
                            previous_x = x
                            previous_y = y
                            error -= change_in_y
                            if error < 0:
                                y += sy
                                error += change_in_x
                            x += sx
                            # Check for collisions
                            collided_particle_index = self.particle_map[int(x)][int(y)]
                            if (collided_particle_index != 0) and (collided_particle_index != particle_index + 1):
                                for axis_index, particle_axis in enumerate(self.particle_list[collided_particle_index - 1]):
                                    particle_axis[i['velocity']],self.particle_list[particle_index][axis_index][i['velocity']] = self.particle_list[particle_index][axis_index][i['velocity']]/1.1, particle_axis[i['velocity']]/1.1
                                    new_position[axis_index] = [previous_x, previous_y][axis_index]
                                    #print('oh shit')
                                    #http://vobarian.com/collisions/2dcollisions2.pdf
                                break
                    else:
                        error = change_in_y / 2
                        while y != final_y:
                            previous_x = x
                            previous_y = y
                            error -= change_in_x
                            if error < 0:
                                x += sx
                                error += change_in_y
                            y += sy
                            # Check for collisions
                            collided_particle_index = self.particle_map[int(x)][int(y)]
                            if (collided_particle_index != 0) and (collided_particle_index != particle_index + 1):
                                for axis_index, particle_axis in enumerate(self.particle_list[collided_particle_index - 1]):
                                    particle_axis[i['velocity']],self.particle_list[particle_index][axis_index][i['velocity']] = self.particle_list[particle_index][axis_index][i['velocity']]/1.1, particle_axis[i['velocity']]/1.1
                                    new_position[axis_index] = [previous_x, previous_y][axis_index]
                                    #print('oh shit')
                                    #http://vobarian.com/collisions/2dcollisions2.pdf
                                break

                    # Update arrays with the new position
                    # Update map
                    self.particle_map[int(self.particle_list[particle_index][i['x']][i['position']])][int(self.particle_list[particle_index][i['y']][i['position']])] = 0
                    self.particle_map[int(new_position[i['x']])][int(new_position[i['y']])] = particle_index + 1
                    # Update list
                    for axis_index, update_required in enumerate(axis_to_update):
                        self.particle_list[particle_index][axis_index][i['position']] = new_position[axis_index]
            particles_to_update = self.frame.get()

    def terminate(self):
        print(self.name+' Exiting')
        self.frame.put(None)
