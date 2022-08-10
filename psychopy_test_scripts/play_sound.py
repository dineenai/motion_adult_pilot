from psychopy import sound, visual, core
import os 
import psychtoolbox as ptb
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import pandas as pd

root_dir = '/Users/aine/Documents/CusackLab/robust_motion_correction_for_mri_using_dnns/pilot_paradigm/motion_adult_pilot/'
print(f"Root dir is: {root_dir}")

# name of subfolder from which to draw stimuli
stim_loc = 'audio_clips'
save_len_loc = os.path.join(root_dir,f'audio_clip_length.tsv')

stim_folder = os.path.join(root_dir,stim_loc)
# aud_file = 'CantinaBand3'
aud_file = 'PieMan_5min_9s'
# aud_file = 'PhoneCallHome SB_comp_v3_3db'

audio = sound.Sound(os.path.join(root_dir,stim_loc,aud_file))


globalClock = core.Clock() 
dur = audio.getDuration()
trialClock = core.Clock()
audio_len = pd.DataFrame(columns=['audio_file','actual_len','playing_len'])
ev = {'audio_file':None, 'actual_len':None,'playing_len':None}
ev['audio_file'] = aud_file
ev['actual_len'] = dur

win = visual.Window()
# audio.play() 
now = ptb.GetSecs()
audio.play(when=now) 
onset = globalClock.getTime() 

while audio.status == PLAYING:
    win.flip()


end = globalClock.getTime() 
ev['playing_len'] = end - onset

audio_len = audio_len.append(ev, ignore_index=True)
#save out events as tsv each time updated
audio_len.to_csv(save_len_loc, sep='\t')

print("did it save???")


