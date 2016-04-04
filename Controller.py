from Physics import Physics_Thread, Particle
from Output import Terminal_Output, Graphical_Output

Jacks_sweet_thread = Physics_Thread()
neat_output_thread = Graphical_Output(Jacks_sweet_thread)
input('Press enter to start')
Jacks_sweet_thread.start()
neat_output_thread.start()
# Waits for you to press enter
input('Press enter to stop')
Jacks_sweet_thread.run_signal = False
neat_output_thread.run_signal = False
