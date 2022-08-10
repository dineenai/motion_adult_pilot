from psychopy import core, sound, visual

import psychtoolbox as ptb

from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, STOPPED, FINISHED)

from datetime import datetime

# trialClock = core.Clock()
# print(trialClock) #<psychopy.clock.Clock object at 0x7f8af7316128>

# print(trialClock.getTime()) #6.938100023035076e-05
# # 4.827700013265712e-05
# # 4.9593000312597724e-05


# now = ptb.GetSecs()
# print(now)
# # 2700.803742682
# # 2707.647665986
# # 2721.132424717
# # 7. 30 am = 27000

# win = visual.Window(fullscr=False, screen=1, color=(-1,-1,-1))

aud_path = '/Users/aine/Documents/CusackLab/robust_motion_correction_for_mri_using_dnns/pilot_paradigm/motion_adult_pilot/audio_clips/CantinaBand3.wav'
# audio = sound.Sound(aud_path)

# dur = audio.getDuration()
# print(f"getdur: {dur}") 

# # TypeError: play() got an unexpected keyword argument 'secs'
# audio.play()
# print(audio) #<psychopy.sound.backend_ptb.SoundPTB object at 0x7fe3c9b52978>
# # sound.Sound(aud_path).play()

# if audio.status == PLAYING:
#     win.flip()





# mySound = sound.Sound(aud_path)
mySound = sound.Sound('A', autoLog=True)
# now = ptb.GetSecs()
# mySound.play(when=now+0.5) 

win = visual.Window()
win.flip()
# nextFlip = win.getFutureFlipTime(clock='ptb')

# mySound.play(when=nextFlip)  # sync with screen refresh

now = ptb.GetSecs()
print(f'NOW: {now}') #4858.902424824
audio_delay = 2.000
mySound.play(when=now+audio_delay) 

globalClock = core.Clock() 
print(f'Global Clock{globalClock}')

print(datetime.now().strftime("%H:%M:%S:%f")) #09:40:33:056490
# t = globalClock.getTime()
print(f'GC.gettime{globalClock.getTime()}')
length = 5

# always

length_is =now+length

# Note once initialised as a variable now is a constant!!!
# need to use ptp.GetSecs()to dynamically update
while length_is > ptb.GetSecs():
    win.flip()
    print(length_is)
    print(now)

print(datetime.now() ) #2022-05-04 10:26:13.993701