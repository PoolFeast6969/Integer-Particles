from timeit import default_timer as current_time
from multiprocessing import Process
from numpy import sign

class Physics_Thread (Process):
    """A process of particles"""

    def __init__(self, frame_queue, particle_list, particle_map, axes, indexs):
        Process.__init__(self)
        self.daemon = True
        self.frame = frame_queue
        self.particle_list = particle_list
        self.particle_map = particle_map
        self.axes = axes
        self.indexs = indexs
        self.size = [particle_map.shape[0] -1, particle_map.shape[1] -1]

    def run(self):
        print(self.name+' ready')
        # Less spag bowl (and great variable naming)
        i = self.indexs

        particles_to_update = self.frame.get()

        while particles_to_update is not None:
            for particle_index in particles_to_update:
                # Check to see if the position would have changed, and the particle should be updated
                axis_to_update = []
                for particle_axis in self.particle_list[particle_index]:
                    # Calculate time since particle was last updated
                    elapsed_time = current_time() - particle_axis[i['time of update']]
                    # Determine if a position change is needed
                    try:
                        inverse_velocity = 1 / (particle_axis[i['velocity']] + particle_axis[i['acceleration']] * elapsed_time)
                    except ZeroDivisionError:
                        inverse_velocity = 0
                    # Determine which axis needs to be updated
                    axis_to_update.append(elapsed_time >= abs(inverse_velocity))

                if any(axis_to_update):
                    move_distance = axis_to_update
                    # Calculate potential new distance
                    for axis_index, update_required in enumerate(axis_to_update):
                        particle_axis = self.particle_list[particle_index][axis_index] # Less spaghetti
                        if update_required:
                            # Calculate acceleration toward center sometimes
                            particle_axis[i['acceleration']] = 2*((self.size[axis_index]+1)/2 - particle_axis[i['position']])
                            # Get elapsed_time
                            elapsed_time = current_time() - particle_axis[i['time of update']]
                            # Calculate velocity
                            particle_axis[i['velocity']] = particle_axis[i['velocity']] + particle_axis[i['acceleration']] * elapsed_time
                            # Calculate new position
                            move_distance[axis_index] = elapsed_time * particle_axis[i['velocity']]
                            # Calculate position accuracy lost due to rounding
                            lost_position = int(move_distance[axis_index]) - move_distance[axis_index]
                            # Reset the timer and adjust time for loss of position
                            try:
                                particle_axis[i['time of update']] = current_time() + lost_position / particle_axis[i['velocity']]
                            except ZeroDivisionError:
                                particle_axis[i['time of update']] = current_time()

                    # Determine positions crossed to reach new position
                    final = [int(move_distance[i['x']]),int(move_distance[i['y']])]
                    coord = [0,0]
                    if 0 in final:
                        slope = [0,0]
                    else:
                        slope = [final[1]/final[0],final[0]/final[1]]
                    lmao = 0 if abs(final[1]) < abs(final[0]) else 1
                    move_distance = [0,0]
                    # Check each coordinate for an obstruction
                    while coord[lmao] != final[lmao]:
                        coord[lmao] += sign(final[lmao])
                        previous_point = move_distance
                        move_distance = [coord[lmao],int(slope[lmao] * coord[lmao])] if lmao is 0 else [int(slope[lmao] * coord[lmao]),coord[lmao]]
                        # Check for inteferance with walls
                        for axis_index in range(len(move_distance)):
                            if not(0 <= self.particle_list[particle_index][axis_index][i['position']] + move_distance[axis_index] <= self.size[axis_index]):
                                # Reverse direction
                                self.particle_list[particle_index][axis_index][i['velocity']] = -self.particle_list[particle_index][axis_index][i['velocity']]
                                # Move back inside wall range
                                move_distance[axis_index] = previous_point[axis_index]
                                # Stop checking coordinates
                                final[lmao] = coord[lmao]
                        if final[lmao] is not coord[lmao]:
                            # Check for collisions with particles
                            hit_particle = self.particle_map[int(self.particle_list[particle_index][i['x']][i['position']] + move_distance[i['x']]), int(self.particle_list[particle_index][i['y']][i['position']] + move_distance[i['y']])]
                            if hit_particle > 0 and hit_particle-1 != particle_index:
                                # Swap velocities
                                self.particle_list[hit_particle - 1][axis_index][i['velocity']], self.particle_list[particle_index][axis_index][i['velocity']] = self.particle_list[particle_index][axis_index][i['velocity']], self.particle_list[hit_particle - 1][axis_index][i['velocity']]
                                # Move back one point
                                move_distance = previous_point
                                # Stop checking coordinates
                                final[lmao] = coord[lmao]
                        # Create a debug particle to show where it's checking
                        self.particle_map[int(self.particle_list[particle_index][i['x']][i['position']] + move_distance[i['x']]), int(self.particle_list[particle_index][i['y']][i['position']] + move_distance[i['y']])] = -1
                    # Adjust for lost time
                    for axis_index, particle_axis in enumerate(final):
                        self.particle_list[particle_index][axis_index][i['time of update']] = self.particle_list[particle_index][axis_index][i['time of update']] + abs(particle_axis - move_distance[axis_index]) / abs(self.particle_list[particle_index][axis_index][i['velocity']])
                    # Update map
                    self.particle_map[int(self.particle_list[particle_index][i['x']][i['position']])][int(self.particle_list[particle_index][i['y']][i['position']])] = 0
                    self.particle_map[int(self.particle_list[particle_index][i['x']][i['position']] + int(move_distance[i['x']]))][int(self.particle_list[particle_index][i['y']][i['position']] + int(move_distance[i['y']]))] = particle_index + 1
                    # Update list
                    for axis_index, update_required in enumerate(final):
                        self.particle_list[particle_index][axis_index][i['position']] = self.particle_list[particle_index][axis_index][i['position']] + int(move_distance[axis_index])
            particles_to_update = self.frame.get()

    def terminate(self):
        print(self.name+' Exiting')
        self.frame.put(None)
