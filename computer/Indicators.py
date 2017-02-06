#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, subprocess
import RPi.GPIO as GPIO
import includes.data as data

# to use Raspberry Pi board pin numbers  
GPIO.setmode(GPIO.BOARD)
 
# set up GPIO output channel
GPIO.setup(13, GPIO.OUT)
GPIO.output(13,GPIO.LOW)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15,GPIO.LOW)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16,GPIO.LOW)

def setLight(pin, isLit):
    """ set light to on or off based on boolean value """
    if isLit:
        GPIO.output(pin,GPIO.HIGH)
    else:
        GPIO.output(pin,GPIO.LOW)

# turn on and off indicator lights based on GPS and Internet connectivity
while True:
    try:

        # get if the internet is connected or not "ok" / "error"
        isConnected = subprocess.check_output(['bash', 'connection.sh'])
        isConnected = isConnected.strip()
       
        # turn on/off internet connected indicator
        if isConnected == "ok":
            setLight(15, 1)
        else:
            setLight(15, 0)

        # check GPS status and turn on light if no issues
        currentLocationInfo = data.getCurrentLatLong()
        setLight(16, 1)
        
    except (Exception):
        # GPS issue, turn off light
        setLight(16, 0)
    
    time.sleep(1)