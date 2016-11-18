# Create particles in shared memory
number_of_particles = 1
width = 1000
height = 1000
from multiprocessing import RawArray
position = {'x':RawArray('i', number_of_particles),'y':RawArray('i', number_of_particles)}
velocity = {'x':RawArray('d', number_of_particles),'y':RawArray('d', number_of_particles)}
time_of_update = {'x':RawArray('d', number_of_particles),'y':RawArray('d', number_of_particles)}
acceleration = {'x':RawArray('d', number_of_particles),'y':RawArray('d', number_of_particles)}
# Set position
for particle in range(len(position['y'])):
    position['y'][particle] = 500
for particle in range(len(acceleration['x'])):
    position['x'][particle] = 500
# Set acceleration
for particle in range(len(acceleration['y'])):
    acceleration['y'][particle] = 98.1
for particle in range(len(acceleration['x'])):
    acceleration['x'][particle] = 0

# Initialise physics threads
frame_queue = {}
phyics_process = {}
from Physics import Physics_Thread
from multiprocessing import Queue, cpu_count
for cpu_core in range(cpu_count()):
    frame_queue[cpu_core] = Queue()
    phyics_process[cpu_core] = Physics_Thread(frame_queue[cpu_core], position, velocity, time_of_update, acceleration)

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
for axis in time_of_update:
    for particle in range(len(time_of_update[axis])):
        time_of_update[axis][particle] = current_time()
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
    pixel_array[position['x'], position['y']] = 99999999
    # Update display
    pygame.surfarray.blit_array(screen, pixel_array)
    pygame.display.flip()

# End physics threads
for process in phyics_process.values():
    process.terminate()
