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

#experiment module
# import audio_motion_adult_pilot_mar_22 # ACTUAL
import audio_motion_adult_pilot_mar_22
import get_audio_clip_length 

### AUDIO ### - set for scan - not compatible with mac

# # set audio levels - only windows compatible            
# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.SetMute(0, None)
# volume.SetMasterVolumeLevel(-12.0, None)
# print("volume.GetMasterVolumeLevel(): %s" % volume.GetMasterVolumeLevel())



#################################################
### set up scan - participant ID, orders etc. ###
#################################################


# MRI PC:
# root_dir = "C:\\Users\cusacklab\Desktop\Aine_Motion_Pilot\motion_adult_pilot"
# Aine Laptop:
# root_dir = '/Users/aine/Documents/CusackLab/robust_motion_correction_for_mri_using_dnns/pilot_paradigm/motion_adult_pilot/'

# root directory depending on user - must contain all necessary subfolders
if os.getlogin()=='cusacklab':
    root_dir = "C:\\Users\cusacklab\Desktop\Aine_Motion_Pilot\motion_adult_pilot"
elif os.getlogin()=='root':
    root_dir = '/Users/aine/Documents/CusackLab/robust_motion_correction_for_mri_using_dnns/pilot_paradigm/motion_adult_pilot/'

print(f"Root dir is: {root_dir}")

# name of subfolder from which to draw stimuli
stim_loc = 'audio_clips'

stim_folder = os.path.join(root_dir,stim_loc)

if not os.path.exists(root_dir):
    raise(NotADirectoryError(f"Could not find root directory {root_dir}"))
elif not os.path.exists(stim_folder):
    raise(NotADirectoryError("One or more of your stimuli sub paths is incorrect"))

if len(os.listdir(stim_folder)) == 0:
    warnings.warn("your stimulus folder is empty")

#set paramaters for display # MRI PC 
centrepos=[0,-450]
distort_centrepos=[0,-480]

stretchy=1/1.46
fixsize=10

#Get participant/run info

warnDlg = gui.Dlg(title='Caution')
warnDlg.addText('Please check PID and run #')
warnDlg.addText('\nIf testing code use: 0, 0')
warnDlg.show()
if not warnDlg.OK:
    core.quit()

max_runs = 6

hist_file = os.path.join(root_dir,'expt_history_motion_pilot.csv')
expt_history = pd.read_csv(hist_file, index_col=0)
last_partic = expt_history['participantID'].max()
last_run = expt_history.loc[max(expt_history.index[expt_history['participantID']==last_partic]),'num_runs']

if last_run >= max_runs:
    subj_num = last_partic + 1
    run_num = 1
else:
    subj_num = last_partic
    run_num = last_run + 1

#Display session information
# USE PID 0 for test
Session_Info = {
    'PID': subj_num, 
    'Run #': run_num,
    }
infoDlg = gui.DlgFromDict(Session_Info, title='Session Info', order=['PID', 'Run #'])

if not infoDlg.OK:
    core.quit()

#reset in case of manual editing in dialogue box
subNum = Session_Info['PID']
runNum = Session_Info['Run #'] 

#reset in case of manual editing in dialogue box
_subj = Session_Info['PID']

#Set output conditions
if len(str(subNum)) == 1:
    _subj = f'00{subNum}'
elif len(str(subNum)) == 2:
    _subj = f'0{subNum}'
else:
    _subj = f'{subNum}'


# Sequence of Acquisitions, depending on participant ID
orders = {    
    0: ['mb_axial_motion', 'mb_axial_still', 'mb_sagit_motion', 'mb_sagit_still', 'sb_axial_motion', 'sb_axial_still'], 
    1: ['mb_axial_still', 'mb_axial_motion', 'mb_sagit_still', 'mb_sagit_motion', 'sb_axial_still', 'sb_axial_motion'], 
    2: ['mb_sagit_motion', 'mb_sagit_still', 'sb_axial_motion', 'sb_axial_still', 'mb_axial_motion', 'mb_axial_still'], 
    3: ['mb_sagit_still', 'mb_sagit_motion', 'sb_axial_still', 'sb_axial_motion', 'mb_axial_still', 'mb_axial_motion'], 
    4: ['sb_axial_motion', 'sb_axial_still', 'mb_axial_motion', 'mb_axial_still', 'mb_sagit_motion', 'mb_sagit_still'], 
    5: ['sb_axial_still', 'sb_axial_motion', 'mb_axial_still', 'mb_axial_motion', 'mb_sagit_still', 'mb_sagit_motion']
}

runNum = int(runNum)
print(runNum)

participant_order = orders[subNum%6]

acquisition = participant_order[runNum -1]

# run ranging from 1 --> 6

print(orders[subNum%6][runNum - 1])
print(acquisition)



#######################
### STIMULI IMPORTS ###
#######################

# Load Audio File depending on runNum

# # # # Short 3s Audio Clip for testing
# # # # aud_filetest = 'CantinaBand3.wav'
# aud_file12 = 'CantinaBand3.wav'
# aud_file34 = 'CantinaBand3.wav'
# aud_file56 = 'CantinaBand3.wav'

# TESTING
# aud_file12 = 'PhoneCallHome SB_comp_v3_3db'
# aud_file34 = 'PhoneCallHome SB_comp_v3_3db'
# aud_file56 = 'PhoneCallHome SB_comp_v3_3db'

# aud_file12 = 'PieMan_5min_9s'
# aud_file34 = 'PieMan_5min_9s'
# aud_file56 = 'PieMan_5min_9s'


# # Actual audio clips for scanning NB
aud_file12 = 'PhoneCallHome SB_comp_v3_3db'
aud_file34 = 'PieMan_5min_9s_comp_v2'
aud_file56 = 'HauntedHouse_5min2s'


# audfiles = (aud_filetest, aud_file12, aud_file12, aud_file34, aud_file34, aud_file56, aud_file56)
# aud_file = audfiles[runNum]
# print(audfiles[runNum])


# if runNum == (0):
#     print("TEST")
#     aud_file = aud_filetest
    
if runNum == (1):
    print("1")
    aud_file = aud_file12

elif runNum == (2):
    print("2")
    aud_file = aud_file12
    
elif runNum == (3):
    print("3")
    aud_file = aud_file34

elif runNum == (4):
    print(" 4")
    aud_file = aud_file34

elif runNum == (5):
    aud_file = aud_file56
    print("5")

elif runNum == (6):
    print("6")
    aud_file = aud_file56
    
else:
    # make message more specific
    print("Failed to assign appropriate audio file")

print(f'Audio file is {aud_file}') 

# Only loads required audio as script is launched for each acquisition
# This is to avoid  error in clip played run needs to be terminated/repeated and to double check that acquisition is correct
# RUns automatically counted, displays desired sequence

# load audio
audio = sound.Sound(os.path.join(root_dir,stim_loc,aud_file))


infoDlg = gui.Dlg(title='Acquisition')
infoDlg.addText(f'{acquisition}')
infoDlg.show()
if not infoDlg.OK:
    core.quit()


#events file save location according to BIDS specification
# bids ordering: task-audio, acq, run
# save_dir = os.path.join(root_dir,'logs0', f'sub-{_subj}',f'task-audio_{aud_file[:-4]}',f'acq-{acquisition}', f'run-{runNum}','func')
save_dir = os.path.join(root_dir,'logs_motion_adult_pilot', f'sub-{_subj}','func')
if not os.path.exists(save_dir):
    os.makedirs(save_dir)


# Update these parameters?
#Configure MRI Settings
MR_settings = {
    'TR': 0.656,     # duration (sec) per whole-brain volume
    # 'volumes': 455,    # number of whole-brain 3D volumes per scanning run (731 seconds per run, 12.18 mins), might be more if pause or attend needed
    'volumes': 10,    # decreased for testing
    'sync': 's', # character to use as the sync timing event; assumed to come at start of a volume
    'skip': 10,       # number of volumes lacking a sync pulse at start of scan (for T1 stabilization)
    'sound': True   # in test mode: play a tone as a reminder of scanner noise
    }


# # all Psychopy stimuli need to be loaded onto a window
# grey: color=(-1,-1,-1) # white: color=(1,1,1) #black:
win = visual.Window(fullscr=True, screen=1, color=(-1,-1,-1))

print('audio loaded')

print(
    """
    --------------------------------
    PARADIGM INSTRUCTIONS:
    --------------------------------
    pre-load audio

    press 'e' to launch experiment and wait for scanner to send first trigger pulse
        if the experiment needs to be relaunched, press 'esc' to return to main waiting screen
    
    press 'r' to re-load audio
        this will be time consuming

    press 'q' to quit the entire experiment.
        all events and logs should have saved within the experiment modules and this should be safe
    """
)


while True: 
    keys = event.getKeys()

    #press e for experiment
    if 'e' in keys:

        launch = datetime.now().strftime("%H-%M-%S")
        
        save_loc = os.path.join(save_dir,f'sub-{_subj}_task-audio_{aud_file[:-4]}_acq-{acquisition}_run-{runNum}-{launch}_events.tsv')
        
        audio_motion_adult_pilot_mar_22.run_trial(win, audio, aud_file, MR_settings, save_loc,  Session_Info) 
        #  To Get duration for which an audio clip is actually played:
        # get_audio_clip_length.run_trial(win, audio, aud_file, MR_settings, save_loc,  Session_Info) 

        # Update history file for auto loading of next participantID and runNum
        _hist = pd.DataFrame({'participantID':[subNum] , 'num_runs':[runNum]})
        expt_history = expt_history.append(_hist, ignore_index=True)
        expt_history.to_csv(os.path.join(root_dir,'expt_history_motion_pilot.csv'))

        core.quit() 


    # reload if necessary: this is time conssuming
    if 'r' in keys:
        print('... reload of audio')

        # assuming aud_file is defined above based on runNum
        audio = sound.Sound(os.path.join(root_dir,aud_file))
        
        print('audio re-loaded')
        

    if 'q' in keys:
        core.quit()
