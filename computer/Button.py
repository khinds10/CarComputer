#! /usr/bin/python
# Kevin Hinds http://www.kevinhinds.com / Dan Mandle http://dan.mandle.me
# License: GPL 2.0
import RPi.GPIO as GPIO
import time
import includes.data as data
import info.ButtonPressed as ButtonPressed

# setup button for BCM pin #25
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# listen for button press and save to file if it happened
while True:
    input_state = GPIO.input(25)
    if input_state == False:
        buttonPressed = ButtonPressed.ButtonPressed()
        buttonPressed.buttonName = 'button1'
        data.saveJSONObjToFile('button.data', buttonPressed)
        time.sleep(0.2)