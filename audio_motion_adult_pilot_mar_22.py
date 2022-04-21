import random
import pandas as pd

from datetime import datetime, timedelta

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


def run_trial(win, audio, aud_file, MR_settings, save_loc, Session_Info, subNum):

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

    # Aine's Macbookair
    # circle = visual.Circle(
    #     win=win,
    #     name='circle', units='pix', 
    #     ori=0, pos=(0, 0), size=1.0, radius=1.5,
    #     lineColor='white',
    #     lineWidth=6.0
    #     # fillColor= 'yellow')
    #     )

    # MRI PC
    circle = visual.Circle(
        win=win,
        name='circle', units='pix', 
        ori=0,
        # pos=(0, 0),
        pos=centrepos,
        size=1.0, radius=1.5,
        lineColor='white',
        lineWidth=6.0,
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
            print(f"This component is: {thisComponent}")
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
        
        # Participant will be informed motion/still verbally
        # Could  add a text instruction to the screen prior to metrenome but not necessary
        
        # Present AUDIO stimuli

        # Stimuli Onsets
        vis_met_onset = globalClock.getTime() #.getTime() Returns the current time on this clock in secs (sub-ms precision).
        # Realtime onsets
        vis_met_onset_realtime = datetime.now().strftime("%H:%M:%S:%f")
        print(vis_met_onset_realtime) #13:54:25:525163


        # 10 seconds to practice task before audio starts - is this sufficient?
        audio_delay = 10.00000
        # Stimuli Onsets
        aud_onset = globalClock.getTime() + audio_delay
        # Realtime onsets
        aud_onset_pre_deay = datetime.now() 
        aud_onset_realtime = (aud_onset_pre_deay + timedelta(0,audio_delay)).strftime("%H:%M:%S:%f")

        # breaks on Rhodri's laptop, work's on Aine's 
        # NB Check if works on MRIPC!
        # # GetSecs: returns the time in seconds (with high precision).
        now = ptb.GetSecs()
        print(f"NOW = {now}") #NOW = 14329.307665261
        
         # # breaks on  Aine's laptop - works on Rhodri's windows
        # # audio onset delay
        # audio.play(secs=10.000)
        # audio.play(when=now+10.000000)
        audio.play(when=now+audio_delay) #WORKING VERSION #NOT THE SOURCE OF THE PsychPortAudio-WARNING
        print(f"AUDIO STARTS: {now+audio_delay}") #22013.113607656
        # audio.play() #TRY TEST
        print(f"Audio will start playing in 10 s at {aud_onset_realtime}") 
        # audio.play()


        ev['real_time'] = vis_met_onset_realtime
        ev['onset']=vis_met_onset
        # end of preaudio period = start of audio => end = aud_onset
        ev['duration']=aud_onset-vis_met_onset
        ev['trial_type']='preaudio_metronome'

        #update events_df with this trial
        expt_events = expt_events.append(ev, ignore_index=True)
        #save out events as tsv each time updated
        expt_events.to_csv(save_loc, sep='\t')


        # Allow an extra 5 seconds as stimuli are over running by 5s
        # 10 s pre audio, audio with approx. 5s overrun, 5s post audio
        # Ideally quantify overrun but ok for now.
        len_of_vis_met = dur +20.0 
        print(f"len_of_vis_met: {len_of_vis_met}")
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
            
                # if tThisFlipGlobal > circle.tStartRefresh + len_of_vis_met-frameTolerance: #Working? Version
                if tThisFlipGlobal > (circle.tStartRefresh + len_of_vis_met-frameTolerance):
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

                # Laptop Version
                # ym = 0.15 *(sin(2 * pi * fm * t) *(cos(4 * pi * fm * t)+ 5))/(6 * fm) 
                # yc = 200 + 1200 * A * cos (2 * pi * fc * t + fdelta/fm * ym  ) /3


                # # Edit for MRI PC - do we want to have a perfect circle or is the distorted oval ok?
                # ym = 0.15 *(sin(2 * pi * fm * t) *(cos(4 * pi * fm * t)+ 5))/(6 * fm) 
                
                # # ORIGINAL MODEL
                # # yc = A * cos (2 * pi * fc * t + fdelta/fm * ym  ) /3
                # # Add scaling:
                # yc = 50 + 250 * A * cos (2 * pi * fc * t + fdelta/fm * ym  ) /3
                # # Collapse to Origin - presents as too volatile
                # # yc = 2000 * A * cos (2 * pi * fc * t + fdelta/fm * ym  ) /3


                # Add phase shift - change systemically with subjects
                n = subNum%6
                ym = 0.15 * (sin(2 * pi * fm * (t + (28/6 * n))) *(cos(4 * pi * fm * (t + (28/6 * n)))+ 5))/(6 * fm)
                yc = 50 + 250 * A * cos (2 * pi * fc * (t + (28/6 * n)) + fdelta/fm * ym  ) /3


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
        
        # Metrenome has stopped playing - retrospectivly log the audio and post audio metrenome periods
        # Audio takes longer to play than it should
        # The accuracy of these logs is affected by this!
        # other logs including button presses are unaffected


        # Log the Audio Clip as an event
        ev = {'onset':None,'duration':None,'trial_type':None, 'real_time':None}

        ev['real_time'] = aud_onset_realtime
        ev['onset']=aud_onset
        ev['duration']= dur 
        ev['trial_type']=aud_file

        #update events_df with this trial
        expt_events = expt_events.append(ev, ignore_index=True)
        #save out events as tsv each time updated
        expt_events.to_csv(save_loc, sep='\t')


        # Should this still be here (currently below?)?
        # sync_now = False


        # End Visual Metrenome
        # -------Ending Routine "trial"-------
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)


        # Log the post audio metrenome period as an event
        # AGAIN: Hard coding of durations is leading to errors in logging of these events 
        # Realtime logs would be prefered BUT difficult to resolve due to the nature of the metrenome code
        ev = {'onset':None,'duration':None,'trial_type':None, 'real_time':None}
        
        onset = aud_onset + dur #timedelta?

        print(f"REALTIME {aud_onset_realtime} vs NOW: {datetime.now()}, type realtime{type(aud_onset_realtime)}.")
        print(datetime.now().strftime("%H:%M:%S:%f"))
        # REALTIME 15:03:15:064398 vs NOW: 2022-04-21 15:03:23.086616, type realtime<class 'str'>
        # 15:03:23:086653
        print("test aud onset now: {aud_onset_pre_deay}")

        ev['trial_type'] = 'postaudio_metronome'
        ev['onset'] = onset

        realtime_start = (aud_onset_pre_deay + timedelta(0,audio_delay) + timedelta(0,dur)).strftime("%H:%M:%S:%f")
        ev['real_time'] = realtime_start
        # ev['duration'] = 5.0 

        end = globalClock.getTime() 
        post_aud_dur = end - onset
        ev['duration'] = post_aud_dur

        #update events_df with this trial
        expt_events = expt_events.append(ev, ignore_index=True)
        #save out events as tsv each time updated
        expt_events.to_csv(save_loc, sep='\t')


        sync_now = False

        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()


    