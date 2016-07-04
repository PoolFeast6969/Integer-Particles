from timeit import default_timer as current_time
from time import sleep

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtOpenGL import QGLWidget

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Window(QGLWidget):
    def __init__(self, plane, update_rate=10):
        super().__init__()
        self.setWindowTitle('nice job')
        self.resize(1000, 1000)
        self.plane = plane
        self.update_interval = 1/update_rate
        logger.info('Initialised Window')

    def paintEvent(self, event):
        logger.info('Redrew Window')
        painter = QPainter()
        painter.begin(self)
        painter.setPen(Qt.black)
        self.run(painter)
        painter.end()

    def run(self, painter):
        #previous_update = current_time()
        # Render each particle
        for particle in self.plane:
            painter.drawPoint(particle.position['x'], particle.position['y'])
        # Sleep to maintain update rate
        #update_delay = previous_update + self.update_interval - current_time()
        #previous_update = current_time()
        #sleep(max(0, update_delay))
