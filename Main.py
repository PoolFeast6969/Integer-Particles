if __name__ == "__main__":
    print('Started')

    number_of_particles = 10000
    properties = ['position','velocity','time of update','acceleration']
    axes = ['x','y']
    axes_size = [200,50]
    scaling = 5

    number_of_properties = len(properties)
    number_of_axes = len(axes)
    width = axes_size[axes.index('x')]
    height = axes_size[axes.index('y')]

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
        particle_map[x_position][y_position] = particle_index

    print('Initialising physics threads')

    # Initialise physics threads
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
    screen = pygame.display.set_mode((width * scaling, height * scaling),HWSURFACE|DOUBLEBUF)

    input('Loaded, press enter to continue')

    # Start physics threads
    for process in phyics_process:
        process.start()

    # Setup main loop
    from timeit import default_timer as current_time
    from time import sleep
    update_interval = 1/60
    running = True

    # Update the time since update to just before it starts
    for particle in particle_list:
        for axis in particle:
            axis[properties.index('time of update')] = current_time()
    previous_update = current_time()

    # Main loop
    while running:
        # Listen for exit button
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
        # Clear screen
        screen.fill(pygame.Color('black'))
        # Draw particles on screen
        for particle in particle_list:
            screen.set_at((int(particle[axes.index('x')][properties.index('position')]), int(particle[axes.index('y')][properties.index('position')])), pygame.Color('white'))
        screen.blit(pygame.transform.scale(screen,(width * scaling**2, height * scaling**2)), (0,0))
        pygame.display.flip()

    # End physics threads
    for process in phyics_process.values():
        process.terminate()
