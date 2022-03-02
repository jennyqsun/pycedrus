#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 16:16:51 2022

@author: jenny
"""


# import pyxid2 as pyxid

# # get a list of all attached XID devices
# devices = pyxid.get_xid_devices()

# dev = devices[0] # get the first device to use
# if dev.is_response_device():
#     dev.reset_base_timer()
#     dev.reset_rt_timer()

#     while True:
#         dev.poll_for_response()
#         if dev.response_queue_size() > 0:
#             response = dev.get_next_response()
#             # do something with the response


import serial
import sys
import numpy as np
import glob
from psychopy import visual
from psychopy import core, visual, sound, event, logging
import struct
from cedrus_example import *


def hextort(t):
    rt = [t[i:i+2] for i,j in enumerate(t) if i%2 ==0 ][::-1]
    rt = ''.join(map(str,rt))
    rt = int(rt,16)
    return rt

portname, keymap = getname()




win = visual.Window([100,100], units="pix")
grating = visual.GratingStim(win=win, mask="circle", size=10, pos=[0,0], sf=3)
text = visual.TextStim(win=win, text = 'pressed!')



s = serial.Serial(portname, 115200) 


# reset RT and base timer
timer = core.Clock()

s.write(b'e1')   #reset RT and base timer
s.write(b'e5')
key = []
timer.reset()
for frameN in range(60*5):
    grating.draw()
    win.flip()
    k = s.in_waiting
    if  k != 0:
        t1= timer.getTime()
        text.draw()
        win.flip()
        key.append(s.read(s.in_waiting))
        key, press, time = readoutput([key[-1]], keymap)
        if key[0] == 2:
            break

t = time[0].hex()
rt = hextort(t)
print('rt: ', rt)
win.close()

