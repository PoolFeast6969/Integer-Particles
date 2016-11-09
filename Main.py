# Create particles in shared memory
number_of_particles = 10
width = 1000
height = 1000
from multiprocessing import RawArray
position = {'x':RawArray('i', number_of_particles),'y':RawArray('i', number_of_particles)}
velocity = {'x':RawArray('f', number_of_particles),'y':RawArray('f', number_of_particles)}
time_since_update = {'x':RawArray('f', number_of_particles),'y':RawArray('f', number_of_particles)}

# Initialise physics threads
frame_queue = {}
phyics_process = {}
from Physics import Physics_Thread
from multiprocessing import Queue, cpu_count
for cpu_core in range(cpu_count()):
    frame_queue[cpu_core] = Queue()
    phyics_process[cpu_core] = Physics_Thread(frame_queue[cpu_core], position, velocity, time_since_update)

# Start physics threads
for process in phyics_process.values():
    process.start()

# Start displayed
import pygame
pygame.init()
screen = pygame.display.set_mode((width, height))

# Main loop
import numpy as np
from timeit import default_timer as current_time
from time import sleep
update_interval = 1/60
running = True
blank_array = np.empty((width,height))
previous_update = current_time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Request new frame
    for frame_que in frame_queue.values():
        frame_que.put(list(range(10)))

    # Add to pygame array
    pixel_array = blank_array
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
