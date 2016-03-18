from Physics import Physics_Thread, Particle
from Output import Terminal_Output

Jacks_sweet_thread = Physics_Thread()
Jacks_sweet_thread.start()
neat_output_thread = Terminal_Output(Jacks_sweet_thread)
neat_output_thread.start()
# Waits for you to press enter
input()
Jacks_sweet_thread.run_signal = False
neat_output_thread.run_signal = False
