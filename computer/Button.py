#! /usr/bin/python
# Listen for button local presses
# Kevin Hinds http://www.kevinhinds.com / Dan Mandle http://dan.mandle.me
# License: GPL 2.0
import RPi.GPIO as GPIO
import time
import includes.data as data
import info.ButtonPressed as ButtonPressed

# setup button for BCM pin #25
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# listen for button press and save to file if it happened
while True:
    input_state_button1 = GPIO.input(24)
    if input_state_button1 == False:
        buttonPressed = ButtonPressed.ButtonPressed()
        buttonPressed.buttonName = 'button1'
        print buttonPressed
        data.saveJSONObjToFile('button.data', buttonPressed)
        time.sleep(0.2)
    input_state_button2 = GPIO.input(17)
    if input_state_button2 == False:
        buttonPressed = ButtonPressed.ButtonPressed()
        buttonPressed.buttonName = 'button2'        
        data.saveJSONObjToFile('button.data', buttonPressed)
        time.sleep(0.2)
