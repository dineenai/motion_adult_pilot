# import random
# import pandas as pd

from datetime import datetime, timedelta

import time

# from psychopy import event, visual, core
# from psychopy.constants import FINISHED, NOT_STARTED, PLAYING, PAUSED
# from psychopy.hardware.emulator import launchScan
# from psychopy.logging import exp

# from psychopy import sound

# from psychopy import locale_setup
# from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock
# from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
#                                 STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

# import numpy as np  
# from numpy import (sin, cos, tan, log, log10, pi, average,
#                    sqrt, std, deg2rad, rad2deg, linspace, asarray)
# from numpy.random import random, randint, normal, shuffle
# import os  # handy system and path functions
# import sys  # to get file system encoding

# import psychtoolbox as ptb

# # To visulise modulated sin wave of pulsing circle
# from matplotlib import pyplot as plt
# import matplotlib.pylab as plb


win = visual.Window(fullscr=False, screen=1, color=(-1,-1,-1))


globalClock = core.Clock() 
print(globalClock) #<psychopy.clock.Clock object at 0x7f8f87c460f0>
print(globalClock.getTime()) #5.666700008077896e-05

trialClock = core.Clock()
print(f'trialClock 1: {trialClock.getTime()}') 


_timeToFirstFrame = win.getFutureFlipTime(clock="now")
print(f'trialClock 2: {trialClock.getTime()}')

time.sleep(0.5)


print(_timeToFirstFrame)  #0.015773587599960948

print(f'trialClock 3: {trialClock.getTime()}') #0.05047978799984776
trialClock.reset(_timeToFirstFrame)
print(f'trialClock 4: {trialClock.getTime()}') #0.015782759599915153

# below with: time.sleep(0.05), trialClock.reset(-_timeToFirstFrame)
# 0.015773587599960948
# trialClock 3: 0.05047978799984776
# trialClock 4: 0.015782759599915153

# below with: time.sleep(0.5), trialClock.reset(-_timeToFirstFrame)
# 0.012241981700118032
# trialClock 3: 0.5005758610000157
# trialClock 4: 0.012280131700208585

# below with: time.sleep(0.5), trialClock.reset(_timeToFirstFrame)
# 0.015172386000404714
# trialClock 3: 0.5009835259997999
# trialClock 4: -0.015164931000072102


print(f'trialClock 5: {trialClock.getTime()}') #0.015803667600266635
time.sleep(0.05)

print(f'trialClock 6: {trialClock.getTime()}')  #0.06633131960006722

win.flip()