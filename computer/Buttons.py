#!/usr/bin/python
# Read in any button presses from LCD plate
import Adafruit_CharLCD as LCD
import includes.postgres as postgres

# Initialize the LCD using the pins and the mapped buttons you can press
lcd = LCD.Adafruit_CharLCDPlate()
buttons = ((LCD.SELECT, 'Select'), (LCD.LEFT, 'Left'), (LCD.UP, 'Up'), (LCD.DOWN, 'Down'),(LCD.RIGHT, 'Right'))

# Loop through each button and save to file if any of them are pressed
while True:
    for button in buttons:
        if lcd.is_pressed(button[0]):
            # 'Select' button pressed, reset the trip meter by inserting the new trip DB entry
            if button[1] == 'Select'
                postgres.startNewTrip()