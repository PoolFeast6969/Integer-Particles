from threading import Thread, Event
import numpy

class Terminal_Output (Thread):
    def __init__(self, source_thread):
        Thread.__init__(self)
        self.plane = source_thread.plane

    def run(self):
        self.run_signal = True
        print('Running ' + str( self.__class__.__name__ ))
        while self.run_signal is True:
            particle_indexs = numpy.argwhere(self.plane)
            print('\033[F\033[2K'*(len(particle_indexs)+1), end='\r')
            print('Press enter to exit')
            for particle in particle_indexs:
                position = {'x':particle[0], 'y':particle[1]}
                print(position)
