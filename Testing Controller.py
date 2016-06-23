from multiprocessing import Process, Pipe
from Physics import Simulation, Particle
from Output import Terminal_Output, Graphical_Output
from random import randint as random_integer

# Make up some shit to simulate
random_plane = [Particle(X_position=random_integer(10, 999), Y_position=count, X_velocity=random_integer(-10, 10), Y_velocity=random_integer(-10, 10)) for count in range(29)]
print(random_plane)


Jacks_sweet_thread = Simulation(random_plane)
input('Press enter to start')
Jacks_sweet_thread.start()
# Waits for you to press enter
input('Press enter to stop')
Jacks_sweet_thread.terminate()
