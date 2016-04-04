from threading import Thread, Event
import numpy
from vispy import gloo, app
from vispy.gloo import Program
import math
from vispy.color import Color


class Terminal_Output (Thread):
    def __init__(self, source_thread):
        Thread.__init__(self)
        self.plane = source_thread.plane

    def run(self):
        self.run_signal = True
        print('Running ' + str( self.__class__.__name__ ))
        while self.run_signal is True:
            particle_indexs = numpy.argwhere(self.plane)
            #print('\033[F\033[2K'*(len(particle_indexs)+1), end='\r')
            print('Press enter to exit')
            for particle in particle_indexs:
                position = {'x':particle[0], 'y':particle[1]}
                print(position)

class Graphical_Output (Thread):
    def __init__(self, source_thread):
        Thread.__init__(self)
        self.plane = source_thread.plane

    def run(self):
        self.run_signal = True
        print('Running ' + str( self.__class__.__name__ ))

        #class Particle (gloo.Texture2D):

        class Canvas (app.Canvas):
            def __init__(self, *args, **kwargs):
                app.Canvas.__init__(self, *args, **kwargs)
                self._timer = app.Timer('auto', connect=self.on_timer, start=True)
                self.color = 'white'

            def on_draw(self, event):
                gloo.clear(color=True)

            def on_timer(self, event):
                # Animation speed based on global time.
                t = event.elapsed
                c = Color(self.color).rgb
                # Simple sinusoid wave animation.
                s = abs(0.5 + 0.5 * math.sin(t))
                gloo.set_clear_color((c[0] * s, c[1] * s, c[2] * s, 1))
                self.update()
        # You should run this demo as main with ipython -i <file>.  If interactive
        # mode is not specified, this demo will exit immediately because this demo
        # doesn't call run and relies on the input hook being setup.
        if __name__ == '__main__':
            # app.use_app('glfw')  # for testing specific backends
            app.set_interactive()


        # All variables listed in this scope are accessible via the console.
        canvas = Canvas(keys='interactive')
        canvas.show()
