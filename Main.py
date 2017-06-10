print('Started')

number_of_particles = 10
properties = ['position','velocity','time of update','acceleration']
axes = ['x','y']
axes_size = [50,50]

window_scaling = 10
particle_color = 0xFFFFFF

number_of_properties = len(properties)
number_of_axes = len(axes)
width = axes_size[axes.index('x')]
height = axes_size[axes.index('y')]

from setproctitle import setproctitle
setproctitle('particle thingo')

print('Creating shared memory')

# Create particles in shared memory
from multiprocessing import RawArray
from numpy import frombuffer
particle_list_flat = RawArray('d', number_of_particles * number_of_axes * number_of_properties)
particle_list = frombuffer(particle_list_flat, dtype='d').reshape((number_of_particles, number_of_axes, number_of_properties))

print('Setting initial values')

# Set initial property values
from random import randint as random_integer
for particle in particle_list:
    # Set acceleration
    particle[axes.index('y')][properties.index('acceleration')] = 100
    for axis_index, axis in enumerate(axes):
        # Randomise position
        particle[axis_index][properties.index('position')] = random_integer(0,axes_size[axis_index] - 1)
        # Randomise velocity
        particle[axis_index][properties.index('velocity')] = random_integer(-1000000,1000000)/10000

print('Creating particle map')

# Create particle map
particle_map_flat = RawArray('I', width * height)
particle_map = frombuffer(particle_map_flat, dtype='I').reshape((width,height))
for particle_index, particle in enumerate(particle_list):
    x_position = int(particle[axes.index('x')][properties.index('position')])
    y_position = int(particle[axes.index('y')][properties.index('position')])
    particle_map[x_position][y_position] = particle_index + 1

print('Initialising physics threads')

# Initialise physics threads
if __name__ == "__main__":
    from Physics import Physics_Thread
    from multiprocessing import Queue, cpu_count
    physics_cpus = cpu_count() - 1 # -1 for main thread
    frame_queue = [None] * physics_cpus
    phyics_process = [None] * physics_cpus
    for cpu_core in range(physics_cpus):
        frame_queue[cpu_core] = Queue()
        phyics_process[cpu_core] = Physics_Thread(frame_queue[cpu_core], particle_list, particle_map, axes, properties)

print('Starting display')

# Initialise display
import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((width * window_scaling, height * window_scaling),HWSURFACE|DOUBLEBUF)
particle_surf = pygame.Surface((width, height))

print('Setting up main loop')

# Start physics threads
if __name__ == "__main__":
    for process in phyics_process:
        process.start()

# Setup main loop
from timeit import default_timer as current_time
from time import sleep
from numpy import where
update_interval = 1/60
running = True

input('Loaded, press enter to start main loop')

# Update the time since update to just before it starts
for particle in particle_list:
    for axis in particle:
        axis[properties.index('time of update')] = current_time()
previous_update = current_time()

# Main loop
while running:
    # Listen for window exit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Request new frame from physics processes
    for cpu_core in range(physics_cpus):
        frame_queue[cpu_core].put(list(range(round(number_of_particles/physics_cpus*(cpu_core)), round(number_of_particles/physics_cpus*(cpu_core+1)))))
    # Sleep to maintain update rate
    update_delay = update_interval - (current_time() - previous_update)
    sleep(max(0, update_delay))
    previous_update = current_time()
    # Draw particles on surface
    pygame.surfarray.blit_array(particle_surf, where(particle_map > 0, particle_color, particle_map))
    # Scale surface to fill window
    screen.blit(pygame.transform.scale(particle_surf,(width * window_scaling, height * window_scaling)), (0,0))
    # Update display
    pygame.display.flip()

# End physics threads
if __name__ == "__main__":
    for process in phyics_process:
        process.terminate()
