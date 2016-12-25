print('Loading..')

number_of_particles = 200
properties = ['position','velocity','time of update','acceleration']
number_of_properties = len(properties)
axes = ['x','y']
number_of_axes = len(axes)
width = 1000
height = 1000

# Create particles in shared memory
from multiprocessing import RawArray
from numpy import frombuffer
particle_array_flat = RawArray('d', number_of_particles * number_of_axes * number_of_properties)
particles = frombuffer(particle_array_flat).reshape((number_of_particles, number_of_axes, number_of_properties))

# Set initial property values
from random import randint as random_integer
for particle in particles:
    # Set acceleration
    particle[axes.index('y')][properties.index('acceleration')] = 98.1
    for axis in particle:
        # Randomise position
        axis[properties.index('position')] = random_integer(0,999)
        # Randomise velocity
        axis[properties.index('velocity')] = random_integer(-100000,100000)/100

# Initialise physics threads
from Physics import Physics_Thread
from multiprocessing import Queue, cpu_count
frame_queue = {}
phyics_process = {}
for cpu_core in range(cpu_count()):
    frame_queue[cpu_core] = Queue()
    phyics_process[cpu_core] = Physics_Thread(frame_queue[cpu_core], particles, axes, properties)

# Initialise display
import pygame
pygame.init()
screen = pygame.display.set_mode((width, height))

print('Loading Finished')

# Start physics threads
for process in phyics_process.values():
    process.start()

# Start the physics loops
from numpy import empty, copy
from timeit import default_timer as current_time
from time import sleep
update_interval = 1/60
running = True
blank_array = empty((width,height))
# Update the time since update to just before it starts
for particle in particles:
    for axis in particle:
        axis[properties.index('time of update')] = current_time()
previous_update = current_time()

# Main loop
while running:
    # Listen for exit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Request new frame
    for cpu_core in range(cpu_count()):
        frame_queue[cpu_core].put(list(range(round(number_of_particles/cpu_count()*(cpu_core)), round(number_of_particles/cpu_count()*(cpu_core+1)))))
    # Sleep to maintain update rate
    update_delay = update_interval - (current_time() - previous_update)
    previous_update = current_time()
    sleep(max(0, update_delay))
    # Add to pygame display array
    pixel_array = copy(blank_array)
    for particle in particles:
        pixel_array[particle[axes.index('x')][properties.index('position')], particle[axes.index('y')][properties.index('position')]] = 99999999
    # Update display
    pygame.surfarray.blit_array(screen, pixel_array)
    pygame.display.flip()

# End physics threads
for process in phyics_process.values():
    process.terminate()
