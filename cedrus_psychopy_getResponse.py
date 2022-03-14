# Created on 3/14/22 at 11:47 AM 

# Author: Jenny Sun

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 16:16:51 2022

@author: jenny
"""

'''this script demonstrates how to display the stimulus 
and get response from the buffer without needing to read from frame to frame 
'''

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


# open the serial port
s = serial.Serial(portname, 115200)

# trial function
# display the stimulus for a period of time
# quit if a button is pressed


timer = core.Clock()
def trial(port, frames, startframe,abortKey):
    clear_buffer(port)  # clear the input and output buffer in case there is a queue
    # display the stimulus
    for f in range(0,frames):
        if f == startframe:
            grating.draw()
            timer.reset()
            reset_timer(port)  # reset responsebox timer if the stimulus starts
        grating.draw()
        win.flip()

    # get response from the buffer if any key is pressed
    keylist = []
    key = []
    k = port.in_waiting

    # if no complete key pressed is detected keep detecting
    while k < 6:     # 6 bytes is one key press
        k = port.in_waiting
    t1 = timer.getTime()
    keylist.append(port.read(6))
    print(keylist)
    key, press, btime = readoutput([keylist[-1]],keymap)
    if key[-1] == abortKey:
        win.close()
        port.close()
        core.quit()
    if press[0] ==0:
        key[-1] =[]
        print('trial skipped')
    return (key[-1],btime,t1, press)


[resp, rt, t1, press] = trial(port=s, frames=30, startframe=0, abortKey=4)
win.close()   # close the window when response is detected
if resp == 2:      # assuming 2 is the correct response
    print('correct')
else:
    print('incorrect')

# convert RT and compare it with psychopy timer
rt = HexToRt(BytesListToHexList(rt))
print(resp, rt, t1)