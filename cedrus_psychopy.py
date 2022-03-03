#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 16:16:51 2022

@author: jenny
"""

import serial
import sys
import numpy as np
import glob
from psychopy import visual
from psychopy import core, visual, sound, event, logging
import struct
from cedrus_util import *


# get portname
portname, keymap = getname()


# create a window if the key press is red button, exit
win = visual.Window([100,100], units="pix")
grating = visual.GratingStim(win=win, mask="circle", size=10, pos=[0,0], sf=3)
text = visual.TextStim(win=win, text = 'pressed!')


# logging for frame detection
win.recordFrameIntervals = True    
win.refreshThreshold = 1/60 + 0.004
logging.console.setLevel(logging.WARNING)   #this will print if there is a delay



s = serial.Serial(portname, 115200) 



############# Trial begins #######################

# reset RT and base timer


timer = core.Clock()


keylist = []
clear_buffer(s)   # clear the input and output buffer in case there is a queue
reset_timer(s)    # reset responsebox timer
timer.reset()     # reset psychopy timer

for frameN in range(60*5):
    grating.draw()
    win.flip()
    k = s.in_waiting
    if  k != 0:
        t1= timer.getTime()
        keylist.append(s.read(s.in_waiting))
        key, press, time = readoutput([keylist[-1]], keymap)
        if press == [1]:
            text.draw()
            win.flip()
        if key[0] == 2:
            break
win.close()
        
# # convert the time of correct button push
# t = BytesListToHexList(time)
# rt = HexToRt(t)
# print('rt of the correct key press: ', rt)
# print('psychopy timer: ', t1*1000)

# convert the time of all button pushes

keys, pressed, times = readoutput(keylist, keymap)
times = BytesListToHexList(times)
times = np.array([HexToRt(i) for i in times])
keys = np.array(keys)
pressed = np.array(pressed)
print('RT:', times[pressed==1])
print('Keys:', keys[pressed==1])


