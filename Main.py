# Create particles in shared memory
number_of_particles = 1000
width = 1000
height = 1000
from multiprocessing import RawValue, Lock
from random import randint as random_integer
particles = [None]*number_of_particles
for particle_number in range(number_of_particles):
    velocity = {'x':RawValue('f',random_integer(-100000,100000)/100),'y':RawValue('f',random_integer(-100000,100000)/100)}
    position = {'x':RawValue('i',random_integer(0,height-1)),'y':RawValue('i',random_integer(0,width-1))}

    acceleration = {'x':RawValue('f', 0),'y':RawValue('f',98.1)}
    time_of_update = {'x':RawValue('f'),'y':RawValue('f')}

    lock = Lock()

    particles[particle_number] = {'velocity':velocity, 'position':position, 'acceleration':acceleration, 'time_of_update':time_of_update, 'lock':lock}

# Initialise physics threads
from Physics import Physics_Thread
from multiprocessing import Queue, cpu_count
frame_queue = {}
phyics_process = {}
for cpu_core in range(cpu_count()):
    frame_queue[cpu_core] = Queue()
    phyics_process[cpu_core] = Physics_Thread(frame_queue[cpu_core], particles)

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
for particle in particles:
    for axis in time_of_update:
        particle['time_of_update'][axis] = current_time()
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
        pixel_array[particle['position']['x'], particle['position']['y']] = 99999999
    # Update display
    pygame.surfarray.blit_array(screen, pixel_array)
    pygame.display.flip()

# End physics threads
for process in phyics_process.values():
    process.terminate()
