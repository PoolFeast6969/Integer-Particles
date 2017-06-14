from timeit import default_timer as current_time
from multiprocessing import Process
from setproctitle import setproctitle
from numpy import sign

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
        self.size = [particle_map.shape[0] -1, particle_map.shape[1] -1]

    def run(self):
        setproctitle(self.name)
        print(self.name+' ready')

        i = self.indexs # Less spag bowl (and great variable naming)

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
                    # Determine which axis needs to be updated
                    if (elapsed_time >= abs(inverse_velocity)):
                        axis_to_update.append(True)
                    else:
                        axis_to_update.append(False)

                if any(axis_to_update):
                    move_distance = [0] * len(self.axes)
                    # Calculate potential new distance
                    for axis_index, update_required in enumerate(axis_to_update):
                        particle_axis = self.particle_list[particle_index][axis_index] # Less spaghetti
                        if update_required:
                            # Calculate acceleration toward center sometimes
                            #particle_axis[i['acceleration']] = (particle_axis[i['position']] + self.size[axis_index]/2) * -2
                            # Get elapsed_time
                            elapsed_time = current_time() - particle_axis[i['time of update']]
                            # Calculate velocity
                            particle_axis[i['velocity']] = particle_axis[i['velocity']] + particle_axis[i['acceleration']] * elapsed_time
                            # Calculate new position
                            move_distance[axis_index] = elapsed_time * particle_axis[i['velocity']]
                            # Calculate position accuracy lost due to rounding
                            lost_position =  int(move_distance[axis_index]) - move_distance[axis_index]
                            # Reset the timer and adjust time for loss of position
                            try:
                                particle_axis[i['time of update']] = current_time() + lost_position / particle_axis[i['velocity']]
                            except ZeroDivisionError:
                                particle_axis[i['time of update']] = current_time()

                    # Determine positions crossed to reach new position
                    # https://www.cs.helsinki.fi/group/goa/mallinnus/lines/bresenh.html
                    final = {'x':int(move_distance[i['x']]),'y':int(move_distance[i['y']])}
                    coord = {'x':0,'y':0}
                    try:
                        bleh = final['y']/final['x']
                    except ZeroDivisionError:
                        bleh = 0
                    try:
                        blarg = final['x']/final['y']
                    except ZeroDivisionError:
                        blarg = 0
                    slope = {'x':bleh,'y':blarg}
                    lmao = 'x' if abs(final['y']) < abs(final['x']) else 'y'
                    point = [0,0]
                    while coord[lmao] != final[lmao]:
                        coord[lmao] += sign(final[lmao])
                        previous_point = point
                        point = [coord[lmao],int(slope[lmao] * coord[lmao])] if abs(final['y']) < abs(final['x']) else [int(slope[lmao] * coord[lmao]),coord[lmao]]
                        for axis_index,point_axis in enumerate(point):
                            if not(0 <= point_axis + self.particle_list[particle_index][axis_index][i['position']] <= self.size[axis_index]):
                                self.particle_list[particle_index][axis_index][i['velocity']] = -self.particle_list[particle_index][axis_index][i['velocity']]/1.1
                                # Teleport back inside displayed range
                                if not(0 <= previous_point[axis_index] + self.particle_list[particle_index][axis_index][i['position']] <= self.size[axis_index]):
                                    print('ohhhhhhh shit')
                                move_distance[axis_index] = previous_point[axis_index]
                                final[lmao] = coord[lmao]

                    # Update map
                    self.particle_map[int(self.particle_list[particle_index][i['x']][i['position']])][int(self.particle_list[particle_index][i['y']][i['position']])] = 0
                    self.particle_map[int(self.particle_list[particle_index][i['x']][i['position']] + int(move_distance[i['x']]))][int(self.particle_list[particle_index][i['y']][i['position']] + int(move_distance[i['y']]))] = particle_index + 1
                    # Update list
                    for axis_index, update_required in enumerate(axis_to_update):
                        self.particle_list[particle_index][axis_index][i['position']] = self.particle_list[particle_index][axis_index][i['position']] + int(move_distance[axis_index])
            particles_to_update = self.frame.get()

    def terminate(self):
        print(self.name+' Exiting')
        self.frame.put(None)
