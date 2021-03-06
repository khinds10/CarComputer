#!/usr/bin/python
# Show on/off indicator lights for if internet connected and if GPS location found
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
        isConnected = subprocess.check_output(['bash', '/home/pi/CarComputer/computer/connection.sh'])
        isConnected = isConnected.strip()
       
        # turn on/off internet connected indicator
        if isConnected == "ok":
            setLight(13, 1)
        else:
            setLight(13, 0)

        # check GPS status and turn on light if no issues
        currentLocationInfo = data.getCurrentLatLong()
        setLight(15, 1)
        
    except (Exception):
        # GPS issue, turn off light
        setLight(15, 0)
    
    time.sleep(1)
