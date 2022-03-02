#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 13:00:45 2022

@author: hnl
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



# ser = serial.Serial(ports(p),115200,"Timeout",1);


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/ttyUSB*')  # ubuntu is /dev/ttyUSB0
    elif sys.platform.startswith('darwin'):
        # ports = glob.glob('/dev/tty.*')
        ports = glob.glob('/dev/tty.SLAB_USBtoUART*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except serial.SerialException as e:
            if e.errno == 13:
                raise e
            pass
        except OSError:
            pass
    return result

  # %In order to identify an XID device, you need to send it "_c1", to
  #   %which it will respond with "_xid" followed by a protocol value. 0 is
  #   %"XID", and we will not be covering other protocols.


def send_ser_command(device, command, bytes_expected=0):
    device.write(command)
    response = device.read(bytes_expected)

    return response



def identiy_device():
    portname = serial_ports()[0]
    with serial.Serial(portname, 115200, timeout=1) as ser:
        ser.write(b"_c1")  # byte string
        query_return = ser.read(5)
        print('device response: ', query_return)

    if (len(query_return)) > 0 & (query_return == b"_xid0"):
        print('device detected!')





def get_model():
 # identify which device we're speaing to
    with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
        ser.write(b"_d2")  # byte string
        device_id = ser.read(1)

        ser.write(b"_d3")  # byte string
        model_id = ser.read(1)
    return device_id, model_id




def def_keyboard(device_id, model_id):
    rb_540_keymap = [-1, 0, -1, 1, 2, 3, 4, -1]
    rb_740_keymap = [-1, 0, 1, 2, 3, 4, 5, 6]
    rb_840_keymap = [7, 3, 4, 1, 2, 5, 6, 0]
    rb_834_keymap = [7, 0, 1, 2, 3, 4, 5, 6]
    lumina_keymap = [-1, 0, 1, 2, 3, 4, -1, -1]
    keymap = []

    if device_id == b'2':
        if model_id == b'1':
            keymap = rb_540_keymap
        elif model_id == b'2':
            keymap = rb_740_keymap
        elif model_id == b'3':
            keymap = rb_840_keymap
        elif model_id == b'4':
            keymap = rb_834_keymap
        else:
            print("An unknown RB model was detected. Very strange.")
            keymap == []
    if keymap:
        print('keymap found')
    else:
        print('no keymap')
    return keymap






def decimalToBinary(n):
    return bin(n).replace("0b", "")


def dtob(num):

    if num >= 1:
        dtob(num // 2)
    print(num % 2, end='')
    
#    ser = serial.Serial('/dev/ttyUSB0')  # open serial port
# print(ser.name)         # check which port was really used
# ser.write(b'hello')     # write a string
# ser.close()


# win = visual.Window(
#     size=[400, 400],
#     units="pix",
#     fullscr=False
# )


# timer.reset()
# resp,time = readKeypress(portname, keymap)
# timer.getTime()


# k=[]
# timer.reset()
# for i in range(0,240):
#     win.flip()
#     resp,time = readKeypress(portname, keymap)
#     # keys = event.getKeys(timeStamped=True)
#     k += resp
# timer.getTime()

# win.close()


# def readKeypress(portname, keymap):
#     resp = []
#     respInfo = []
#     key = []
#     pressed = []

#     # with serial.Serial(portname, 115200, timeout=1) as ser:
#     #     send_ser_command(ser, b'e1')
#     #     send_ser_command(ser, b'e5')
#     #     time= send_ser_command(ser, b'e3',6)
#     #     ser.close()
#     timer = core.Clock()
#     for i in range(0, 1):
#         with serial.Serial(portname, 115200, timeout=1) as ser:
#             # send_ser_command(ser, b'e1')
#             # send_ser_command(ser, b'e5')
#             k = ser.read(10)
#             # print(k)
#         if not k:
#             pass
#         else:
#             resp.append(k)
#             respInfo = list(decimalToBinary(resp[0][1]))
#             respInfo = [(int(i)) for i in respInfo]
#             respInfo = np.pad(respInfo, (8-len(respInfo), 0))
#             key = respInfo[2] + respInfo[1]*2 + respInfo[0]*4
#             # port = respInfo[7] + respInfo[6]*2 + respInfo[5]*4 + respInfo[4]*8
#             pressed = respInfo[3]
#             key = keymap[key]
#             # stamp = struct.unpack('>HH',resp[0][2:6])
#         # print(timer.getTime())

#     # print(timer.getTime())
#     return resp, key, pressed


def fastreadKeypress(portname, keymap):
    resp = []
    respInfo = []
    key = []
    pressed = []
    timer = core.Clock()
    for i in range(0, 1):
        with serial.Serial(portname, 115200) as ser:
            # send_ser_command(ser, b'e1')
            # send_ser_command(ser, b'e5')
            k = ser.read(6)
            # print(k)
        if not k:
            pass
        else:
            resp.append(k)
            respInfo = list(decimalToBinary(resp[0][1]))
            respInfo = [(int(i)) for i in respInfo]
            respInfo = np.pad(respInfo, (8-len(respInfo), 0))
            key = respInfo[2] + respInfo[1]*2 + respInfo[0]*4
            # port = respInfo[7] + respInfo[6]*2 + respInfo[5]*4 + respInfo[4]*8
            pressed = respInfo[3]
            key = keymap[key]
            # stamp = struct.unpack('>HH',resp[0][2:6])
            stamp = resp[0][2:6]
        # print(timer.getTime())

    # print(timer.getTime())
    return resp, key, pressed, stamp




# set up resposne pad
portname = serial_ports()[0]
print('writing to device...')
identiy_device()
device_id, model_id = get_model()
keymap = def_keyboard(device_id, model_id)

def getKeypress(portname, keymap):
    resp = []
    respInfo = []
    key = []
    pressed = []
    timer = core.Clock()
    s = serial.Serial(portname, 115200, timeout=None) 
    s.write(b'e1')
    s.write(b'e5')
    k = s.read(6)
            # print(k)
    if not k:
        pass
    else:
        resp.append(k)
        respInfo = list(decimalToBinary(resp[0][1]))
        respInfo = [(int(i)) for i in respInfo]
        respInfo = np.pad(respInfo, (8-len(respInfo), 0))
        key = respInfo[2] + respInfo[1]*2 + respInfo[0]*4
        # port = respInfo[7] + respInfo[6]*2 + respInfo[5]*4 + respInfo[4]*8
        pressed = respInfo[3]
        key = keymap[key]
        # stamp = struct.unpack('>HH',resp[0][2:6])
        stamp = resp[0][2:6]
        # print(timer.getTime())

    # print(timer.getTime())
    return resp, key, pressed, stamp




import time
    
# def fastreadKeypress(portname, keymap):
#     resp = []
#     key = []
#     pressed = []
#     s = serial.Serial(portname, 115200)

#     k = s.read(6)

#     resp.append(k)
#     if k:
#         respInfo = list(decimalToBinary(resp[0][1]))
#         respInfo = [(int(i)) for i in respInfo]
#         respInfo = np.pad(respInfo, (8-len(respInfo), 0))
#         key = respInfo[2] + respInfo[1]*2 + respInfo[0]*4
#         # port = respInfo[7] + respInfo[6]*2 + respInfo[5]*4 + respInfo[4]*8
#         key = keymap[key]
#         pressed = respInfo[3]
#     if k:
#         s = serial.Serial(portname, 115200, timeout=1)

#         k = s.read(6)

#     stamp =resp[0][2:6]

#     return key, pressed, stamp


# timer = core.Clock()

def test_myfunction():
    print('press now')
    timer = core.Clock()
    timer.reset()
    key = fastreadKeypress(portname, keymap)
    t1= timer.getTime()
    return ('function takes %s to run ',t1)
    

def test_trialresponse():
    rt = [(0,0)]*10
    c = 0
    core.wait(1)
    s= serial.Serial(portname, 115200, timeout=2)   
    
    flag = False
    timer = core.Clock()
    timer.reset()
    
    ts=timer.getTime()
    while flag is False:
        key,p = fastreadKeypress(portname, keymap)
        if p==1:
            t = timer.getTime()
            rt[c] = (key,t)
            c +=1
        if timer.getTime()>=2:
            flag = True
            te = timer.getTime()
    print('trial begins and end:',ts, te)
    return rt






def test_trialresponse():
    rt = [(0,0)]*10
    c = 0
    core.wait(1)
    s= serial.Serial(portname, 115200, timeout=2)   
    
    flag = False
    timer = core.Clock()
    timer.reset()
    
    ts=timer.getTime()
    while flag is False:
        k = s.read(6)
        if k:
            t = timer.getTime()
            rt[c] = (k,t)
            c +=1
        if timer.getTime()>=2:
            flag = True
            te = timer.getTime()
    print('trial begins and end:',ts, te)
    return rt


def test_serialport():
    core.wait(1)
    s= serial.Serial(portname, 115200, timeout=2)   
    
    flag = False
    timer = core.Clock()
    timer.reset()
    
    ts=timer.getTime()
    while flag is False:
        k = s.read(6)
        if k:
            t = timer.getTime()
            rt[c] = (k,t)
            c +=1
        if timer.getTime()>=2:
            flag = True
            te = timer.getTime()
    print('trial begins and end:',ts, te)
    return rt


    
# print('device', serial_ports())
# portname = serial_ports()[0]
# print('writing to device...')
# identiy_device()

# device_id, model_id = get_model()
# keymap = def_keyboard(device_id, model_id)



# t = struct.unpack('>HH', time[2:6])

# for i in range(len(resp)):
#     respInfo = list(decimalToBinary(resp[i][1]))
#     respInfo = [(int(i)) for i in respInfo]
#     respInfo = np.pad(respInfo, (8-len(respInfo), 0))
#     key = respInfo[2] + respInfo[1]*2 + respInfo[0]*4
#     port = respInfo[7] + respInfo[6]*2 + respInfo[5]*4 + respInfo[4]*8
#     pressed = respInfo[3]
#     key = keymap[key]
#     stamp = struct.unpack('>HH', resp[i][2:6])
#     print('key', key, '\nport', port, '\npressed', pressed,
#           'stamp', stamp)

#     stamp = typecast(int8(k(3:6)),'int32');

#     # Convert the bits to an array
#     respInfo = logical(dec2bin(k(2))-'0');
#     %Pad out the array with zeroes
#     respInfo = [zeros(1, 8-length(respInfo)), respInfo];

#     %Here is how the response packet breaks down:
#     % The first byte is simply the letter “k”, lower case
#     % The second byte consists is divided into the following bits:
#     %  Bits 0-3 store the port number.
#     %  Bit 4 stores whether the key was pressed (1) or released(0)
#     %  Bits 5-7 indicate which push button was pressed.
#     key = int8(respInfo(3) + respInfo(2)*2 + respInfo(1)*4);
#     pressed = respInfo(4);
#     port = respInfo(8) + respInfo(7)*2 + respInfo(6)*4 + respInfo(5)*8;

#     fprintf("Key: %d\n", keymap(key+1))
#     fprintf("Pressed: %d\n", pressed)
#     fprintf("Port: %d\n", port)
#     fprintf("Timestamp: %d\n\n",stamp)
# end
