import random
import pandas as pd

from datetime import datetime, timedelta

import time

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

import os  
import sys  

import psychtoolbox as ptb
from matplotlib import pyplot as plt
import matplotlib.pylab as plb


def run_trial(win, audio, aud_file, save_aud_status_loc, MR_settings, save_loc, Session_Info, subNum):

    #launch scanning
    globalClock = core.Clock() 
    key_code = MR_settings['sync']
    pause_during_delay = (MR_settings['TR'] > 0.4)
    sync_now = False
    infer_missed_sync = False
    max_slippage = 0.02

    centrepos=[0,-450]
    distort_centrepos=[0,-480]

    stretchy=1/1.46
    fixsize=10

    audio_clip_dur = audio.getDuration()
    print(f"Length of audio clip: {audio_clip_dur}") 

    # Is there any advantage t ousing global clock vs trial clock - such as syncing with scanner?

    #### NB remember to revert to 'Scan' for scan... ####
    vol = launchScan(win, MR_settings, globalClock=globalClock, mode='Test', wait_msg='waiting for scanner ...')
    # vol = launchScan(win, MR_settings, globalClock=globalClock, mode='Scan', wait_msg='waiting for scanner ...')

    # Initialize components for Routine "trial"
    trialClock = core.Clock()

    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    frameTolerance = 0.001

    # Circle for Visual Metrenome
    circle = visual.Circle(
        win=win,
        name='circle', units='pix', 
        ori=0,
        # pos=(0, 0),
        pos=centrepos,
        size=1.0, radius=1.5,
        lineColor='white',
        lineWidth=6.0,
        # fillColor= 'yellow') # Decided to leave as outline - better visibility with anterior coil on 
        )

    #Setup events  
    #include real time column for sanity checking, will be excluded in BIDS
    expt_events = pd.DataFrame(columns=['onset','duration','trial_type', 'real_time'])

    flip_time = []
  
    audio_status = []
    audio_status_time = []
    audio_status_realtime = []
    # audio_status_trialtime = []
    audio_status_globaltime = []

    allKeys = []
    while len(allKeys) == 0:
        allKeys = event.getKeys()
    if MR_settings['sync'] in allKeys:
        sync_now = key_code # flag
    if sync_now:    # waits for sync 

        # ------Prepare to start Visual Metronome-------
        continueRoutine = True

        # update component parameters for each repeat
        # keep track of which components have finished
        trialComponents = [circle]
        for thisComponent in trialComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
                # Circle component hasthe attribute status

        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now") # around 15 ms
        
        # Should this  be added (instead of subtracted) so that the clock starts when the next frame flips????? 
        # This is how it was written in the builder code but I do not understand why?
        trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        print(f'trialClock start time: {trialClock.getTime()}') #0.0.015855798000302457
        frameN = -1

        #reset event dict for this stimulus
        ev = {'onset':None,'duration':None,'trial_type':None, 'real_time':None}
    
        # Present AUDIO stimuli
        
        # NB 13/6/22: Change all logs from glocalClock to trialClock: WHICH IS PREFERABLE # added - _timeToFirstFrame 13/6/22 
        # vis_met_onset = trialClock.getTime() + _timeToFirstFrame
        vis_met_onset = globalClock.getTime() + _timeToFirstFrame


        # Realtime onsets
        vis_met_onset_realtime = (datetime.now() + timedelta(milliseconds=_timeToFirstFrame)).strftime("%H:%M:%S:%f")  
        print(vis_met_onset_realtime) 
        
        # 10 seconds to practice task before audio starts - is this sufficient?
        audio_delay = 10.00000        
        
        # Stimuli Onsets
        # aud_onset = trialClock.getTime() + audio_delay + _timeToFirstFrame
        aud_onset = globalClock.getTime() + audio_delay + _timeToFirstFrame
        
        # Realtime onsets

        nextFlip = win.getFutureFlipTime(clock='ptb')
        # _timeToFirstFrame - number in ms!!!!!!
        # nextFlip is essentially ptb.GetSecs() + _timeToFirstFrame
        # nextFlip is the time it will be at the nextflip
        # _timeToFirstFrame is the time to the next flip


        timeToNextFLip = nextFlip - ptb.GetSecs()

        aud_onset_realtime = (datetime.now() + timedelta(milliseconds=_timeToFirstFrame) + timedelta(0,audio_delay)).strftime("%H:%M:%S:%f")  
        # aud_onset_realtime = (nextFlip + timedelta(0,audio_delay)).strftime("%H:%M:%S:%f")  #TypeError: unsupported operand type(s) for +: 'float' and 'datetime.timedelta'
    
        print(f'timedelta(milliseconds=_timeToFirstFrame) {timedelta(milliseconds=_timeToFirstFrame)}, timedelta(0,audio_delay) {timedelta(0,audio_delay)}')

        # Next flip is in around 15 ms

        audio.play(when=nextFlip+audio_delay) 
    
        # Record audio status from next flip
        audio_status.append(audio.status)
        # This is recorded as nextflip because audio status will change now but
        # we want to log audio from beginning of preaudio period
        # Note that audio status is recorded as 1 for plaing in the df for the duration of the delay
        audio_status_time.append(nextFlip)
        # audio_status_trialtime.append(trialClock.getTime() + _timeToFirstFrame)
        audio_status_globaltime.append(globalClock.getTime() + _timeToFirstFrame)
        audio_status_realtime.append(aud_onset_realtime)

        print(f"Audio will start playing in 10 s at {aud_onset_realtime}") 

        ev['real_time'] = vis_met_onset_realtime
        ev['onset']=vis_met_onset
        # end of preaudio period = start of audio => end = aud_onset
        
        ev['duration']=aud_onset-vis_met_onset
        ev['trial_type']='preaudio_metronome'

        #update events_df with this trial
        expt_events = expt_events.append(ev, ignore_index=True)
        
        # around 6 ms for save
        #save out events as tsv each time updated
        expt_events.to_csv(save_loc, sep='\t')

        # 10 s pre audio, 5 s post audio
        # SHOULD BE: 10 pre aduio, 5 post audio
        preaudio_met_dur = 10.000
        post_audio_met_dur = 5.000
        # Audio duration should be accuract and is used to set the length of the visual metrenome
        len_of_vis_met = preaudio_met_dur + audio_clip_dur + post_audio_met_dur

        print(f"Visual Metrenome will run for: {len_of_vis_met} units?")
        
        # while continueRoutine and routineTimer.getTime() > 0:
        while continueRoutine > 0:

            # get current time
            t = trialClock.getTime()

            # print(f"START: {ptb.GetSecs()}" )
            audio_status.append(audio.status)
            audio_status_time.append(ptb.GetSecs())
            # audio_status_trialtime.append(trialClock.getTime())
            audio_status_globaltime.append(globalClock.getTime())
            audio_status_realtime.append(datetime.now().strftime("%H:%M:%S:%f"))
            
            tThisFlip = win.getFutureFlipTime(clock=trialClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *circle* updates
            if circle.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                circle.frameNStart = frameN  # exact frame index
                circle.tStart = t  # local t and not account for scr refresh
                circle.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(circle, 'tStartRefresh')  # time at next scr refresh
                circle.setAutoDraw(True)
                
            if circle.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                # if tThisFlipGlobal > circle.tStartRefresh + 10-frameTolerance:
                if tThisFlipGlobal > (circle.tStartRefresh + len_of_vis_met-frameTolerance):
                    # keep track of stop time/frame for later
                    circle.tStop = t  # not accounting for scr refresh
                    circle.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(circle, 'tStopRefresh')  # time at next scr refresh
                    circle.setAutoDraw(False)

            if circle.status == STARTED:  # only update if drawing

                # Set Radius of the Circle
                # Do we want to have a perfect circle or is the distorted oval ok? If former, edit for MRI PC
                # Collapse to Origin - presents as too volatile, translate in y-direction
                # Add phase shift (28/6 * n) - change systematically with subjects

                fc = 1/7
                fdelta = 0.6 * fc
                A = 0.2
                fm = 1/28

                # Laptop Version
                ym = 0.15 *(sin(2 * pi * fm * t) *(cos(4 * pi * fm * t)+ 5))/(6 * fm) 
                yc = 200 + 1200 * A * cos (2 * pi * fc * t + fdelta/fm * ym  ) /3
                
                # MRI PC
                # n = subNum%6
                # ym = 0.15 * (sin(2 * pi * fm * (t + (28/6 * n))) *(cos(4 * pi * fm * (t + (28/6 * n)))+ 5))/(6 * fm)
                # yc = 50 + 250 * A * cos (2 * pi * fc * (t + (28/6 * n)) + fdelta/fm * ym  ) /3

                circle.setSize(yc, log=False)

            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
    
                # remove long sleep, replaced with multiple short sleeps to enable repeated audio status recording
                # time.sleep(0.005)
                # sleep for 0.0005 s x 10 ie 5 ms - but slipt be 10 to allow higher precision audio status recording and => script timing
                # 5 ms total sleep
                for i in range(10):
                    time.sleep(0.0005)
                    # print(f'Audio Status is: {audio.status}')

                    audio_status.append(audio.status)
                    audio_status_time.append(ptb.GetSecs())
                    audio_status_realtime.append(datetime.now().strftime("%H:%M:%S:%f"))
                    # audio_status_trialtime.append(trialClock.getTime())
                    audio_status_globaltime.append(globalClock.getTime())
                
                t_bef = ptb.GetSecs()

                win.flip()

                t_af = ptb.GetSecs()

                flip_dif = t_af - t_bef
                flip_time.append(flip_dif)

                keys = event.getKeys()

                if 'a' in keys:
                    if audio.status == PLAYING:
                        ev = {'onset':None,'duration':None,'trial_type':None, 'real_time':None}

                        ev['real_time'] = datetime.now().strftime("%H:%M:%S:%f")
                        
                        press_left_onset = globalClock.getTime()  
                        # press_left_onset = trialClock.getTime()  
                        ev['onset']=press_left_onset
                        ev['trial_type']='Left-Min'
                        ev['duration']=0
                    
                        #update events_df with this trial
                        expt_events = expt_events.append(ev, ignore_index=True)
                        #save out events as tsv each time updated
                        expt_events.to_csv(save_loc, sep='\t')
            

                if 'c' in keys: #Changed from d to c - new NNL leads
                    if audio.status == PLAYING:
                        ev = {'onset':None,'duration':None,'trial_type':None, 'real_time':None}

                        ev['real_time'] = datetime.now().strftime("%H:%M:%S:%f")
                        
                        press_right_onset = globalClock.getTime()  
                        # press_right_onset = trialClock.getTime()  
                        ev['onset']=press_right_onset
                        ev['trial_type']='Right-Max'
                        ev['duration']=0
                    
                        #update events_df with this trial
                        expt_events = expt_events.append(ev, ignore_index=True)
                        #save out events as tsv each time updated
                        expt_events.to_csv(save_loc, sep='\t')


                elif 'escape' in keys:
                    ev = {'onset':None,'duration':None,'trial_type':None, 'real_time':None}
                    end = globalClock.getTime()
                    # end = trialClock.getTime()
                    audio.pause()
                    
                    ev['real_time'] = aud_onset_realtime
                    ev['onset']=aud_onset
                    ev['duration']=end-aud_onset
                    ev['trial_type']=aud_file

                    #update events_df with this trial
                    expt_events = expt_events.append(ev, ignore_index=True)
                    #save out events as tsv each time updated
                    expt_events.to_csv(save_loc, sep='\t')
                    
                    return

        # Attempt moving this here from below
        # End Visual Metrenome
        # -------Ending Routine "trial"-------
        # Log time that metrenome ends
        end_post_met_period = ptb.GetSecs()
        
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False) 
        
        print(f"END OF EXPERIMENT: {end_post_met_period}")
        
        # Metrenome has stopped playing - log audio and post audio metrenome periods

        print(f'Flip Time Stats\nMin value is: {min(flip_time)} Max: {max(flip_time)} avg: {average(flip_time)}')


        # Get audio timing
        # aud_dict = {'audio_status': audio_status, 'audio_status_time': audio_status_time, 'audio_status_realtime': audio_status_realtime, 'audio_status_trialtime': audio_status_trialtime}  
        aud_dict = {'audio_status': audio_status, 'audio_status_time': audio_status_time, 'audio_status_realtime': audio_status_realtime, 'audio_status_globaltime': audio_status_globaltime}
        aud_df = pd.DataFrame(aud_dict)  

        # extract time audio starts from df, NB includes preaudio wait period, precisly timed as above
        audio_start = aud_df['audio_status_time'][0]
        audio_real_start = aud_df['audio_status_realtime'][0]
        # audio_trialtime_start = aud_df['audio_status_trialtime'][0]
        audio_globaltime_start = aud_df['audio_status_globaltime'][0]
               
        # extract time audio stops from df
        audio_stop = aud_df['audio_status_time'][aud_df[aud_df.audio_status == -1].index[0]]
        audio_realstop = aud_df['audio_status_realtime'][aud_df[aud_df.audio_status == -1].index[0]]
        # audio_trialtime_stop = aud_df['audio_status_trialtime'][aud_df[aud_df.audio_status == -1].index[0]]
        audio_globaltime_stop = aud_df['audio_status_globaltime'][aud_df[aud_df.audio_status == -1].index[0]]
        
        print(f'audio_real_start: {audio_real_start}, audio_realstop {audio_realstop}')
        audio_TIME = audio_stop - audio_start
        actual_audio_TIME = audio_stop - audio_start - audio_delay
        print(f'AUDIO STOP: {audio_stop}')
        print(f"AUDIO TIME IS {audio_TIME}")
        # print(f"Actual AUDIO TIME IS {actual_audio_TIME}, audio_trialtime_start {audio_trialtime_start}")
        print(f"Actual AUDIO TIME IS {actual_audio_TIME}, audio_globaltime_start {audio_globaltime_start}")

        print(f'audio_stop{audio_stop} type {type(audio_stop)} audio_stop-aud_onset = {audio_stop-aud_onset}')

        aud_df.to_csv(save_aud_status_loc)  


        # Log the Audio Clip as an event
        ev = {'onset':None,'duration':None,'trial_type':None, 'real_time':None}

        ev['real_time'] = aud_onset_realtime
        ev['onset']=aud_onset
        # replace duration with realtime
        # ev['duration']= dur 
        ev['duration']= actual_audio_TIME
        ev['trial_type']=aud_file

        #update events_df with this trial
        expt_events = expt_events.append(ev, ignore_index=True)
        #save out events as tsv each time updated
        expt_events.to_csv(save_loc, sep='\t')

        # Sucessfully moved to above!
        # # End Visual Metrenome
        # # -------Ending Routine "trial"-------
        # for thisComponent in trialComponents:
        #     if hasattr(thisComponent, "setAutoDraw"):
        #         thisComponent.setAutoDraw(False)

        # end_post_met_period = ptb.GetSecs()
        # print(f"END OF EXPERIMENT: {end_post_met_period}")


        # POST METRONOME PERIOD

        # Log the post audio metrenome period as an event
        # AGAIN: Hard coding of durations is leading to errors in logging of these events 
        # Realtime logs would be prefered BUT difficult to resolve due to the nature of the metrenome code
        ev = {'onset':None,'duration':None,'trial_type':None, 'real_time':None}
        
        ev['trial_type'] = 'postaudio_metronome'
        # fix the onset here: trialClock.getTime() 
        ev['onset'] = audio_stop #audio_trialtime_start
        # ev['onset'] = audio_trialtime_stop
        ev['onset'] = audio_globaltime_stop
        # ev['real_time'] = audio_realstop.strftime("%H:%M:%S:%f")  
        ev['real_time'] = audio_realstop

        # Around 10 ms longer than expected - is this for one final flip?/ one final run through the loop after stimuli ave ended?
        post_aud_dur = end_post_met_period - audio_stop
        ev['duration'] = post_aud_dur

        #update events_df with this trial
        expt_events = expt_events.append(ev, ignore_index=True)
        #save out events as tsv each time updated
        expt_events.to_csv(save_loc, sep='\t')

        sync_now = False

        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()


    