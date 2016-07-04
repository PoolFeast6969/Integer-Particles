import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Start Manager (shares plane between processes)
from multiprocessing import Process, Manager
manager = Manager()
random_plane = manager.list()

# Make up some things to simulate
from Physics import Particle
from random import randint as random_integer
particle_amount = 2000
random_plane = [Particle(X_position=random_integer(1, 999), Y_position=random_integer(1, 999), X_velocity=random_integer(-10, 10), Y_velocity=random_integer(-10, 10)) for count in range(particle_amount)]
logger.info('Created plane with %s particles', particle_amount)

# Initialise the physics stuff
from Physics import World
Jacks_sweet_thread = World(random_plane)
logger.info('Initialised World')

# Initialise Window
import sys
from PyQt5.QtWidgets import QApplication
from GUI import Window
app = QApplication(sys.argv) # ????
jacks_okay_window = Window(random_plane)
logger.info('Initialised Window')

# Start things
Jacks_sweet_thread.start()
logger.info('Running Physics')
jacks_okay_window.show()
logger.info('Running window')

# ????????????
sys.exit(app.exec_()) # ??????
