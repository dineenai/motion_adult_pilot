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

# To visulise modulated sin wave of pulsing circle
from matplotlib import pyplot as plt
import matplotlib.pylab as plb


def run_trial(win, audio, aud_file, MR_settings, save_loc, Session_Info):

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

    dur = audio.getDuration()
    print(f"getdur: {dur}")

    #### NB remember to revert to 'Scan' for scan... ####
    vol = launchScan(win, MR_settings, globalClock=globalClock, mode='Test', wait_msg='waiting for scanner ...')
    # vol = launchScan(win, MR_settings, globalClock=globalClock, mode='Scan', wait_msg='waiting for scanner ...')

    # Initialize components for Routine "trial"
    trialClock = core.Clock()

    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    frameTolerance = 0.001

    circle = visual.Circle(
        win=win,
        name='circle', units='pix', 
        ori=0, pos=(0, 0), size=1.0, radius=1.5,
        lineColor='white',
        lineWidth=6.0
        # fillColor= 'yellow')
        )

    #Setup events
    #include real time column for sanity checking, will be excluded in BIDS
    expt_events = pd.DataFrame(columns=['onset','duration','trial_type', 'real_time'])
    
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
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1


        #reset event dict for this stimulus
        ev = {'onset':None,'duration':None,'trial_type':None, 'real_time':None}

        # 10 seconds to practice task before audio starts - is this sufficient?
        audio_delay = 10.00000
        
        # Present AUDIO stimuli

        # Stimuli Onsets
        vis_met_onset = globalClock.getTime() #.getTime() Returns the current time on this clock in secs (sub-ms precision).
        aud_onset = globalClock.getTime() + audio_delay

        # Realtime onsets
        vis_met_onset_realtime = datetime.now().strftime("%H:%M:%S:%f")
        aud_onset_realtime = (datetime.now() + timedelta(0,audio_delay)).strftime("%H:%M:%S:%f")

        print(vis_met_onset_realtime)
        print(aud_onset_realtime)

        # breaks on Rhodri's laptop, work's on Aine's        
        # # GetSecs: returns the time in seconds (with high precision).
        now = ptb.GetSecs()
        # audio.play(when=now+3.000000)
        audio.play(when=now+audio_delay)

        # breaks on  Aine's laptop - works on Rhodri's windows
        # audio onset delay
        # audio.play(secs=10.000)

        ev['real_time'] = vis_met_onset_realtime
        ev['onset']=vis_met_onset
        # end of preaudio period = start of audio => end = aud_onset
        ev['duration']=aud_onset-vis_met_onset
        ev['trial_type']='preaudio_metronome'

  
        #update events_df with this trial
        expt_events = expt_events.append(ev, ignore_index=True)
        #save out events as tsv each time updated
        expt_events.to_csv(save_loc, sep='\t')

        # while continueRoutine and routineTimer.getTime() > 0:
        while continueRoutine > 0:
            # get current time
            t = trialClock.getTime()
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
                # CHANGE L of AUDIO HERE TO BE LEN OF CLIP..... + 5????
                # add length of audio to pre audio len and post audio len - make pre audio len longer
                # add instruction to the screen?????
                # pre = 10.0
                # post = 5.0
                # len_of_vis_met = dur + pre + post
                len_of_vis_met = dur +15.0
                # print(f"len_of_vis_met: {len_of_vis_met}")
                if tThisFlipGlobal > circle.tStartRefresh + len_of_vis_met-frameTolerance:
                # if tThisFlipGlobal > circle.tStartRefresh + 15-frameTolerance:
                    # keep track of stop time/frame for later
                    circle.tStop = t  # not accounting for scr refresh
                    circle.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(circle, 'tStopRefresh')  # time at next scr refresh
                    circle.setAutoDraw(False)

            if circle.status == STARTED:  # only update if drawing

                fc = 1/7
                fdelta = 0.6 * fc
                A = 0.2
                fm = 1/28

                ym = 0.15 *(sin(2 * pi * fm * t) *(cos(4 * pi * fm * t)+ 5))/(6 * fm) 
                # ORIGINAL MODEL
                # yc = A * cos (2 * pi * fc * t + fdelta/fm * ym  ) /3
                # Add scaling:
                yc = 200 + 1200 * A * cos (2 * pi * fc * t + fdelta/fm * ym  ) /3
                # Collapse to Origin - presents as too volatile
                # yc = 2000 * A * cos (2 * pi * fc * t + fdelta/fm * ym  ) /3

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
                win.flip()


                    # # while audio.status != FINISHED:
                keys = event.getKeys()

                # Probably no need for pause function, remove?
                
                #functionality to pause the audio while scan is still running
                #this will record how long the stimulus was paused for
                #note that a paused screen and no audio will be displayed if pressed
                if 'p' in keys:
                    # ev = {'onset':None,'duration':None,'trial_type':None,'real_time':None}
                    ev = {'onset':None,'duration':None,'trial_type':None, 'real_time':None}
                    if audio.status == PLAYING:
                        audio.pause()
                        ev['real_time'] = datetime.now().strftime("%H:%M:%S:%f")
                        
                        pause_onset = globalClock.getTime()  
                        ev['onset']=pause_onset
                        ev['trial_type']='pause'

                    elif audio.status == PAUSED:
                        audio.play()

                        pause_end = globalClock.getTime()
                        ev['duration']=pause_end - pause_onset
                    
                        #update events_df with this trial
                        expt_events = expt_events.append(ev, ignore_index=True)
                        #save out events as tsv each time updated
                        expt_events.to_csv(save_loc, sep='\t')

                if 'a' in keys:
                    # ev = {'onset':None,'duration':None,'trial_type':None,'real_time':None}
                    if audio.status == PLAYING:
                        ev = {'onset':None,'duration':None,'trial_type':None, 'real_time':None}

                        ev['real_time'] = datetime.now().strftime("%H:%M:%S:%f")
                        
                        press_left_onset = globalClock.getTime()  
                        ev['onset']=press_left_onset
                        ev['trial_type']='Left-Min'

                        # press_left_end = globalClock.getTime()
                        # ev['duration']=press_left_end-press_left_onset
                        ev['duration']=0
                    
                        #update events_df with this trial
                        expt_events = expt_events.append(ev, ignore_index=True)
                        #save out events as tsv each time updated
                        expt_events.to_csv(save_loc, sep='\t')
            
                if 'd' in keys:
                    if audio.status == PLAYING:
                        # ev = {'onset':None,'duration':None,'trial_type':None,'real_time':None}
                        ev = {'onset':None,'duration':None,'trial_type':None, 'real_time':None}

                        ev['real_time'] = datetime.now().strftime("%H:%M:%S:%f")
                        
                        press_right_onset = globalClock.getTime()  
                        ev['onset']=press_right_onset
                        ev['trial_type']='Right-Max'

                        # press_right_end = globalClock.getTime()
                        # ev['duration']=press_right_end - press_right_onset
                        ev['duration']=0
                    
                        #update events_df with this trial
                        expt_events = expt_events.append(ev, ignore_index=True)
                        #save out events as tsv each time updated
                        expt_events.to_csv(save_loc, sep='\t')


                elif 'escape' in keys:
                    ev = {'onset':None,'duration':None,'trial_type':None, 'real_time':None}
                    end = globalClock.getTime()
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
               
        ev = {'onset':None,'duration':None,'trial_type':None, 'real_time':None}


        # NO NEED AS ONLY GET TO HERE WHEN THIS IS THE CASE ANYWAY!
        # # MAKE SURE THAT EVENT INDEXES DURATION OF STIMULUS!!!!!
        # if audio.status == FINISHED:
        # # if audio.status != PLAYING:
            

        # audio.pause()
        end = globalClock.getTime() 
        
        ev['real_time'] = aud_onset_realtime
        ev['onset']=aud_onset
        # also subtract duration of post audio
        ev['duration']=end-aud_onset-5.0
        ev['trial_type']=aud_file

        #update events_df with this trial
        expt_events = expt_events.append(ev, ignore_index=True)
        #save out events as tsv each time updated
        expt_events.to_csv(save_loc, sep='\t')






# Post Audio Period
        ev = {'onset':None,'duration':None,'trial_type':None, 'real_time':None}

        # end = globalClock.getTime()
        onset = globalClock.getTime()-5.0
        # realtime_end = datetime.now().strftime("%H:%M:%S:%f")
        # realtime_start = datetime.now().strftime("%H:%M:%S:%f")- timedelta(seconds=5)
        realtime_start = (datetime.now()- timedelta(seconds=5)).strftime("%H:%M:%S:%f")
        post=0.5
        ev['trial_type'] = 'postaudio_metronome'
        ev['onset'] = onset
        # ev['real_time'] = realtime_end-5.0
        ev['real_time'] = realtime_start
        ev['duration'] = 5.0 

        #update events_df with this trial
        expt_events = expt_events.append(ev, ignore_index=True)
        #save out events as tsv each time updated
        expt_events.to_csv(save_loc, sep='\t')

        # # Post Audio Period
        # ev = {'onset':None,'duration':None,'trial_type':None, 'real_time':None}

        # onset = globalClock.getTime()
        # realtime = datetime.now().strftime("%H:%M:%S:%f")

        # ev['trial_type'] = 'postaudio_metronome'
        # ev['onset'] = onset
        # ev['real_time'] = realtime

        
        # # # length of postaudio period - set desired n of seconds
        # post_audio_length = 5
        # timer = core.Clock()
        # timer.add(post_audio_length)
        # while timer.getTime()<0:
        #     # fixation.draw()
        #     win.flip()

        # end = globalClock.getTime()
        # ev['duration'] = end - onset

        # #update events_df with this trial
        # expt_events = expt_events.append(ev, ignore_index=True)
        # #save out events as tsv each time updated
        # expt_events.to_csv(save_loc, sep='\t')

        sync_now = False


        # End Visual Metrenome
        # -------Ending Routine "trial"-------
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)

        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()


    