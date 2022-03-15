
# pycedrus

## python library for communication between Cedrus response pad and Linux machine using Pyserial. 
### Contains code to integrate the response to psychopy
### Currently works for Ubuntu 20.08. 

cedrus_utils.py contains utility functions  
cedrus_psychopy.py gives an example of integrating to psychopy frame control and precision test  

currently works for all cedurs response pad models  

Problem shoot:

if fail to open the serial port, type the following command line in terminal:

sudo usermod -a -G tty username

then reboot the machine

sudo reboot






