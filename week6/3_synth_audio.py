from pyo import *
import time

s = Server().boot()
a = Sine(440, 0, 0.1).out()

s.start()
time.sleep(1)
s.stop()

print("finished")