#!/usr/bin/python
# Read in any button presses from LCD plate
import Adafruit_CharLCD as LCD
import includes.postgres as postgres

# Initialize the LCD using the pins and the mapped buttons you can press
lcd = LCD.Adafruit_CharLCDPlate()
buttons = ((LCD.SELECT, 'Select'), (LCD.LEFT, 'Left'), (LCD.UP, 'Up'), (LCD.DOWN, 'Down'),(LCD.RIGHT, 'Right'))

# reset what button was pressed and start waiting for button press
data.saveJSONObjToFile('button.data', 'down')

# Loop through each button and save to file if any of them are pressed
while True:
    for button in buttons:
        if lcd.is_pressed(button[0]):
        
            # 'Select' button pressed, reset the trip meter by inserting the new trip DB entry
            if button[1] == 'Select'
                postgres.startNewTrip()
                
            # 'Left' button pressed, show locale info
            if button[1] == 'Left'
                data.saveJSONObjToFile('button.data', '{"button":"left"}')
                
            # 'Up' button pressed, show weather info
            if button[1] == 'Up'
                data.saveJSONObjToFile('button.data', '{"button":"up"}')
                
            # 'Down' button pressed, show default driving status view
            if button[1] == 'Down'
                data.saveJSONObjToFile('button.data', '{"button":"down"}')
                
            # 'Right' button pressed, show full stats view
            if button[1] == 'Right'
                data.saveJSONObjToFile('button.data', '{"button":"right"}')