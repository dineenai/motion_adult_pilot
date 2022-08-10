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
        lineWidth=6.0
        # fillColor= 'yellow')
        )

    root_dir = '/Users/aine/Documents/CusackLab/robust_motion_correction_for_mri_using_dnns/pilot_paradigm/motion_adult_pilot/'
    print(f"Root dir is: {root_dir}")
    save_len_loc = os.path.join(root_dir,f'audio_clip_length_{aud_file}.tsv')

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

        # EVENTS FOR CLIP LENGTH
        dur = audio.getDuration()
        # trialClock = core.Clock()
        audio_len = pd.DataFrame(columns=['audio_file','actual_len','playing_len'])
        ev = {'audio_file':None, 'actual_len':None,'playing_len':None}
        ev['audio_file'] = aud_file
        ev['actual_len'] = dur


        audio.play() 
        onset = globalClock.getTime() 

        len_of_vis_met = dur +20.0 

        # while continueRoutine > 0:
        while audio.status == PLAYING:
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


                # Edit for MRI PC - do we want to have a perfect circle or is the distorted oval ok?
                ym = 0.15 *(sin(2 * pi * fm * t) *(cos(4 * pi * fm * t)+ 5))/(6 * fm) 
                
                # ORIGINAL MODEL
                # yc = A * cos (2 * pi * fc * t + fdelta/fm * ym  ) /3
                # Add scaling:
                yc = 50 + 250 * A * cos (2 * pi * fc * t + fdelta/fm * ym  ) /3
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

        # POST METRENOME PERIOD........
        # How do I log the lengh of the stimulus?????????
        end = globalClock.getTime() 
        ev['playing_len'] = end - onset

        audio_len = audio_len.append(ev, ignore_index=True)
        #save out events as tsv each time updated
        audio_len.to_csv(save_len_loc, sep='\t')


        # End Visual Metrenome
        # -------Ending Routine "trial"-------
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)


        sync_now = False

        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()


    