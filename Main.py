# Create particles in shared memory
number_of_particles = 100000
width = 1000
height = 1000
from multiprocessing import RawArray
position = {'x':RawArray('i', number_of_particles),'y':RawArray('i', number_of_particles)}
velocity = {'x':RawArray('d', number_of_particles),'y':RawArray('d', number_of_particles)}
time_since_update = {'x':RawArray('d', number_of_particles),'y':RawArray('d', number_of_particles)}
acceleration = {'x':RawArray('d', number_of_particles),'y':RawArray('d', number_of_particles)}
# Set acceleration
for particle in range(len(acceleration['y'])):
    acceleration['y'][particle] = 9.81
for particle in range(len(acceleration['x'])):
    acceleration['x'][particle] = 0
# Randomise sideways velocity
from random import randint as random_integer
for particle in range(len(velocity['x'])):
    velocity['x'][particle] = random_integer(-1000,1000)

# Initialise physics threads
frame_queue = {}
phyics_process = {}
from Physics import Physics_Thread
from multiprocessing import Queue, cpu_count
for cpu_core in range(cpu_count()):
    frame_queue[cpu_core] = Queue()
    phyics_process[cpu_core] = Physics_Thread(frame_queue[cpu_core], position, velocity, time_since_update, acceleration)

# Initialise display
import pygame
pygame.init()
screen = pygame.display.set_mode((width, height))

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
for axis in time_since_update:
    for particle in range(len(time_since_update[axis])):
        time_since_update[axis][particle] = current_time()
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
    # Add to pygame array
    pixel_array = copy(blank_array)
    pixel_array[position['x'], position['y']] = 6000000
    # Update display
    pygame.surfarray.blit_array(screen, pixel_array)
    pygame.display.flip()
    # Sleep to maintain update rate
    update_delay = update_interval - (current_time() - previous_update)
    previous_update = current_time()
    sleep(max(0, update_delay))

# End physics threads
for process in phyics_process.values():
    process.terminate()
