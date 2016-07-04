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

# Initialise Window
import sys
from PyQt5.QtWidgets import QApplication
from GUI import Window
app = QApplication(sys.argv) # ????
window = Window(random_plane)

# Start things
Jacks_sweet_thread.start()
window.show()

# ????????????
sys.exit(app.exec_()) # ??????
