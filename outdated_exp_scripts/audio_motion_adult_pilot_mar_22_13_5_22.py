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
    pre_flip_time = []
    loop_start_time = []
    loop_end_time = []
    loop_length = []

    audio_status = []
    audio_status_time = []
    
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
        # SHOULD ADUIO BE A TRIAL COMPONENT - NO AS DOES NOT RESETART WITH EACH TRIAL!
        trialComponents = [circle]
        for thisComponent in trialComponents:
            print(f"This component is: {thisComponent}")
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
                # print(f'THIS PRINTS IF THE CIRCLE HAS ATTR STATUS!!!, {thisComponent.status}') #prints!
                # thisComponent: Circle(__class__=<class 'psychopy.visual.circle.Circle'>, autoDraw=False, etc.
        
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        print(f'_timeToFirstFrame is: {_timeToFirstFrame} ') # eg. 0.004471029301566176, 0.01110622899432201

        print(f'PRE-RESET trialClock STRAT TIME: {trialClock.getTime()}') #0.6545188300005975
        trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        print(f'trialClock STRAT TIME: {trialClock.getTime()}') #0.011109428995041526
        frameN = -1

        #reset event dict for this stimulus
        ev = {'onset':None,'duration':None,'trial_type':None, 'real_time':None}
    
        # Present AUDIO stimuli

        # Stimuli Onsets
        
        # # SHOULD I subtract time to first flip
        # vis_met_onset = globalClock.getTime() #.getTime() Returns the current time on this clock in secs (sub-ms precision). 
        # TRY: -_timeToFirstFrame
        vis_met_onset = globalClock.getTime()-_timeToFirstFrame

        print(f"trialClock: {trialClock.getTime()} vs globalClock.getTime() {globalClock.getTime()}")

        # Realtime onsets
        vis_met_onset_realtime = datetime.now().strftime("%H:%M:%S:%f")
        print(vis_met_onset_realtime) #13:54:25:525163
        print(f'timedelta(0,_timeToFirstFrame):  {timedelta(0,_timeToFirstFrame)}') #timedelta(0,_timeToFirstFrame):  0:00:00.014873

        # (datetime.now() - timedelta(0,_timeToFirstFrame)).strftime("%H:%M:%S:%f")
        print(f'vis_met_onset_realtime {vis_met_onset_realtime} ,  {(datetime.now() - timedelta(0,_timeToFirstFrame)).strftime("%H:%M:%S:%f")}')
        # CANNOT DO THIS {vis_met_onset_realtime-timedelta(0,_timeToFirstFrame)}!!!


        # 10 seconds to practice task before audio starts - is this sufficient?
        audio_delay = 10.00000
        # Stimuli Onsets
        aud_onset = globalClock.getTime() + audio_delay
        # Realtime onsets
        aud_onset_pre_delay = datetime.now() 
        aud_onset_realtime = (aud_onset_pre_delay + timedelta(0,audio_delay)).strftime("%H:%M:%S:%f")
        
        print(f'INITIAL {ptb.GetSecs()}')
        nextFlip = win.getFutureFlipTime(clock='ptb')
        # instead of nextflip

        print(f"nextFlip {nextFlip} vs ptb.GetSecs() {ptb.GetSecs()}") #nextFlip 3137.1734444529993 vs ptb.GetSecs() 3137.169162458
        audio.play(when=nextFlip+audio_delay) 
        # does it need to be ptb
        audio_status.append(audio.status)

        print(f"REAL AUDIO START????? {nextFlip}") # 9543.487606745703

        # instead of getSetc can use next clip or something
        # Window.getFutureFlipTime(clock=’ptb’) if you want a synchronized time:
        
        # audio_status_time.append(ptb.GetSecs())
        # TRY + nextFlip
        # audio_status_time.append(ptb.GetSecs()+nextFlip)

        # CHANGE TO NEXTFLIP - BAISI?????
        audio_status_time.append(nextFlip)

        # print(f"AUDIO STARTS: {now+audio_delay}") #22013.113607656
        print(f"Audio will start playing in 10 s at {aud_onset_realtime}") 

        ev['real_time'] = vis_met_onset_realtime
        ev['onset']=vis_met_onset
        # end of preaudio period = start of audio => end = aud_onset
        ev['duration']=aud_onset-vis_met_onset
        ev['trial_type']='preaudio_metronome'

        #update events_df with this trial
        expt_events = expt_events.append(ev, ignore_index=True)
        
        # around 6 ms for save
        print(f'pre save: s{ptb.GetSecs()}')
        #save out events as tsv each time updated
        expt_events.to_csv(save_loc, sep='\t')
        print(f'post save: s{ptb.GetSecs()}')


        # Allow an extra 5 seconds as stimuli are over running by 5s
        # 10 s pre audio, audio with approx. 5s overrun, 5s post audio
        # Ideally quantify overrun but ok for now.
        # len_of_vis_met = dur +20.0 

        # CHANGE TO WHAT IT SHOULD BE: 10 pre aduio, 5 post audio
        len_of_vis_met = dur +15.0 

        print(print(f'POST {ptb.GetSecs()}'))
        print(f"len_of_vis_met: {len_of_vis_met}")
        # while continueRoutine and routineTimer.getTime() > 0:
        while continueRoutine > 0:
            # print(f"START: {ptb.GetSecs()}" )
            audio_status.append(audio.status)
            audio_status_time.append(ptb.GetSecs())
            
            start_pre_flip_time = ptb.GetSecs()
            loop_start_t = ptb.GetSecs()

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


                # print(f'pre size change: {ptb.GetSecs()}')

                # Set Radius of the Circle
                # Do we want to have a perfect circle or is the distorted oval ok? If former, edit for MRI PC
                # Collapse to Origin - presents as too volatile, translate in y-direction
                # Add phase shift (28/6 * n) - change systematically with subjects

                fc = 1/7
                fdelta = 0.6 * fc
                A = 0.2
                fm = 1/28

                # Laptop Version
                # ym = 0.15 *(sin(2 * pi * fm * t) *(cos(4 * pi * fm * t)+ 5))/(6 * fm) 
                # yc = 200 + 1200 * A * cos (2 * pi * fc * t + fdelta/fm * ym  ) /3
                
                # MRI PC
                n = subNum%6
                ym = 0.15 * (sin(2 * pi * fm * (t + (28/6 * n))) *(cos(4 * pi * fm * (t + (28/6 * n)))+ 5))/(6 * fm)
                yc = 50 + 250 * A * cos (2 * pi * fc * (t + (28/6 * n)) + fdelta/fm * ym  ) /3

                circle.setSize(yc, log=False)

                # print(f'post size change: {ptb.GetSecs()}')

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
                # print(f"AFTER T: {ptb.GetSecs()}" )
                
                # print(f'Before flip: {t_bef}')
                
                # end_pre_flip_time = ptb.GetSecs() #move 9/6/22
                
                # remove long sleep, replaced with multiple short sleeps to enable repeated audio status recording
                # time.sleep(0.005)

                # sleep for 0.0005 s x 10 ie 5 ms - but slipt be 10 to allow higher precision audio status recording and => script timing
                for i in range(10):
                    time.sleep(0.0005)
                    # print(f'Audio Status is: {audio.status}')

                    audio_status.append(audio.status)
                    audio_status_time.append(ptb.GetSecs())

                end_pre_flip_time = ptb.GetSecs() #move 9/6/22
                
                t_bef = ptb.GetSecs()

                win.flip()

                t_af = ptb.GetSecs()
                # print(f'After flip: {t_af}')

                pre_flip_dif = end_pre_flip_time - start_pre_flip_time 

                flip_dif = t_af - t_bef
                # print(f'Dif befor and after flip: {flip_dif}')

                flip_time.append(flip_dif)
                pre_flip_time.append(pre_flip_dif)

                # # while audio.status != FINISHED:
                keys = event.getKeys()

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
            
                if 'c' in keys: #Changed from d to c - new NNL leads
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
            t_end = ptb.GetSecs()
            loop_end_t = ptb.GetSecs()
            loop_t_dif = loop_end_t - loop_start_t
            
            loop_start_time.append(loop_start_t)
            loop_end_time.append(loop_end_t)
            loop_length.append(loop_t_dif)

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

        # End Visual Metrenome
        # -------Ending Routine "trial"-------
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)

        print(f"END OF EXPERIMENT: {ptb.GetSecs()}")

        # Log the post audio metrenome period as an event
        # AGAIN: Hard coding of durations is leading to errors in logging of these events 
        # Realtime logs would be prefered BUT difficult to resolve due to the nature of the metrenome code
        ev = {'onset':None,'duration':None,'trial_type':None, 'real_time':None}
        
        onset = aud_onset + dur 

        # print(f"REALTIME {aud_onset_realtime} vs NOW: {datetime.now()}, type realtime{type(aud_onset_realtime)}.")
        # print(datetime.now().strftime("%H:%M:%S:%f"))
        # # REALTIME 15:03:15:064398 vs NOW: 2022-04-21 15:03:23.086616, type realtime<class 'str'>
        # # 15:03:23:086653
        # print(f"test aud onset now: {aud_onset_pre_delay}")

        ev['trial_type'] = 'postaudio_metronome'
        ev['onset'] = onset

        realtime_start = (aud_onset_pre_delay + timedelta(0,audio_delay) + timedelta(0,dur)).strftime("%H:%M:%S:%f")
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

        print(f'Min value is: {min(flip_time)} Max: {max(flip_time)} avg: {average(flip_time)}')

        plot = plt.hist(flip_time)
        # plt.savefig('foo2.png', bins=[0.01109236799993596])
        
        # id = 'PCH_sleep_0.0005x10_23_5_22'
        id = 'cat_sleep_0.0005x10_v3'

        output_dir = "/Users/aine/Documents/CusackLab/robust_motion_correction_for_mri_using_dnns/pilot_paradigm/motion_adult_pilot/test_outputs_23_5_22"
  
        
        # Path
        path = os.path.join(output_dir, id)
        os.mkdir(path)
        # id = 'cat'
        plt.savefig(f'test_outputs_23_5_22/{id}/{id}.png') #ADD PATH

        print(f"len: {len(flip_time)}\n{len(pre_flip_time)} \n{len(loop_start_time)} \n{len(loop_end_time)}\n {len(loop_length)}")

        # dictionary of lists (just one list) 
        dict = {'flip_time': flip_time, 'pre_flip_time': pre_flip_time}     
        dict2 = {'loop_start_time':loop_start_time, 'loop_end_time':loop_end_time, 'loop_length':loop_length} 
        df = pd.DataFrame(dict) 
        df2 = pd.DataFrame(dict2) 
        # saving the dataframe 
        df.to_csv(f'test_outputs_23_5_22/{id}/win_flip_{id}.csv')  #add path
        df2.to_csv(f'test_outputs_23_5_22/{id}/win_flip_{id}_loop.csv')  #add path

        aud_dict = {'audio_status': audio_status, 'audio_status_time': audio_status_time}  
        aud_df = pd.DataFrame(aud_dict)  

        print(aud_df[aud_df.audio_status == -1].index[0])
        # print(aud_df[aud_df.audio_status == -1].index[0])
        print(aud_df['audio_status_time'][aud_df[aud_df.audio_status == -1].index[0]])
        # time audio stops
        audio_stop = aud_df['audio_status_time'][aud_df[aud_df.audio_status == -1].index[0]]
        audio_start = aud_df['audio_status_time'][0]
        audio_TIME = audio_stop - audio_start
        print(f'AUDIO STOP: {audio_stop}')
        print(f"AUDIO TIME IS {audio_TIME}")

        aud_df.to_csv(f'test_outputs_23_5_22/{id}/aud_{id}.csv')  #add path

        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()


    