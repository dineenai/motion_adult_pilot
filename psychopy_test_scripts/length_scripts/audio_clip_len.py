from datetime import datetime
import os
import warnings
import random
from numpy.lib.npyio import save
import pandas as pd

#psychopy
from psychopy import visual, gui, core, sound, event
# from psychopy.clock import wait
from psychopy.constants import PLAYING, PAUSED, FINISHED, NOT_STARTED
from psychopy.gui.qtgui import DlgFromDict

#audio - try to re-add for windows - not mac compatible
from ctypes import POINTER, cast
# from comtypes import CLSCTX_ALL #re-add for test session...
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume #re-add


import random
import pandas as pd

from datetime import datetime, timedelta
# from paradigm_test2 import Session_Info

from psychopy import event, visual, core
from psychopy.constants import FINISHED, NOT_STARTED, PLAYING, PAUSED
from psychopy.hardware.emulator import launchScan
from psychopy.logging import exp

from psychopy import sound

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

import psychtoolbox as ptb



# root directory depending on user - must contain all necessary subfolders
if os.getlogin()=='cusacklab':
    root_dir = "C:\\Users\cusacklab\Desktop\Aine_Motion_Pilot\motion_adult_pilot"
elif os.getlogin()=='root':
    root_dir = '/Users/aine/Documents/CusackLab/robust_motion_correction_for_mri_using_dnns/pilot_paradigm/motion_adult_pilot/'

print(f"Root dir is: {root_dir}")


# /Users/aine/Documents/CusackLab/robust_motion_correction_for_mri_using_dnns/pilot_paradigm/motion_adult_pilot
# name of subfolder from which to draw stimuli
stim_loc = 'audio_clips'

stim_folder = os.path.join(root_dir,stim_loc)

if not os.path.exists(root_dir):
    raise(NotADirectoryError(f"Could not find root directory {root_dir}"))
elif not os.path.exists(stim_folder):
    raise(NotADirectoryError("One or more of your stimuli sub paths is incorrect"))

if len(os.listdir(stim_folder)) == 0:
    warnings.warn("your stimulus folder is empty")


save_loc = os.path.join(root_dir,f'audio_clip_length_FS.tsv')

# aud_file = 'PieMan_5min_9s'
aud_file = 'CantinaBand3'
print(f'Audio file is {aud_file}') 

# Only loads required audio as script is launched for each acquisition
# This is to avoid  error in clip played run needs to be terminated/repeated and to double check that acquisition is correct
# RUns automatically counted, displays desired sequence

# load audio
audio = sound.Sound(os.path.join(root_dir,stim_loc,aud_file))

win = visual.Window(screen=1, color=(-1,-1,-1))

globalClock = core.Clock() 

dur = audio.getDuration()

trialClock = core.Clock()

audio_len = pd.DataFrame(columns=['actual_len','playing_len'])
ev = {'actual_len':None,'playing_len':None}

ev['playing_len'] = dur

# aud_onset = globalClock.getTime() 
# audio.play()

now = ptb.GetSecs()
audio.play(when=now+0.5)  # play in EXACTLY 0.5s


if audio.status == PLAYING:
    win.flip()
# Add both numbers to a txt file...
# while audio
# if audio.status == FINISHED:

# if not audio.status == PLAYING:

if audio.status == PAUSED:
# = FINISHED
    end = globalClock.getTime() 
    ev['duration']=end-aud_onset


    audio_len = audio_len.append(ev, ignore_index=True)
    #save out events as tsv each time updated
    audio_len.to_csv(save_loc, sep='\t')





print("test")

# get a blank screen to display when audio is playing?